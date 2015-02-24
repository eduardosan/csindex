#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
from .daemon import Daemon
from . import config
from cassandra.query import dict_factory

log = logging.getLogger()


class Sync(Daemon):
    """
    Classe responsável pela sincronia dos documentos
    """
    def __init__(self):
        """
        Método construtor
        """
        Daemon.__init__(self)
        self.es_index = config.ES_INDEX
        self.es = config.ES
        self.session = config.session
        self.session.row_factory = dict_factory

    def process_es(self):
        """
        Procedimento que processa os documentos do Elastic Search para
        sincronizar com o Cassandra.

        Regra: o mais atual sempre ganha
        :return:
        """
        response = self.es.search(index=self.es_index, body={"query": {"match_all": {}}})
        hits = response.get('hits')
        if hits is not None:
            for res in hits['hits']:
                # Now try to find document in Cassandra
                cassandra_doc = self.get_cassandra(int(res['_id']))
                if cassandra_doc is None:
                    # Add document in Cassandra
                    log.info("Documento %s não encontrado no Cassandra. Adicionando...", res['_id'])
                    self.add_cassandra(res['_source'])
                else:
                    # Check which is newer
                    if cassandra_doc['document_date'] > res['_source']['document_date']:
                        log.info("Documento do Cassandra mais atual. Adicionando %s no ES", res['_id'])
                        self.update_es(res)
                    else:
                        log.info("Documento do ES mais atual ou data igual. Atualiza %s no cassandra", res['_id'])
                        self.update_cassandra(res)

        return True

    def get_cassandra(self, id_doc):
        """
        Get document on Cassandra

        :param id_doc: Document ID
        :return: dict with document data
        """
        result = self.session.execute("SELECT content FROM %s WHERE id_doc = %d LIMIT 1", (self.es_index, id_doc))

        # Add document date as timestamp
        doc_seconds = self.session.execute("SELECT WRITETIME (content) FROM %s WHERE id_doc = %d LIMIT 1", (self.es_index, id_doc))
        result['document_date'] = time.gmtime(doc_seconds)

        return result

    def add_es(self, doc):
        """
        Add document on ES

        :param doc: Document JSON
        :return: Result
        """
        result = self.es.create(
            index=self.es,
            doc_type='document',
            body=doc
        )

        return result

    def add_cassandra(self, document):
        """
        Add document on Cassandra

        :param document: Document to be inserted
        :return: Insertion result
        """

        result = self.session.execute(
            """
            INSERT INTO %s (id_doc, content)
            VALUES (%d, %s)
            """,
            (self.es_index, document['_id'], document['_source'])
        )

        return result

    def update_cassandra(self, document):
        """
        Update document on Cassandra

        :param document: Document content
        :return:
        """
        result = self.session.execute(
            """
            UPDATE %s
            SET content = %s
            WHERE  id_doc= %d
            """,
            (self.es_index, document['_source'], document['_id'])
        )

        return result

    def update_es(self, document):
        """
        Update document on ES

        :param document: Document JSON
        :return: Results
        """
        result = self.es.update(
            index=self.es_index,
            doc_type='document',
            body=document
        )

        return result