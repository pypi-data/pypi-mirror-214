import logging
from typing import Optional
from typeguard import typechecked
from contextlib import contextmanager
from multiprocessing import Queue

from kestrel.exceptions import DataSourceManagerInternalError
from kestrel_datasource_stixshifter.worker.transmitter import TransmitterPool
from kestrel_datasource_stixshifter.worker.translator import Translator


_logger = logging.getLogger(__name__)


@contextmanager
@typechecked
def transmit(
    connector_name: str,
    connection_dict: dict,
    configuration_dict: dict,
    retrieval_batch_size: int,
    translators_count: int,
    queries: list,
    raw_records_queue: Queue,
):
    _logger.debug(f"{translators_count} translation workers to be started")
    transmitter_pool = TransmitterPool(
        connector_name,
        connection_dict,
        configuration_dict,
        retrieval_batch_size,
        translators_count,
        queries,
        raw_records_queue,
    )

    try:
        transmitter_pool.start()
        yield transmitter_pool
    finally:
        transmitter_pool.join(2)
        if transmitter_pool.is_alive():
            raise DataSourceManagerInternalError(
                f"transmitter pool process do not terminate in interface {__package__}"
            )


@contextmanager
@typechecked
def translate(
    connector_name: str,
    observation_metadata: dict,
    translation_options: dict,
    cache_data_path_prefix: Optional[str],
    is_fast_translation: bool,
    raw_records_queue: Queue,
    translated_data_queue: Queue,
    translators_count: int,
):
    _logger.debug(f"fast translation enabled: {is_fast_translation}")
    translators = [
        Translator(
            connector_name,
            observation_metadata,
            translation_options,
            cache_data_path_prefix,
            is_fast_translation,
            raw_records_queue,
            translated_data_queue,
        )
        for _ in range(translators_count)
    ]

    try:
        for translator in translators:
            translator.start()
        yield translators
    finally:
        for translator in translators:
            translator.join(1)
            if translator.is_alive():
                raise DataSourceManagerInternalError(
                    f"one or more translators do not terminate in interface {__package__}"
                )
