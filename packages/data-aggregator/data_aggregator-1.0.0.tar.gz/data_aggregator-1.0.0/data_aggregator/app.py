# Copyright (C) 2022, NG:ITL
import argparse
import logging
import abc
import sys
import traceback

from abc import ABCMeta
from pathlib import Path
from PySide6.QtCore import QObject, Slot
from typing import Optional, Tuple

from data_aggregator.processing.processor.base_processor import BaseProcessor
from data_aggregator.processing.reader.base_reader import BaseReader
from data_aggregator.processing.writer.cached_writer import CachedWriter
from data_aggregator.gui.gui import Gui
from data_aggregator.processing.aggregator import DataAggregator

from ngitl_common_py.log import init_logging, init_emergency_logging
from ngitl_common_py.config import (
    get_config,
    get_config_param,
    find_config_file,
    read_config,
    write_config_to_file,
    ConfigEntryError,
    SEARCH_PATHS,
)


class DataAggregatorAppMeta(type(QObject), ABCMeta):  # type: ignore
    pass


class DataAggregatorApp(QObject, metaclass=DataAggregatorAppMeta):
    def __init__(self, parent: Optional[QObject] = None):
        QObject.__init__(self, parent)

        self.config_filepath = self.setup_config()
        self.setup_logging()

        self.gui = self.setup_gui()
        self.input_reader, self.processor, self.output_writer = self.setup_components()
        self.data_aggregator: Optional[DataAggregator] = self.setup_aggregator()

    @abc.abstractmethod
    def setup_components(self) -> Tuple[BaseReader, BaseProcessor, CachedWriter]:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_config(self, config: dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get_version(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def get_name(self) -> str:
        raise NotImplementedError

    def setup_config(self) -> Path:
        name = self.get_name()
        config_filepath = find_config_file(f"{name}_config.json")
        if config_filepath is None:
            init_emergency_logging(name)
            logging.error("Unable to find config file in search paths: %s", SEARCH_PATHS)
            sys.exit(-1)
        read_config(config_filepath)
        try:
            config = get_config()
            self.validate_config(config)
        except ConfigEntryError as e:
            init_emergency_logging(name)
            logging.error(e)
            sys.exit(-1)
        return config_filepath

    def setup_logging(self) -> None:
        log_file_directory = Path(get_config_param("log_file_directory"))
        logging_level = get_config_param("logging_level")
        init_logging("data_aggregator", log_file_directory, logging_level)
        logging.info("Config search paths: %s", SEARCH_PATHS)
        logging.info("Using config file: %s", self.config_filepath)

    def setup_gui(self) -> Gui:
        gui = Gui()
        gui.request_reinit_signal.connect(self.handle_reinit_signal)
        return gui

    def setup_aggregator(self) -> DataAggregator:
        data_aggregator = DataAggregator(self.input_reader, self.processor, self.output_writer)

        data_aggregator.show_message_signal.connect(self.gui.handle_show_message_signal)
        data_aggregator.processing_results_signal.connect(self.gui.handle_processing_results)
        self.gui.request_cache_flush_signal.connect(data_aggregator.handle_cache_flush_request)
        self.gui.request_write_config_to_file_signal.connect(self.handle_request_write_config_to_file_signal)

        data_aggregator.start_initial_file_check()
        data_aggregator.start_filesystem_watcher()
        return data_aggregator

    def stop_processor(self) -> None:
        if self.data_aggregator:
            self.data_aggregator.stop()
            self.data_aggregator = None

    @Slot()
    def handle_reinit_signal(self) -> None:
        logging.info("Reinit signal triggered")
        self.stop_processor()
        self.data_aggregator = self.setup_aggregator()

    @Slot()
    def handle_request_write_config_to_file_signal(self) -> None:
        logging.info("Writing config to file")
        write_config_to_file(self.config_filepath)

    def run(self) -> None:
        try:
            parser = argparse.ArgumentParser(prog="data_aggregator", description="Smart data processing")
            parser.add_argument("--version", action="store_true")
            args = parser.parse_args()

            if args.version:
                print(self.get_version())
                sys.exit(0)

            self.gui.run()

        except Exception as e:
            logging.error(traceback.format_exc())
            raise e
