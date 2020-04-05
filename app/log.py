#!/usr/bin/env python3

import os
import sys
import logging
from logging import StreamHandler


def setup_logging():
    logger_instance = logging.getLogger('autoscaling')
    logger_instance.addHandler(StreamHandler(sys.stdout))
    level = os.environ['LOGGING_LEVEL'] if os.environ.get('LOGGING_LEVEL') else 'ERROR'
    logger_instance.setLevel(level)
    return logger_instance

logger = setup_logging()
