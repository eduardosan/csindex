#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import uuid


class Document(object):
    """
    Documento a ser sicnronizado nas várias bases de dados
    """
    def __init__(self,
                 document_date,
                 document_content,
                 document_author,
                 document_id=None):
        """
        :param document_id: Identificador do documento
        :param document_date: Data do documento
        :param document_content: Conteúdo
        :param document_author: Autor
        """
        # Auto generate UUID if it is not supplied
        if document_id is None:
            document_id = uuid.uuid4()

        self.document_id = document_id
        self.document_date = document_date
        self.document_content = document_content
        self.document_author = document_author