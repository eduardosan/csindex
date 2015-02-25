#!/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import os
import os.path
import logging
from .. import config

config.setup_config()

# Set to test environment
config.INI_FILE = 'test.ini'

test_dir = os.path.dirname(os.path.realpath(__file__))
log = logging.getLogger()


def setup_package():
    """
    Setup test data for the package
    """
    pass


def teardown_package():
    """
    Remove test data
    """
    pass