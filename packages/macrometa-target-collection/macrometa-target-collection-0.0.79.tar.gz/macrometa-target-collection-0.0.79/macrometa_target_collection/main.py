#!/usr/bin/env python3

import argparse
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from threading import Lock

import jsonschema
import requests
from adjust_precision_for_schema import adjust_decimal_precision_for_schema
from c8 import C8Client, DocumentInsertError
from c8.collection import StandardCollection
from jsonschema import Draft4Validator
from prometheus_client import Counter, Gauge, start_http_server
from singer import get_logger
from typing import AsyncIterable

from macrometa_target_collection import extract_gdn_host

logger = get_logger('macrometa_target_collection')

DEFAULT_BATCH_SIZE_ROWS = 500
DEFAULT_BATCH_FLUSH_INTERVAL = 10
DEFAULT_MIN_BATCH_FLUSH_TIME_GAP = 10

# Prometheus metrics
ingested_bytes = Counter('ingested_bytes', 'Total number of bytes ingested', ['region', 'tenant', 'fabric', 'workflow'])
ingested_documents = Counter('ingested_documents', 'Total number of documents ingested',
                             ['region', 'tenant', 'fabric', 'workflow'])
ingest_errors = Counter('ingest_errors', 'Total number of errors during ingestion',
                        ['region', 'tenant', 'fabric', 'workflow'])
ingest_lag = Gauge('ingest_lag', 'Average time lag between data changes in GDN collections and external data sources',
                   ['region', 'tenant', 'fabric', 'workflow'])
scrape_complete_flag = Counter("scrape_complete_flag", "Flag to check if the last scrape has been completed",
                               ['workflow'])

region_label = os.getenv("GDN_FEDERATION", "NA")
tenant_label = os.getenv("GDN_TENANT", "NA")
fabric_label = os.getenv("GDN_FABRIC", "NA")
workflow_label = os.getenv("WORKFLOW_UUID", "NA")
metric_service_url = os.getenv("METRIC_SERVICE_API")
is_metrics_enabled = os.getenv("MACROMETA_TARGET_COLLECTION_IS_METRICS_ENABLED", 'False')

# Start the Prometheus HTTP server for exposing metrics
if is_metrics_enabled.lower() == 'true':
    logger.info("Target is starting the metrics server.")
    start_http_server(8000)


class RecordBatch:
    """Class wrapping the record batch in order to make it thread safe."""

    def __init__(self, config: dict):
        self._list = list()
        self._delete_list = set()
        self._lock = Lock()
        self.interval = config.get('batch_flush_interval', DEFAULT_BATCH_FLUSH_INTERVAL)
        self.last_executed_time = datetime.now(timezone.utc)
        self.min_time_gap = config.get('batch_flush_min_time_gap', DEFAULT_MIN_BATCH_FLUSH_TIME_GAP)
        self.max_batch_size = config.get('batch_size_rows', DEFAULT_BATCH_SIZE_ROWS)
        self.is_completed = False

    def append(self, value, delete=False) -> None:
        """Acquire the lock and add a record to the list."""
        with self._lock:
            if not delete:
                self._list.append(value)
            else:
                self._delete_list.add(value)

    def remove_from_delete_list(self, value) -> None:
        """Acquire the lock and delete a record from the delete list."""
        with self._lock:
            if value in self._delete_list:
                self._delete_list.remove(value)

    def length(self) -> int:
        """Acquire the lock and return the number of items in the list."""
        with self._lock:
            return len(self._list) + len(self._delete_list)

    def flush(self) -> tuple:
        """Acquire the lock, create a copy of the existing batch,
        clear the existing batch, and return the copy."""
        with self._lock:
            c = self._list.copy()
            self._list.clear()
            d = list(self._delete_list)
            self._delete_list.clear()
            return c, d

    def update_last_executed_time(self, value) -> None:
        """Acquire the lock and update last executed time."""
        with self._lock:
            self.last_executed_time = value

    def set_is_completed(self, value) -> None:
        """Acquire the lock and set is completed flag."""
        with self._lock:
            self.is_completed = value


def emit_state(state):
    if state is not None:
        line = json.dumps(state)
        logger.debug('Emitting state {}'.format(line))
        sys.stdout.write("{}\n".format(line))
        sys.stdout.flush()


def try_upsert(collection: StandardCollection, record_batch: RecordBatch, force=False):
    if record_batch.length() > 0 and (record_batch.length() >= record_batch.max_batch_size or force):
        logger.info(f"*** Inside try_upsert if condition. ***")
        start_time = time.time()
        insert_end_time = None
        to_insert, to_delete = record_batch.flush()
        to_update = []

        if len(to_insert) > 0:
            records_array = remove_time_extracted(to_insert)
            for i, r in enumerate(collection.insert_many(records_array)):
                if type(r) is DocumentInsertError:
                    to_update.append(to_insert[i])
                else:
                    insert_end_time = time.time()
                    # Update ingested_documents and ingested_bytes metrics
                    ingested_documents.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                    ingested_bytes.labels(region_label, tenant_label, fabric_label, workflow_label).inc(len(json.dumps(r)))
                    # Update ingest_lag metric
                    diff = datetime.now(timezone.utc) - ensure_datetime(to_insert[i]["time_extracted"])
                    ingest_lag.labels(region_label, tenant_label, fabric_label, workflow_label).set(diff.total_seconds())

        if len(to_update) > 0:
            records_array = remove_time_extracted(to_update)
            for i, r in enumerate(collection.update_many(records_array)):
                if type(r) is DocumentInsertError:
                    # Increment ingest_errors metric
                    ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                    logger.warn(f'Failed to insert/update record: {to_update[i]}. {r}')
                else:
                    # Update ingest_lag metric
                    diff = datetime.now(timezone.utc) - ensure_datetime(to_update[i]["time_extracted"])
                    ingest_lag.labels(region_label, tenant_label, fabric_label, workflow_label).set(
                        diff.total_seconds())

        if len(to_delete) > 0:
            start_delete = time.time()
            try_delete(collection, to_delete)
            end_delete = time.time()
            if end_delete - start_delete > 10:
                logger.info(
                    f"*** Delete Took {end_delete - start_delete}seconds")
        end_time = time.time()
        if end_time - start_time > 1:
            logger.warn(
                f"Insert took {insert_end_time - start_time} *** "
                f"*** Batch Process Took {end_time - start_time}seconds to process: ***")
    record_batch.update_last_executed_time(datetime.now(timezone.utc))


def remove_time_extracted(records):
    return [{k: v for k, v in record.items() if k != 'time_extracted'} for record in records]


def try_delete(collection: StandardCollection, delete_list):
    try:
        collection.delete_many(delete_list)
    except Exception as e:
        # Increment ingest_errors metric
        ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
        logger.warn(f'Failed to delete records with keys: {delete_list}. {e}')


async def read_stdin() -> AsyncIterable[str]:
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    reader_protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: reader_protocol, sys.stdin)
    while not reader.at_eof():
        line = await reader.readline()
        if not line:
            break
        if line == b'' and reader.at_eof():
            logger.info("reached here 2...")
            break
        yield line.decode('utf-8').rstrip('\r\n')
    logger.info("reached here 3...")


async def persist_messages(collection: StandardCollection,
                           record_batch: RecordBatch, state):

    schemas = {}
    key_properties = {}
    validators = {}
    count = 0

    messages = read_stdin()
    async for message in messages:
        if not message:
            logger.info("reached here 1...")
        try:
            o = json.loads(message)
        except json.decoder.JSONDecodeError as e:
            # Increment ingest_errors metric
            ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
            logger.error(f"Unable to parse:\n{message}")
            raise e

        message_type = o['type']
        if message_type == 'RECORD':
            count += 1
            if count >= 30000:
                logger.info(f"*** Record {count} is {o['record']} ***")
            stream = o['stream']
            if stream not in schemas:
                # Increment ingest_errors metric
                ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                raise Exception(f"A record for stream {stream} was encountered before a corresponding schema")

            try:
                validators[stream].validate((o['record']))
            except jsonschema.ValidationError as e:
                # Increment ingest_errors metric
                ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                logger.error(f"Failed parsing the json schema for stream: {stream}.")
                continue

            try:
                rec = o['record']
                if 'time_extracted' in o:
                    rec["time_extracted"] = ensure_datetime(o["time_extracted"])
                else:
                    rec["time_extracted"] = ensure_datetime(record_batch.last_executed_time)
                try:
                    kps = key_properties.get(stream)
                    _key = None
                    # Appending _ to keys inorder for preserving values of reserved keys in source data
                    reserved_keys = ['_key', '_id', '_rev']

                    if kps:
                        if len(kps) > 1:
                            logger.warn(f'Multiple key_properties found ({",".join(kps)}).'
                                        f' Only `{kps[0]}` will be considered.')
                        _key = str(rec[kps[0]]).strip()
                        if kps[0] == '_key':
                            reserved_keys.remove('_key')

                    for reserved_key in reserved_keys:
                        if rec.get(reserved_key):
                            new_key = "_" + reserved_key
                            while True:
                                if rec.get(new_key):
                                    new_key = "_" + new_key
                                else:
                                    break
                            rec[new_key] = rec.pop(reserved_key)

                    if _key and not (
                            1 <= len(_key) <= 254 and bool(re.match("^[-_!\$%'\(\)\*\+,\.:;=@a-zA-Z0-9]+$", _key))):
                        hashed_key = hashlib.sha256(_key.encode('utf-8'))
                        _key = hashed_key.hexdigest()
                        logger.info(f"Primary key of the source doesn't satisfy the constraints of macrometa "
                                    f"document key, Hashing the key and using it in hex form to make it compliant.")
                    if _key:
                        rec['_key'] = _key
                except:
                    _key = None

                if '_sdc_deleted_at' in rec:
                    if rec['_sdc_deleted_at'] and rec.get('_key'):
                        record_batch.append(rec['_key'], delete=True)
                    else:
                        rec.pop('_sdc_deleted_at', None)
                        if rec.get('_key'):
                            record_batch.remove_from_delete_list(rec['_key'])

                record_batch.append(rec)
            except TypeError as e:
                # Increment ingest_errors metric
                ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
                # TODO: This is temporary until json serializing issue for Decimals are fixed in pyC8
                logger.debug("pyC8 error occurred")

            state = None
            try_upsert(collection, record_batch)
        elif message_type == 'STATE':
            logger.debug('Setting state to {}'.format(o['value']))
            state = o['value']
            emit_state(state)
        elif message_type == 'SCHEMA':
            stream = o['stream']
            schemas[stream] = o['schema']
            adjust_decimal_precision_for_schema(schemas[stream])
            validators[stream] = Draft4Validator((o['schema']))
            key_properties[stream] = o['key_properties']
        else:
            # Increment ingest_errors metric
            ingest_errors.labels(region_label, tenant_label, fabric_label, workflow_label).inc()
            logger.warning("Unknown message type {} in message {}".format(o['type'], o))

    logger.info("reached here 4...")
    scrape_complete_flag.labels(workflow_label).inc()
    record_batch.set_is_completed(True)
    logger.info("reached here 5...")


def ensure_datetime(time_extracted):
    if isinstance(time_extracted, str):
        time_extracted = datetime.strptime(time_extracted, "%Y-%m-%dT%H:%M:%S.%fZ")
        # Make the datetime object timezone-aware by setting it to UTC timezone
        time_extracted = time_extracted.replace(tzinfo=timezone.utc)
    elif time_extracted.tzinfo is None:
        # If the datetime object is timezone-naive, set it to UTC timezone
        time_extracted = time_extracted.replace(tzinfo=timezone.utc)
    return time_extracted


async def setup_batch_task(collection: StandardCollection,
                           record_batch: RecordBatch, state) -> None:
    event_loop = asyncio.get_event_loop()
    persist_messages_coro = persist_messages(collection, record_batch, state)
    asyncio.run_coroutine_threadsafe(persist_messages_coro, event_loop)
    process_batch_coro = process_batch(collection, record_batch)
    asyncio.run_coroutine_threadsafe(process_batch_coro, event_loop)

    # Wait for all Futures to complete and propagate any exceptions raised
    await asyncio.gather(
        persist_messages_coro,
        process_batch_coro,
    )


async def process_batch(collection: StandardCollection, record_batch: RecordBatch) -> None:
    count = 0
    # As soon as persist_messages is completed process_batch should also exit
    while not record_batch.is_completed:
        count += 1
        logger.info(f"***** Entered process batch..... is_completed: {record_batch.is_completed}")
        await asyncio.sleep(record_batch.interval)
        timedelta = datetime.now(timezone.utc) - ensure_datetime(record_batch.last_executed_time)
        if timedelta.total_seconds() >= record_batch.min_time_gap:
            # if batch has records that need to be processed but haven't reached batch size then process them.
            try_upsert(collection, record_batch, force=True)
        if count > 20:
            logger.warn("process batch exception raised..")
            raise Exception("process batch stopped.")


async def main_impl():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='Config file')
    args = parser.parse_args()
    if args.config:
        with open(args.config) as input_json:
            config = json.load(input_json)
    else:
        raise Exception("Required '--config' parameter was not provided")
    gdn_host = extract_gdn_host(config['gdn_host'])
    fabric = config['fabric']
    apikey = config['api_key']
    target_collection = config['target_collection']
    client = C8Client(
        protocol='https',
        host=gdn_host,
        port=443,
        apikey=apikey,
        geofabric=fabric
    )

    if not client.has_collection(target_collection):
        client.create_collection(name=target_collection)

    state = None
    collection = client.get_collection(target_collection)
    record_batch = RecordBatch(config)
    await setup_batch_task(collection, record_batch, state)

    # There can still be records in the `record_batch` which is not processed,
    # So, we have to force process it one last time before the workflow terminates.
    try_upsert(collection, record_batch, force=True)

    if is_metrics_enabled.lower() == 'true':
        # Wait for Prometheus to scrape the metrics
        while not is_scrape_complete(metric_service_url, f"{scrape_complete_flag._name}_total",
                                     f"workflow=\"{workflow_label}\""):
            logger.info("Waiting for metrics scrape...")
            time.sleep(15)
        logger.info("Metrics scrape complete. Exiting...")

    emit_state(state)
    logger.info("Completing normally...")


def is_scrape_complete(prometheus_url, metric_name, filter):
    response = requests.get(f"{prometheus_url}/query", params={"query": f"{metric_name}{{{filter}}}"})
    if response.status_code == 200:
        json_data = response.json()
        if json_data["data"]["result"] and len(json_data["data"]["result"]) > 0:
            return True
    return False


def main():
    """Main entry point"""
    try:
        asyncio.run(main_impl())
    except Exception as exc:
        logger.critical(exc)
        raise exc


if __name__ == '__main__':
    main()
