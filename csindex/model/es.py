#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import logging
import uuid
import datetime
import time
from elasticsearch.client import IndicesClient
from . import document
from .. import config

log = logging.getLogger()


class ES(document.Document):
    """
    Documento no Elastic Search
    """
    def __init__(self, **args):
        """
        Método construtor da documento no Elastic Search

        :param args: parâmetros do Elastic Search
        """
        super(ES, self).__init__(**args)

        self.es_index = config.ES_INDEX
        self.es = config.ES

    @property
    def document_id(self):
        """
        ID do document
        """
        return self._document_id

    @document_id.setter
    def document_id(self, value):
        """
        Convert uuid to str
        :param value: Received value
        """
        if type(value) == type(uuid.uuid4()):
            value = str(value)

        self._document_id = value

    @property
    def document_date(self):
        """
        Data do documento
        """
        return self._document_date

    @document_date.setter
    def document_date(self, value):
        """
        A data não pode ser nula
        :return:
        """
        if value is None:
            value = datetime.datetime.now()
        elif isinstance(value, int):
            print(value)
            s, ms = divmod(value, 1000000)
            value = datetime.datetime.fromtimestamp(s)
            value = value.replace(microsecond=ms)

        self._document_date = value

    @staticmethod
    def create_table():
        """
        Cria índice no Elastic Search
        """
        options = {
            "settings": {
                "number_of_shards": "5",
                "number_of_replicas": "1",
                "analysis.analyzer.default.filter.0": "lowercase",
                "analysis.analyzer.default.filter.1": "asciifolding",
                "analysis.analyzer.default.tokenizer": "standard",
                "analysis.analyzer.default.type": "custom",
                "analysis.filter.pt_stemmer.type": "stemmer",
                "analysis.filter.pt_stemmer.name": "portuguese"
            },
            "mappings": {
                "document": {
                    "_timestamp": {
                        "enabled": "true"
                    }
                }
            }
        }
        result = config.ES.indices.create(
            index=config.ES_INDEX,
            body=options
        )

        return result

    @staticmethod
    def drop_table():
        """
        Apaga índice no Elastic Search
        """
        result = config.ES.indices.delete(
            index=config.ES_INDEX
        )

        return result

    @staticmethod
    def get_all():
        """
        Lista todos os documentos do Elastic Search

        :return: ES response
        """
        es = config.ES

        # Necessário dar um referesh no índice antes
        es.indices.refresh(index=config.ES_INDEX)

        query = {
            "query": {
                "match_all": {}
            }
        }


        response = es.search(
            index=config.ES_INDEX,
            body=query
        )
        return response

    def get(self):
        """
        Get document from ES

        :return: Dict with document
        """
        # Query for id field in element
        # query = {
        #    "query": {
        #        "query_string": {
        #            "default_field": "_id",
        #            "query": self.document_id
        #        }
        #    },
        #    "size": "1"
        # }

        # Check if document exists first

        exists = self.es.exists(
            index=self.es_index,
            id=self.document_id,
            doc_type='document'
        )

        if not exists:
            return None

        response = self.es.get(
            index=self.es_index,
            id=self.document_id,
            doc_type='document'
        )

        return response

    def add(self):
        """
        Add document on ES

        :return: Result
        """
        # O mapping nunca funciona direito
        content = self.content
        content['document_date'] = str(self.document_date)
        result = self.es.create(
            index=self.es_index,
            doc_type='document',
            body=content,
            id=self.document_id,
            timestamp=self.document_date
        )

        return result

    def update(self):
        """
        Update document on ES

        :return: Results
        """
        result = self.es.update(
            index=self.es_index,
            doc_type='document',
            body=self.content,
            id=self.document_id,
            timestamp=self.document_date
        )

        return result