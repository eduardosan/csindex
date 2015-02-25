#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import logging
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

    @staticmethod
    def get_all():
        """
        Lista todos os documentos do Elastic Search

        :return: ES response
        """
        query = {
            "match_all": {}
        }

        es = config.ES
        response = es.search(
            index=config.ES_INDEX,
            body={"query": query}
        )
        return response

    def get(self):
        """
        Get document from ES

        :return: Dict with document
        """
        # Query for id field in element
        query = {
            "query": {
                "query_string": {
                    "default_field": "id",
                    "query": self.document_id
                }
            },
            "size": "1"
        }

        response = self.es.search(
            index=self.es_index,
            body={"query": query}
        )

        # Now we have to parse the result back to package dict
        hits = response.get('hits')
        resources = dict()
        for res in hits['hits']:
            # Store it in extras
            resources = res

            # Return only first item
            break

        # Verifica se houve algum resultado
        if resources:
            self.document_date = resources['_source']['document_date']

            return resources
        else:
            # Return empty dict if it's not found
            return None

    def add(self):
        """
        Add document on ES

        :return: Result
        """
        result = self.es.create(
            index=self.es,
            doc_type='document',
            body=self.content
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
            body=self.content
        )

        return result