#!/usr/bin/python
# coding:utf-8
# Copyright (C) 2005-2019 All rights reserved.
# FILENAME:  logger.py
# VERSION: 	 1.0
# CREATED: 	 2019-05-21 10:21
# AUTHOR: 	 Aekasitt Guruvanich <aekazitt@gmail.com>
# DESCRIPTION:
#
# HISTORY:
#*************************************************************
"""Module defining class Logger"""
import sys
import threading
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
# pylint: disable=E0401, E0611, E1101
import importlib
importlib.reload(sys)

# Define Color Escape Codes for Logging
CYAN='\033[1;36m'     # Light Cyan ANSI Escape Code
NC='\033[0m'          # No Colour ANSI Escape Code

class Logger(object):
    """Class used Log to sys.stdout"""
    instance = None
    mutex = threading.Lock()
    def __init__(self, log_name):
        self.logger = logging.getLogger(log_name)
        handler = StreamHandler(sys.stdout)
        fileHandler = TimedRotatingFileHandler(
                filename='logs/{}.log'.format(log_name),
                when='D', interval=1, backupCount=10)
        fmt = logging.Formatter(f'{CYAN}[%(levelname)s]{NC} %(message)s')
        handler.setFormatter(fmt)
        self.logger.addHandler(handler)
        self.logger.addHandler(fileHandler)
        self.logger.setLevel(logging.INFO)

    def shutdown(self):
        """Release all of Logger instance handler and then release Logger."""
        try:
            for handler in list(self.logger.handlers):
                self.logger.removeHandler(handler)
                del handler
            if self.logger is not None:
                del self.logger
        except AttributeError:
            pass

    @staticmethod
    def get_instance(log_name):
        """Get Singleton instance of Logger"""
        if Logger.instance is None:
            Logger.mutex.acquire()
            if Logger.instance is None:
                Logger.instance = Logger(log_name)
            Logger.mutex.release()
        return Logger.instance.logger

    @staticmethod
    def release_instance():
        """Release Singleton instance of Logger"""
        if Logger.instance is not None:
            Logger.instance.shutdown()
        Logger.instance = None
