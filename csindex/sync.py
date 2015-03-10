#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
from .daemon import Daemon
from . import config
from .model import es
from .model import cs
from elasticsearch.exceptions import NotFoundError
from cassandra import InvalidRequest
from multiprocessing import Pool

log = logging.getLogger()


class Sync(Daemon):
    """
    Classe responsável pela sincronia dos documentos
    """
    def __init__(self, **args):
        """
        Método construtor
        """
        super(Sync, self).__init__(**args)

    @staticmethod
    def process_es():
        """
        Procedimento que processa os documentos do Elastic Search para
        sincronizar com o Cassandra.

        Regra: o mais atual sempre ganha
        :return:
        """
        try:
            response = es.ES.get_all()
        except NotFoundError as e:
            log.debug("Índice não existe no Elastic Search. Criando...")
            es.ES.create_table()

            log.debug("Índice do Elastic Search criado com sucesso. Finalizando...")
            return True

        hits = response.get('hits')
        if hits is not None:
            for res in hits['hits']:
                # Now try to find document in Cassandra
                cassandra = cs.CS(
                    document_id=int(res['_id']),
                    content=res['_source']
                )
                cassandra_doc = cassandra.get()
                if cassandra_doc is None:
                    # Add document in Cassandra
                    log.info("Documento %s não encontrado no Cassandra. Adicionando...", res['_id'])
                    cassandra.add()
                else:
                    # Check which is newer
                    if cassandra.document_date > res['_source']['document_date']:
                        log.info("Documento do Cassandra mais atual. Adicionando %s no ES", res['_id'])
                        es_obj = es.ES(
                            document_id=cassandra_doc['document_id'],
                            content=cassandra_doc['content'],
                            document_date=cassandra_doc['document_date']
                        )
                        es_obj.update()
                    else:
                        log.info("Documento do ES mais atual ou data igual. Atualiza %s no cassandra", res['_id'])
                        cassandra.update()

        return True

    @staticmethod
    def process_cassandra():
        """
        Processa documentos do Cassandra
        """
        try:
            response = cs.CS.get_all()
        except InvalidRequest as e:
            log.debug("Tabela do Cassandra não existe. Criando...")
            cs.CS.create_table()

            log.debug("Tabela criada com sucesso. Finalizando...")
            return True

        if type(response) == list and len(response) > 0:
            # Processa somente se houve respostas
            for elm in response:
                # Busca primeiro no ES
                es_obj = es.ES(
                    document_id=elm['document_id'],
                    content=elm['content']
                )
                es_doc = es_obj.get()
                if es_doc is None:
                    log.info("Documento %s não encontrado no ES. Adicionando...", elm['document_id'])
                    es_obj.add()
                else:
                    # Verifica o mais atual
                    if es_obj.document_date >= elm['document_date']:
                        log.info("Documento do ES mais atual ou igual. Adicionando %s no Cassandra", elm['document_id'])
                        cassandra = cs.CS(
                            document_id=es_doc['_id'],
                            document_date=es_doc['_source']['document_date'],
                            content=es_doc['_source']
                        )
                        cassandra.update()
                    else:
                        log.info("Documento do Cassandra mais atual. Atualiza %s no ES", elm['document_id'])
                        es_obj.update()

        return True

    def run(self):
        """
        Executa a sincronia entre os dois bancos
        """
        log.info("Iniciando módulo de sincronia ES e Cassandra")
        while True:
            log.info("Iniciando sincronia no Elastic Search")
            try:
                self.process_es()
            except Exception as e:
                log.critical(str(e))

            log.info("Iniciando sincronia do Cassandra")
            try:
                self.process_cassandra()
            except Exception as e:
                log.critical(str(e))

            # Tempo de espera
            log.info("Execução finalizada. Esperando %s segundos", config.TIMER)
            time.sleep(config.TIMER)