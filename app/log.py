#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    @project: k8scontroller-sqs-autoscaler
    @component: core
    @copyright: © 2020 by vfabi
    @author: vfabi
    @support: vfabi
    @initial date:
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE', which is part of this source code package
    @description:
    @todo:
"""

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
