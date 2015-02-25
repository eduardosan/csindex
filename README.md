# csindex
Cassandra Index on Elastic Search

# Install
* Instala dependências

<pre>
sudo apt-get install build-essential python-dev libev4 libev-dev
</pre>

* Instala o Elastic Search: [Página de download](http://www.elasticsearch.org/overview/elkdownloads/)

* Instala o Cassandra: [Manual para o Debian](http://www.datastax.com/documentation/cassandra/2.1/cassandra/install/installDeb_t.html)

# Utilização

* Configure as URL's do Elastic Search e do Cassandra no arquivo production.ini

* Execute o comando para iniciar a sincronia

<pre>
python csindex start
</pre>

O daemon de execução da sincronia vai rodar 