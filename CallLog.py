from logging.handlers import TimedRotatingFileHandler
from rich.logging import RichHandler
from datetime import datetime 
from typing import Union
import logging 
import pytz


class CallLog:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    _STREAM_HANDLER_FORMAT = "[%(asctime)s]\t[%(filename)s:%(lineno)s] >> %(message)s"
    _FILE_HANDLER_FORMAT = "[%(asctime)s] / %(levelname)s / %(filename)s / line:%(lineno)s\t>> %(message)s"
    _TIME_FORMAT = "%y%m%d_%Hh%Mm"
    _str_Level = {
        'c': logging.CRITICAL,
        'f': logging.FATAL,
        'e': logging.ERROR,
        'w': logging.WARNING,
        'i': logging.INFO,
        'd': logging.DEBUG,
        'n': logging.NOTSET,
        }
    _int_Level = {
        CRITICAL : logging.CRITICAL,
        FATAL : logging.FATAL,
        ERROR : logging.ERROR,
        WARNING : logging.WARNING,
        INFO : logging.INFO,
        DEBUG : logging.DEBUG,
        NOTSET : logging.NOTSET,
    }

    def __init__(self, log_name,  log_level : Union[str, int], log_extension=".log",) -> None:
        self._logger = logging.getLogger(log_name)
        self._log_extension = self._extension_check(log_extension)
        self._file_handler = None 
        self._stream_handler = None 
        self._root_logger_log_level = self._call_level( log_level )
        self._logger.setLevel(self._root_logger_log_level)

    def __del__(self):
        for handler in self._logger.handlers:
            if handler.name == "file_handler":
                self._logger.removeHandler(handler)
                handler.close()
    @staticmethod
    def _extension_check(extension):
        if extension[0] == ".":
            return extension
        else:
            return "."+extension
    @staticmethod
    def _call_level(level:Union[int, str]):
        if isinstance(level, str):
            level = CallLog._str_Level[level[0].lower()]
        elif isinstance(level, int):
            level = CallLog._int_Level[level]
        else: 
            raise ValueError("level must be int or string.")
        return level 

    def add_file_handler(self, path:str, H_type=None, when="midnight", interval=1, log_level:Union[str,int]=None, name="file_handler") -> None:
        if H_type == "rotating" or H_type == "R":
            handler = TimedRotatingFileHandler(filename=f'{path}_{str(datetime.now().strftime(CallLog._TIME_FORMAT))}{self._log_extension}', encoding='utf-8', when=when, interval=interval)
        else: 
            handler = logging.FileHandler(filename=f'{path}_{str(datetime.now().strftime(CallLog._TIME_FORMAT))}{self._log_extension}',mode='a', encoding='utf-8')
        if log_level != None :
            log_level = self._call_level(log_level)
            assert self._root_logger_log_level <= log_level, "Handler level is low than root log level"
            handler.setLevel(log_level)
        handler.setFormatter(CallLog.TimeFormatter(CallLog._FILE_HANDLER_FORMAT))
        handler.name = name
        self._logger.addHandler(handler)
        self._file_handler = handler
        return 

    def add_stream_handler(self, H_type:str="rich", log_level:Union[str,int]=None, name="stream_handler") -> None :
        if H_type == "rich":
            handler = RichHandler(rich_tracebacks=True)
        elif H_type == "stream":
            handler = logging.StreamHandler()
        if log_level != None:
            log_level = self._call_level(log_level)
            assert self._root_logger_log_level <= log_level, "Handler level is low than root log level"
            handler.setLevel(log_level)
        handler.name = name
        handler.setFormatter(logging.Formatter(CallLog._STREAM_HANDLER_FORMAT))
        self._logger.addHandler(handler)
        self._stream_handler = handler
        return

    def debug(self, msg, *args, **kwargs):
        self._logger.debug(msg, *args, **kwargs)
    def info(self, msg, *args, **kwargs):
        self._logger.info(msg, *args, **kwargs)
    def warning(self,msg, *args, **kwargs):
        self._logger.warning(msg, *args, **kwargs)
    def error(self,msg, *args, **kwargs):
        self._logger.error(msg, *args, **kwargs)
    def exception(self,msg, *args, **kwargs):
        self._logger.exception(msg, *args, **kwargs)
    def critical(self,msg, *args, **kwargs):
        self._logger.critical(msg, *args, **kwargs)
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        self._logger.error(
            "Unexpected exception",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    class TimeFormatter(logging.Formatter):
        """logging.Formatter에 타임존 내부 설정"""
        timezone = 'Asia/Seoul'

        def converter(self, timestamp):
            dt = datetime.fromtimestamp(timestamp, tz=pytz.UTC)
            return dt.astimezone(pytz.timezone(self.timezone))

        def formatTime(self, record, datefmt=None):
            dt = self.converter(record.created)
            if datefmt:
                s = dt.strftime(datefmt)
            else:
                try:
                    s = dt.isoformat(timespec='seconds')
                except TypeError:
                    s = dt.isoformat()
            return s
