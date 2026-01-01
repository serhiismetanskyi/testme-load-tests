"""Test execution logger."""

import datetime
import enum
import json
import logging
import threading
from pathlib import Path

from requests import Response


class LogType(enum.Enum):
    """Log levels."""

    INFO = 1
    DEBUG = 2
    ERROR = 3
    CRITICAL = 4


class Logger:
    """Runtime messages and HTTP request/response logger."""

    log_obj = None
    file_handler = None
    _file_lock = threading.Lock()

    _dir_path = Path(__file__).parent.parent
    _logs_dir = Path(_dir_path, "logs")
    _request_log_file = Path(_logs_dir, f"log_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

    @classmethod
    def _ensure_logs_dir(cls):
        """Create logs directory."""
        cls._logs_dir.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _write_log_to_file(cls, data: str):
        """Write to request/response log file (thread-safe)."""
        cls._ensure_logs_dir()
        with cls._file_lock, open(cls._request_log_file, "a", encoding="utf-8") as log_file:
            log_file.write(data)

    @staticmethod
    def init_logger(name, log_file):
        """Init logger with file output."""
        Logger.log_obj = logging.getLogger(name)
        Logger.log_obj.setLevel(logging.DEBUG)
        Logger.log_obj.handlers.clear()

        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        Logger.file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
        Logger.file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        Logger.file_handler.setFormatter(formatter)
        Logger.log_obj.addHandler(Logger.file_handler)

    @staticmethod
    def log_message(message, log_type=LogType.INFO):
        """Log message with specified log level."""
        if not Logger.log_obj:
            return

        if log_type == LogType.INFO:
            Logger.log_obj.info(message)
        elif log_type == LogType.DEBUG:
            Logger.log_obj.debug(message)
        elif log_type == LogType.ERROR:
            Logger.log_obj.error(message)
        else:
            Logger.log_obj.critical(message)

    @classmethod
    def add_request(cls, task_name: str, url: str, method: str, body=None):
        """Log request details."""
        data_to_add = "\n-----\n"
        data_to_add += f"Task: {task_name}\n"
        data_to_add += f"Time: {datetime.datetime.now()}\n"
        data_to_add += f"Request method: {method}\n"
        data_to_add += f"Request URL: {url}\n"
        if body is not None:
            if isinstance(body, dict):
                data_to_add += f"Request Body: {json.dumps(body, indent=2)}\n"
            else:
                data_to_add += f"Request Body: {body}\n"
        data_to_add += "\n"

        cls._write_log_to_file(data_to_add)

    @classmethod
    def add_response(cls, result: Response, task_result: str = None):
        """Log response details."""
        try:
            cookies_as_dict = dict(result.cookies) if result.cookies else {}
        except (TypeError, AttributeError):
            cookies_as_dict = {}

        try:
            headers_as_dict = dict(result.headers) if result.headers else {}
        except (TypeError, AttributeError):
            headers_as_dict = {}

        data_to_add = f"Task result: {task_result}\n"
        data_to_add += f"Response code: {result.status_code}\n"
        data_to_add += f"Response text: {result.text}\n"
        data_to_add += f"Response headers: {headers_as_dict}\n"
        data_to_add += f"Response cookies: {cookies_as_dict}\n"
        data_to_add += "\n-----\n"

        cls._write_log_to_file(data_to_add)
