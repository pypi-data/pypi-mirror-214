from logging import handlers
import logging
import os
import sys
import src.util.util as util
import colorlog
from pathlib import Path


class Logger:
    __instance = None  # for singleton

    def __init__(self, prop):
        if Logger.__instance is None:
            Logger.__instance = self
        self.prop = prop
        self.logger_name = self.prop['general']['job_name']
        self.log_dir = Path.joinpath(util.get_project_path(), "log")

    def init_logger(self):
        __logger = logging.getLogger(self.logger_name)
        if len(__logger.handlers) > 0:
            return __logger

        stream_formatter = colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)-8s]%(reset)s <%(name)s>: %(module)s:%(lineno)d:  %(bg_blue)s%(message)s"
        )
        file_formatter = logging.Formatter(
            # "%(asctime)s [%(levelname)-8s] <%(name)s>: %(pathname)s:%(module)s:%(lineno)d: %(message)s"
            "%(asctime)s [%(levelname)-8s] %(module)s:%(lineno)d: %(message)s"
        )
        stream_handler = colorlog.StreamHandler(sys.stdout)
        stream_handler.setFormatter(stream_formatter)

        file_handler = handlers.TimedRotatingFileHandler(
            os.path.abspath(Path.joinpath(self.log_dir, self.prop['log']['pipeline_file'])),
            when="midnight",
            interval=1,
            backupCount=self.prop['log']['backup_count'],
            encoding=self.prop['general']['encoding']
        )
        file_handler.setFormatter(file_formatter)

        sql_file_handler = handlers.TimedRotatingFileHandler(
            os.path.abspath(Path.joinpath(self.log_dir, self.prop['log']['sql_log_file'])),
            when="midnight",
            interval=1,
            backupCount=self.prop['log']['backup_count'],
            encoding=self.prop['general']['encoding']
        )
        sql_file_handler.setFormatter(file_formatter)

        sql_logger = logging.getLogger('sqlalchemy')
        sql_logger.addHandler(sql_file_handler)
        __logger.addHandler(stream_handler)
        __logger.addHandler(file_handler)
        __logger.setLevel(logging.DEBUG)
        return __logger
