# csindex
Cassandra Index on Elastic Search

# Install
* Instala dependências

<pre>
sudo apt-get install build-essential python-dev libev4 libev-dev git
</pre>

* Instala o Elastic Search: [Página de download](http://www.elasticsearch.org/overview/elkdownloads/)

* Instala o Cassandra: [Manual para o Debian](http://www.datastax.com/documentation/cassandra/2.1/cassandra/install/installDeb_t.html)

* Cria um ambiente virtual. No exemplo utilizaremos o diretório srv por padrão

<pre>
cd /srv
virtualenv -p /usr/bin/python3.4 csindex
cd csindex
mkdir src
</pre>

* Agora baixe e compile o código

<pre>
cd /srv/csindex/src
git clone https://github.com/eduardosan/csindex.git
cd csindex
/srv/csindex/bin/python setup.py develop
</pre>

*Importante*: O sistema foi testado apenas no **Python 3.4**

# Utilização

* Configure o arquivo production.ini para a sua instação

<pre>
cd /srv/csindex/src/csindex
cp production.ini-dist production.ini
</pre>

* Configure as URL's do Elastic Search e do Cassandra no arquivo production.ini Se você fez a instalação padrão os parâmetros devem estar assim:

<pre>
[Daemon]
(...)
cassandra_cluster = 127.0.0.1
es_url = http://localhost:9200/
</pre>

* Configure o nome da base onde deve ocorrer a sincronia. Deve coincidir com o índice do Elstic Search.

<pre>
[Daemon]
(...)
es_index = doc
</pre>

* Execute o comando para iniciar a sincronia

<pre>
cd /srv/csindex/src/csindex
/srv/csindex/bin/python csindex start
</pre>

O daemon de execução da sincronia vai rodar.

# Operação

* Teste inserido um documento no Cassandra:

<pre>
cqlsh 
Connected to Test Cluster at 127.0.0.1:9042.
[cqlsh 5.0.1 | Cassandra 2.1.3 | CQL spec 3.2.0 | Native protocol v3]
Use HELP for help.
cqlsh> desc keyspaces;

doc  system  demo  system_traces

cqlsh> use doc;
cqlsh:doc> INSERT INTO doc (id_doc, content) VALUES ('02117321-a40b-40a1-8b54-faee7fb4e6a5', '{"teste": 1234}');
cqlsh:doc> select * from doc;

 id_doc                               | content
--------------------------------------+-----------------
 02117321-a40b-40a1-8b54-faee7fb4e6a5 | {"teste": 1234}

(1 rows)
cqlsh:doc> exit
</pre>

* Verifique se o document existe no elastic search

<pre>
curl -XGET 'http://localhost:9200/doc/document/02117321-a40b-40a1-8b54-faee7fb4e6a5'
{"_index":"doc","_type":"document","_id":"02117321-a40b-40a1-8b54-faee7fb4e6a5","_version":1,"exists":true, "_source" : {"teste": 1234}}
</pre>

* Agora teste o contrário

<pre>

</pre>