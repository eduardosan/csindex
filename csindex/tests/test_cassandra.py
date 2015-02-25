#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
from . import config
from cassandra.cluster import Session


class TestCassandra(unittest.TestCase):
    """
    Test interação com o banco de dados Cassandra
    """
    def setUp(self):
        """
        Load test data
        """
        self.session = config.session
        pass

    def test_communication(self):
        """
        Testa comunicação com o cassandra
        """
        self.assertIsInstance(self.session, Session)

    def tearDown(self):
        """
        Remove test data
        """
        pass