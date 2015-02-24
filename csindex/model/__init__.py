__author__ = 'eduardo'

from cassandra.cluster import Cluster
from .. import config

cluster = Cluster(config.CASSANDRA_CLUSTER)