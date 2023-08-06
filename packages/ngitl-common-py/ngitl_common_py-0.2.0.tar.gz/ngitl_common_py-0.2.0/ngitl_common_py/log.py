# Copyright (C) 2023, NG:ITL
import logging
import datetime
import sys
from pathlib import Path
from typing import Optional


EMERGENCY_LOGGING_LOG_LEVEL = "DEBUG"

LOG_FORMAT = "%(asctime)s [%(levelname)s][%(module)s]: %(message)s"

log_filepath: Optional[Path] = None


def init_logging(component_name: str, log_file_directory: Path, logging_level: str):
    global log_filepath
    timestamp = datetime.datetime.now()
    timestamp_prefix = timestamp.strftime("%Y%m%d-%H%M%S")
    log_filepath = log_file_directory / f"{timestamp_prefix}_{component_name}.log"
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_filepath)
    logging.basicConfig(
        force=True,
        handlers=[stdout_handler, file_handler],
        level=logging_level,
        format=LOG_FORMAT,
    )
    logging.info("Logging initialized!")


def init_emergency_logging(component_name: str, log_file_directory: Path = Path.cwd()):
    global log_filepath
    log_filepath = log_file_directory / f"{component_name}_emergency.log"
    stdout_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(log_filepath)
    logging.basicConfig(
        force=True,
        handlers=[stdout_handler, file_handler],
        level=EMERGENCY_LOGGING_LOG_LEVEL,
        format=LOG_FORMAT,
    )
    logging.error("Emergency log initialized!")


def get_log_filepath() -> Path:
    global log_filepath
    return log_filepath


def flush():
    logger = logging.getLogger()
    for handler in logger.handlers:
        handler.flush()
