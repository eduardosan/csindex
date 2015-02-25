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
    global TIMER

    INI_FILE = 'production.ini'

    config = configparser.ConfigParser()
    config.read(INI_FILE)

    # Daemon configuration
    PIDFILE_PATH = config.get('Daemon', 'pidfile_path')
    TIMER = int(config.get('Daemon', 'timer'))

    # Cassandra
    servers = config.get('Daemon', 'cassandra_cluster')
    if servers is not None:
        CASSANDRA_CLUSTER = Cluster(servers.split(','))
    else:
        CASSANDRA_CLUSTER = Cluster()

    # Elastic Search
    ES = Elasticsearch(config.get('Daemon', 'es_url'))
    ES_INDEX = config.get('Daemon', 'es_index')

    # Cassandra session
    session = CASSANDRA_CLUSTER.connect(ES_INDEX)