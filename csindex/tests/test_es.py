#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import uuid
import datetime
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

    def test_add_es(self):
        """
        Test inserção de documento no Elastic Search
        """
        result = es.ES.create_table()
        self.assertIsNotNone(result)

        # Rgistro 1
        id1 = uuid.uuid4()
        doc1 = es.ES(
            content={'teste': 123},
            document_id=id1
        )
        doc1.add()
        result = doc1.get()
        self.assertIsNotNone(result)

        # Registro 2
        id2 = uuid.uuid4()
        doc2 = es.ES(
            content={'teste': 1234},
            document_id=id2
        )
        doc2.add()
        result = doc2.get()
        self.assertIsNotNone(result)

        result = es.ES.drop_table()
        self.assertIsNotNone(result)

    def test_get_all(self):
        """
        Retorna todos os documentos inseridos
        """
        result = es.ES.create_table()
        self.assertIsNotNone(result)

        # Rgistro 1
        id1 = uuid.uuid4()
        doc1 = es.ES(
            content={'teste': 123},
            document_id=id1
        )
        doc1.add()
        result = doc1.get()
        self.assertIsNotNone(result)

        # Registro 2
        id2 = uuid.uuid4()
        doc2 = es.ES(
            content={'teste': 1234},
            document_id=id2
        )
        doc2.add()
        result = doc2.get()
        self.assertIsNotNone(result)

        # Testa recuperar documento que não existe
        id3 = uuid.uuid4()
        doc3 = es.ES(
            content={'teste': 12345},
            document_id=id3
        )
        result = doc3.get()
        self.assertIsNone(result)

        result = es.ES.get_all()
        self.assertGreater(result['hits']['total'], 0)

        result = es.ES.drop_table()
        self.assertIsNotNone(result)

    def tearDown(self):
        """
        Apaga dados
        """
        pass
