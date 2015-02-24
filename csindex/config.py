#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import configparser
from cassandra.cluster import Cluster
from elasticsearch import Elasticsearch


def setup_config():
    """
    Setup configuration as global vars
    """
    global INI_FILE

    global PIDFILE_PATH
    global CASSANDRA_CLUSTER
    global ES
    global ES_INDEX
    global session

    INI_FILE = 'production.ini'

    config = configparser.ConfigParser()
    config.read(INI_FILE)

    # GEt pidfile from config
    PIDFILE_PATH = config.get('Daemon', 'pidfile_path')
    CASSANDRA_CLUSTER = Cluster(config.get('Daemon', 'cassandra_cluster'))
    ES = Elasticsearch(config.get('Daemon', 'es_url'))
    ES_INDEX = config.get('Daemon', 'es_index')
    session = CASSANDRA_CLUSTER.connect(ES_INDEX)