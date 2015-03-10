#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import unittest
import uuid
from . import config
from ..model import cs
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
        self.es_index = config.ES_INDEX
        pass

    def test_communication(self):
        """
        Testa comunicação com o cassandra
        """
        self.assertIsInstance(self.session, Session)

    def test_create_table(self):
        """
        Testa criação da tabela
        """
        cs.CS.create_table()

        # Verifica se tabela existe
        cql = "SELECT * from {}".format(self.es_index)
        result = self.session.execute(cql)
        self.assertListEqual(result, [])

        # Apaga tabela
        cs.CS.drop_table()

    def test_add_cassandra(self):
        """
        Testa adição de registro no Cassandra
        """
        cs.CS.create_table()

        # Rgistro 1
        id1 = uuid.uuid4()
        doc1 = cs.CS(
            content={'teste': 123},
            document_id=id1
        )
        doc1.add()
        result = doc1.get()
        self.assertIsNotNone(result)

        # Registro 2
        id2 = uuid.uuid4()
        doc2 = cs.CS(
            content={'teste': 1234},
            document_id=id2
        )
        doc2.add()
        result = doc2.get()
        self.assertIsNotNone(result)

        # Apaga tabela
        cs.CS.drop_table()

    def test_get_all(self):
        """
        Retorna todos os documentos inseridos
        """
        cs.CS.create_table()

        # Rgistro 1
        id1 = uuid.uuid4()
        doc1 = cs.CS(
            content={'teste': 123},
            document_id=id1
        )
        doc1.add()
        result = doc1.get()
        self.assertIsNotNone(result)

        # Registro 2
        id2 = uuid.uuid4()
        doc2 = cs.CS(
            content={'teste': 1234},
            document_id=id2
        )
        doc2.add()
        result = doc2.get()
        self.assertIsNotNone(result)

        # Testa documento que não existe
        id3 = uuid.uuid4()
        doc3 = cs.CS(
            content={'teste': 12345},
            document_id=id3
        )
        result = doc3.get()
        self.assertIsNone(result)

        # lista registros
        result = cs.CS.get_all()
        self.assertIs(type(result), list)
        self.assertGreater(len(result), 0)

        # Apaga tabela
        cs.CS.drop_table()

    def tearDown(self):
        """
        Remove test data
        """
        pass