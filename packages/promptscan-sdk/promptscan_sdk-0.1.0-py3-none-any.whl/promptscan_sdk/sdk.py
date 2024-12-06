from __future__ import annotations

import logging
import os
from dataclasses import dataclass
from itertools import groupby
from queue import Queue, Empty
from threading import Timer, Lock
from typing import List

from .client import GraphQLClient, GenerationInput, KeyValuePairInput

__all__ = ["PromptScanSDK", "configure", "collect", "client", "close"]


@dataclass
class GenerationRecord:
    generation: GenerationInput
    api_key: str = None
    retries: int = 0


class CollectorManager:
    def __init__(self, sdk: PromptScanSDK):
        self.lock = Lock()
        self.sdk = sdk
        self.timer = None

    def schedule(self):
        with self.lock:
            if not self.timer and not self.sdk.is_closed:
                try:
                    self.timer = Timer(self.sdk.flush_interval_millis / 1000, self.flush)
                    self.timer.start()
                except RuntimeError:
                    self.timer = None

    def flush(self):
        self.cancel()
        self.sdk.flush()
        self.schedule()

    def cancel(self):
        with self.lock:
            if self.timer:
                self.timer.cancel()
                self.timer = None


class PromptScanSDK:
    def __init__(
            self,
            api_key: str = None,
            base_url: str = None,
            enabled: bool = True,
            debug: bool = False,
            auto_flush: bool = True,
            flush_interval_millis: int = 5000,
            max_retries: int = 3,
            default_tags: dict = None
    ):
        self.enabled = enabled if enabled is not None else True
        self.debug = debug if debug is not None else False
        self.auto_flush = auto_flush if auto_flush is not None else True
        self.flush_interval_millis = flush_interval_millis if isinstance(flush_interval_millis, int) else 5000
        self.max_retries = max_retries if isinstance(max_retries, int) else 3
        self.default_tags = default_tags if isinstance(default_tags, dict) else {}

        self._logger = logging.getLogger("promptscan_sdk")
        self._queue = Queue()
        self._collector_manager: CollectorManager = None
        self.is_closed = False

        api_key = api_key or os.getenv("PROMPTSCAN_API_KEY", None)
        base_url = base_url or os.getenv("PROMPTSCAN_BASE_URL", "https://api.promptscan.com/graphql/")

        if not api_key:
            raise ValueError("API key is required.")

        self.client = GraphQLClient(
            base_url,
            headers={"Authorization": f"Bearer {api_key}"} if api_key else None)

        self._setup_auto_flush()

    def _setup_auto_flush(self):
        self._reset_auto_flush()

        if not self.auto_flush or not self.flush_interval_millis:
            return

        self._collector_manager = CollectorManager(self)
        self._collector_manager.schedule()

    def _reset_auto_flush(self):
        if self._collector_manager:
            self._collector_manager.cancel()

    def queued_generations_count(self):
        return self._queue.qsize()

    def collect(self, generation: GenerationInput, api_key: str = None):
        if self.debug:
            self._logger.debug(f"Adding generation record {generation.id} to queue.")
        self._queue.put_nowait(GenerationRecord(generation, api_key))

    def flush(self) -> List[GenerationInput]:
        if self._queue.empty():
            return []

        records = []
        flushed_generations = []

        try:
            while True:
                record = self._queue.get_nowait()
                records.append(record)
        except Empty:
            pass

        if not self.enabled:
            if self.debug:
                self._logger.debug(f"SDK is disabled. Discarding {len(records)} collected generations.")
            return [r.generation for r in records]

        if self.debug:
            self._logger.debug(f"Flushing {len(records)} collected generations.")

        def append_default_tags(rec: GenerationRecord) -> GenerationRecord:
            tags = {**self.default_tags, **{t.key: t.value for t in (rec.generation.tags or [])}}
            rec.generation.tags = [KeyValuePairInput(key=k, value=v) for k, v in tags.items()]
            return rec

        records = filter(lambda r: r.retries < self.max_retries, records)
        records = map(append_default_tags, records)
        records = sorted(records, key=lambda r: r.api_key or "")
        records = groupby(records, key=lambda r: r.api_key)

        for api_key, record_group in records:
            record_group = list(record_group)
            try:
                if api_key:
                    kwargs = {"headers": {"Authorization": f"Bearer {api_key}"}}
                else:
                    kwargs = {}
                res = self.client.collect_generations([r.generation for r in record_group], **kwargs)
                if retry := not res.collect.success:
                    self._logger.error(f"Failed to collect generations: {res.collect.error.message}")
            except Exception as e:
                if self.debug:
                    self._logger.error(f"Failed to collect generations.", exc_info=True)
                retry = True

            if retry:
                for record in record_group:
                    record.retries += 1
                    self._queue.put_nowait(record)
                if self.debug:
                    self._logger.debug(f"Adding {len(record_group)} records back to queue for retry.")
            else:
                flushed_generations.extend([r.generation for r in record_group])

        return flushed_generations

    def close(self):
        if self.is_closed:
            self._logger.warning("PromptScanSDK is already closed.")
            return

        self.is_closed = True

        if self.debug:
            self._logger.debug("Closing PromptScanSDK...")

        self._reset_auto_flush()
        self.flush()

        if self.debug:
            self._logger.debug("PromptScanSDK is closed.")


def configure(
        api_key: str = None,
        base_url: str = None,
        enabled: bool = True,
        debug: bool = False,
        auto_flush: bool = True,
        flush_interval_millis: int = 5000,
        max_retries: int = 3,
        default_tags: dict = None
):
    global _sdk
    _sdk = PromptScanSDK(
        api_key=api_key,
        base_url=base_url,
        enabled=enabled,
        debug=debug,
        auto_flush=auto_flush,
        flush_interval_millis=flush_interval_millis,
        max_retries=max_retries,
        default_tags=default_tags)


def close():
    global _sdk
    assert _sdk, "PromptScanSDK is not configured."
    _sdk.close()
    _sdk = None


def collect(generation: GenerationInput, api_key: str = None):
    assert _sdk, "PromptScanSDK is not configured."
    _sdk.collect(generation, api_key)


def client():
    assert _sdk, "PromptScanSDK is not configured."
    return _sdk.client


_sdk: PromptScanSDK | None = None
