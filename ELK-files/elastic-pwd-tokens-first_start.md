https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html#deb-enable-indices

#
1. The generated password for the elastic built-in superuser is :
vJESd5V9XhDktrXa-Eus

#
2. On any node in your existing cluster, generate a node enrollment token:
sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
token for node:
eyJ2ZXIiOiI4LjE0LjAiLCJhZHIiOlsiMTcyLjE3LjAuMTo5MjAwIl0sImZnciI6ImMwZWEzMjllMmY0NmQwZTI2ZWQxOGM4YWM4ZjFkN2VhNTg4MjAyM2Q3NDZlY2MxMzM1MDU0NjJlYjA2OWUyMzIiLCJrZXkiOiJYSU81aDVJQmdLZzdPeXZFWkdoYzp2RlpuZnBXT1NqeUhRdWVLanBaUWpBIn0=

#
Copy the enrollment token, which is output to your terminal.

#
On your new Elasticsearch node, pass the enrollment token as a parameter to the elasticsearch-reconfigure-node tool:
/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
Elasticsearch is now configured to join the existing cluster.

# 
3. echo vJESd5V9XhDktrXa-Eus > /home/user/HW-11/ELK-files/elasticsearch_pwd.tmp

#
4. sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=~/HW-11/ELK-files/elasticsearch_pwd.tmp
5. sudo systemctl start elasticsearch.service

#
6. By default the Elasticsearch service doesn’t log information in the systemd journal. To enable journalctl logging, the --quiet option must be removed from the ExecStart command line in the elasticsearch.service file.

When systemd logging is enabled, the logging information are available using the journalctl commands:

To tail the journal:
sudo journalctl -f

To list journal entries for the elasticsearch service:
sudo journalctl --unit elasticsearch

To list journal entries for the elasticsearch service starting from a given time:
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"

## Проверка работы:
7. Проверка запуска
Check that Elasticsearch is running
You can test that your Elasticsearch node is running by sending an HTTPS request to port 9200 on localhost:
curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 

Ensure that you use https in your call, or the request will fail.
--cacert

Path to the generated http_ca.crt certificate for the HTTP layer.

### добавить в ~/.bashrc
user@debian:~/Загрузки$ export ELASTIC_PASSWORD=vJESd5V9XhDktrXa-Eus

user@debian:~/Загрузки$ sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 
{
  "name" : "debian",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "kNvCuHMDRkqq14q-3SSBEg",
  "version" : {
    "number" : "8.15.2",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "98adf7bf6bb69b66ab95b761c9e5aadb0bb059a3",
    "build_date" : "2024-09-19T10:06:03.564235954Z",
    "build_snapshot" : false,
    "lucene_version" : "9.11.1",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}

## Проверка 2:
user@debian:~$ sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200/_cluster/health?pretty 

{
  "cluster_name" : "elasticsearch",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 1,
  "active_shards" : 1,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}




