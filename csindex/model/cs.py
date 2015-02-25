#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
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
        config.session.row_factory = dict_factory
        result = config.session.execute(
            "SELECT id_doc as document_id, content, WRITETIME (content) as document_date FROM %s",
            config.ES_INDEX
        )

        return result

    def get(self):
        """
        Get document on Cassandra
        :return: dict with document data
        """
        result = self.session.execute(
            "SELECT content FROM %s WHERE id_doc = %d LIMIT 1",
            (self.es_index, self.document_id)
        )

        if result is not None:
            # Add document date as timestamp
            doc_seconds = self.session.execute(
                "SELECT WRITETIME (content) FROM %s WHERE id_doc = %d LIMIT 1",
                (self.es_index, self.document_id)
            )
            result['document_date'] = time.gmtime(doc_seconds)
            self.document_date = time.gmtime(doc_seconds)

        return result

    def add(self):
        """
        Add document on Cassandra

        :return: Insertion result
        """

        result = self.session.execute(
            """
            INSERT INTO %s (id_doc, content)
            VALUES (%d, %s)
            """,
            (self.es_index, self.document_id, self.content)
        )

        return result

    def update(self):
        """
        Update document on Cassandra

        :return:
        """
        result = self.session.execute(
            """
            UPDATE %s
            SET content = %s
            WHERE  id_doc= %d
            """,
            (self.es_index, self.content, self.document_id)
        )

        return result