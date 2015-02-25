#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
import json
from . import document
from .. import config
from cassandra.query import dict_factory

log = logging.getLogger()


class CS(document.Document):
    """
    Classe que contém o Cassandra
    """
    def __init__(self, **args):
        """
        Método construtor

        :param args: parâmetros para colocar o documento
        :return:
        """
        super(CS, self).__init__(**args)
        self.session = config.session
        self.session.row_factory = dict_factory
        self.es_index = config.ES_INDEX

    @staticmethod
    def get_all():
        """
        Get all documents from Cassandra

        :return: Dict with all documents
        """
        cql = "SELECT id_doc as document_id, content, WRITETIME (content) as document_date FROM {}".format(config.ES_INDEX)
        config.session.row_factory = dict_factory
        result = config.session.execute(cql)

        return result

    @staticmethod
    def create_table():
        """
        Cria tabela para armazenar os documentos no Cassandra

        :return: Resultado do Cassandra
        """
        cql = "CREATE TABLE {} (id_doc text, content text, PRIMARY KEY (id_doc))".format(config.ES_INDEX)
        result = config.session.execute(cql)

        return result

    @staticmethod
    def drop_table():
        """
        Remove tabela

        :return: Resultado do Cassandra
        """
        cql = "DROP TABLE {}".format(config.ES_INDEX)
        result = config.session.execute(cql)

        return result

    def get(self):
        """
        Get document on Cassandra
        :return: dict with document data
        """
        cql = "SELECT content FROM {} WHERE id_doc = '{}' LIMIT 1".format(self.es_index, self.document_id)
        res = self.session.execute(cql)

        if res is not None and len(res) > 0:
            result = res[0]
            cql = "SELECT WRITETIME (content) as document_date FROM {} WHERE id_doc = '{}' LIMIT 1".format(
                self.es_index,
                self.document_id
            )
            # Add document date as timestamp
            seconds_result = self.session.execute(cql)
            doc_seconds = seconds_result[0]['document_date']
            #print(doc_seconds)
            result['document_date'] = time.gmtime(doc_seconds)
            self.document_date = time.gmtime(doc_seconds)
        else:
            result = None

        return result

    def add(self):
        """
        Add document on Cassandra

        :return: Insertion result
        """
        # Store content as text
        content = json.dumps(self.content)
        #print(content)

        cql = """
            INSERT INTO {} (id_doc, content)
            VALUES ('{}', '{}')
            """.format(self.es_index, self.document_id, content)

        print(cql)
        result = self.session.execute(cql)

        return result

    def update(self):
        """
        Update document on Cassandra

        :return:
        """
        cql = """
            UPDATE {}
            SET content = {}
            WHERE  id_doc= '{}'
            """.format(self.es_index, self.content, self.document_id)

        result = self.session.execute(cql)

        return result