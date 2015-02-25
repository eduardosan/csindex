#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import uuid
import logging

log = logging.getLogger()


class Document(object):
    """
    Documento a ser sicnronizado nas várias bases de dados
    """
    def __init__(self,
                 content,
                 document_date=None,
                 document_id=None):
        """
        :param content: De onde veio a última sincronia
        :param document_date: Data do documento
        :param document_id: Identificador do documento
        """
        # Auto generate UUID if it is not supplied
        if document_id is None:
            document_id = uuid.uuid4()

        self.document_id = document_id
        self.document_date = document_date
        self.content = content