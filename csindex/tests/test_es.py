#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import uuid
from elasticsearch import Elasticsearch
from . import config
from ..model import es


class TestES(unittest.TestCase):
    """
    Testa operações com o Elastic Search
    """
    def setUp(self):
        """
        Carrega dados iniciais
        """
        self.es = config.ES
        self.es_index = config.ES_INDEX
        pass

    def test_communication(self):
        """
        Testa comunicação com o Elastic Search
        """
        self.assertIsInstance(self.es, Elasticsearch)
        teste = self.es.info()
        self.assertIsNotNone(teste)

    def test_create_table(self):
        """
        Testa criação e remoção dos índices
        """
        result = es.ES.create_table()
        self.assertIsNotNone(result)

        result = es.ES.drop_table()
        self.assertIsNotNone(result)

    def tearDown(self):
        """
        Apaga dados
        """
        pass
