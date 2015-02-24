#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import configparser

def setup_config():
    """
    Setup configuration as global vars
    """
    global INI_FILE

    global PIDFILE_PATH
    global CASSANDRA_CLUSTER

    INI_FILE = 'production.ini'

    config = configparser.ConfigParser()
    config.read(INI_FILE)

    # GEt pidfile from config
    PIDFILE_PATH = config.get('Daemon', 'pidfile_path')
    CASSANDRA_CLUSTER = config.get('Daemon', 'cassandra_cluster')