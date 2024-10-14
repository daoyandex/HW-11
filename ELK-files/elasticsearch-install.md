# Import the Elasticsearch PGP Key
![elastic.co installation guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)

We sign all of our packages with the Elasticsearch Signing Key (PGP key D88E42B4, available from https://pgp.mit.edu) with fingerprint:

4609 5ACC 8548 582C 1A26 99A9 D27D 666C D88E 42B4

## Download and install the public signing key:
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg

# Installing from the APT repository

## You may need to install the apt-transport-https package on Debian before proceeding:
sudo apt-get install apt-transport-https

## Save the repository definition to /etc/apt/sources.list.d/elastic-8.x.list:
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list


These instructions do not use add-apt-repository for several reasons:

add-apt-repository adds entries to the system /etc/apt/sources.list file rather than a clean per-repository file in /etc/apt/sources.list.d
add-apt-repository is not part of the default install on many distributions and requires a number of non-default dependencies.
Older versions of add-apt-repository always add a deb-src entry which will cause errors because we do not provide a source package. If you have added the deb-src entry, you will see an error like the following until you delete the deb-src line:

Unable to find expected entry 'main/source/Sources' in Release file
(Wrong sources.list entry or malformed file)

(
    Эти инструкции не используют add-apt-repository по нескольким причинам:

add-apt-repository добавляет записи в системный файл /etc/apt/sources.list, а не в чистый файл для каждого репозитория в /etc/apt/sources.list.d
add-apt-repository не является частью установки по умолчанию во многих дистрибутивах и требует ряда нестандартных зависимостей.
Более старые версии add-apt-repository всегда добавляют запись deb-src, что приведет к ошибкам, поскольку мы не предоставляем исходный пакет. Если вы добавили запись deb-src, вы увидите ошибку, подобную следующей, пока не удалите строку deb-src:

Невозможно найти ожидаемую запись 'main/source/Sources' в файле Release
(Неправильная запись sources.list или некорректный файл)
)

# You can install the Elasticsearch Debian package with:
sudo apt-get update && sudo apt-get install elasticsearch

If two entries exist for the same Elasticsearch repository, you will see an error like this during apt-get update:
Duplicate sources.list entry https://artifacts.elastic.co/packages/8.x/apt/ ...`
Examine /etc/apt/sources.list.d/elasticsearch-8.x.list for the duplicate entry or locate the duplicate entry amongst the files in /etc/apt/sources.list.d/ and the /etc/apt/sources.list file.

On systemd-based distributions, the installation scripts will attempt to set kernel parameters (e.g., vm.max_map_count); you can skip this by masking the systemd-sysctl.service unit.

# Download and install the Debian package manually

## The Debian package for Elasticsearch v8.15.2 can be downloaded from the website and installed as follows:
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.2-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.2-amd64.deb.sha512
shasum -a 512 -c elasticsearch-8.15.2-amd64.deb.sha512 
sudo dpkg -i elasticsearch-8.15.2-amd64.deb


Start Elasticsearch with security enabled
edit
When installing Elasticsearch, security features are enabled and configured by default. When you install Elasticsearch, the following security configuration occurs automatically:

Authentication and authorization are enabled, and a password is generated for the elastic built-in superuser.
Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.
The password and certificate and keys are output to your terminal. You can reset the password for the elastic user with the elasticsearch-reset-password command.

We recommend storing the elastic password as an environment variable in your shell. For example:

export ELASTIC_PASSWORD="your_password"
Reconfigure a node to join an existing cluster
edit
When you install Elasticsearch, the installation process configures a single-node cluster by default. If you want a node to join an existing cluster instead, generate an enrollment token on an existing node before you start the new node for the first time.

On any node in your existing cluster, generate a node enrollment token:

/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
Copy the enrollment token, which is output to your terminal.
On your new Elasticsearch node, pass the enrollment token as a parameter to the elasticsearch-reconfigure-node tool:

/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
Elasticsearch is now configured to join the existing cluster.

Start your new node using systemd.
Enable automatic creation of system indices
edit
Some commercial features automatically create indices within Elasticsearch. By default, Elasticsearch is configured to allow automatic index creation, and no additional steps are required. However, if you have disabled automatic index creation in Elasticsearch, you must configure action.auto_create_index in elasticsearch.yml to allow the commercial features to create the following indices:

action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*
If you are using Logstash or Beats then you will most likely require additional index names in your action.auto_create_index setting, and the exact value will depend on your local configuration. If you are unsure of the correct value for your environment, you may consider setting the value to * which will allow automatic creation of all indices.

Running Elasticsearch with systemd
edit
To configure Elasticsearch to start automatically when the system boots up, run the following commands:

sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
Elasticsearch can be started and stopped as follows:

sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
These commands provide no feedback as to whether Elasticsearch was started successfully or not. Instead, this information will be written in the log files located in /var/log/elasticsearch/.

If you have password-protected your Elasticsearch keystore, you will need to provide systemd with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once Elasticsearch is up and running.

echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
By default the Elasticsearch service doesn’t log information in the systemd journal. To enable journalctl logging, the --quiet option must be removed from the ExecStart command line in the elasticsearch.service file.

When systemd logging is enabled, the logging information are available using the journalctl commands:

To tail the journal:

sudo journalctl -f
To list journal entries for the elasticsearch service:

sudo journalctl --unit elasticsearch
To list journal entries for the elasticsearch service starting from a given time:

sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
Check man journalctl or https://www.freedesktop.org/software/systemd/man/journalctl.html for more command line options.

Startup timeouts with older systemd versions
By default Elasticsearch sets the TimeoutStartSec parameter to systemd to 900s. If you are running at least version 238 of systemd then Elasticsearch can automatically extend the startup timeout, and will do so repeatedly until startup is complete even if it takes longer than 900s.

Versions of systemd prior to 238 do not support the timeout extension mechanism and will terminate the Elasticsearch process if it has not fully started up within the configured timeout. If this happens, Elasticsearch will report in its logs that it was shut down normally a short time after it started:

[2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
...
[2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...
However the systemd logs will report that the startup timed out:

Jan 31 01:22:30 debian systemd[1]: Starting Elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start Elasticsearch.
To avoid this, upgrade your systemd to at least version 238. You can also temporarily work around the problem by extending the TimeoutStartSec parameter.

Check that Elasticsearch is running
edit
You can test that your Elasticsearch node is running by sending an HTTPS request to port 9200 on localhost:

curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 

Ensure that you use https in your call, or the request will fail.

--cacert
Path to the generated http_ca.crt certificate for the HTTP layer.
The call returns a response like this:

{
  "name" : "Cp8oag6",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
  "version" : {
    "number" : "8.15.2",
    "build_type" : "tar",
    "build_hash" : "f27399d",
    "build_flavor" : "default",
    "build_date" : "2016-03-30T09:51:41.449Z",
    "build_snapshot" : false,
    "lucene_version" : "9.11.1",
    "minimum_wire_compatibility_version" : "1.2.3",
    "minimum_index_compatibility_version" : "1.2.3"
  },
  "tagline" : "You Know, for Search"
}
Configuring Elasticsearch
edit
The /etc/elasticsearch directory contains the default runtime configuration for Elasticsearch. The ownership of this directory and all contained files are set to root:elasticsearch on package installations.

The setgid flag applies group permissions on the /etc/elasticsearch directory to ensure that Elasticsearch can read any contained files and subdirectories. All files and subdirectories inherit the root:elasticsearch ownership. Running commands from this directory or any subdirectories, such as the elasticsearch-keystore tool, requires root:elasticsearch permissions.

Elasticsearch loads its configuration from the /etc/elasticsearch/elasticsearch.yml file by default. The format of this config file is explained in Configuring Elasticsearch.

The Debian package also has a system configuration file (/etc/default/elasticsearch), which allows you to set the following parameters:

ES_JAVA_HOME

Set a custom Java path to be used.

ES_PATH_CONF

Configuration file directory (which needs to include elasticsearch.yml, jvm.options, and log4j2.properties files); defaults to /etc/elasticsearch.

ES_JAVA_OPTS

Any additional JVM system properties you may want to apply.

RESTART_ON_UPGRADE

Configure restart on package upgrade, defaults to false. This means you will have to restart your Elasticsearch instance after installing a package manually. The reason for this is to ensure, that upgrades in a cluster do not result in a continuous shard reallocation resulting in high network traffic and reducing the response times of your cluster.

Distributions that use systemd require that system resource limits be configured via systemd rather than via the /etc/sysconfig/elasticsearch file. See Systemd configuration for more information.

Connect clients to Elasticsearch
edit
When you start Elasticsearch for the first time, TLS is configured automatically for the HTTP layer. A CA certificate is generated and stored on disk at:

/etc/elasticsearch/certs/http_ca.crt
The hex-encoded SHA-256 fingerprint of this certificate is also output to the terminal. Any clients that connect to Elasticsearch, such as the Elasticsearch Clients, Beats, standalone Elastic Agents, and Logstash must validate that they trust the certificate that Elasticsearch uses for HTTPS. Fleet Server and Fleet-managed Elastic Agents are automatically configured to trust the CA certificate. Other clients can establish trust by using either the fingerprint of the CA certificate or the CA certificate itself.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate. You can also copy the CA certificate to your machine and configure your client to use it.

Use the CA fingerprint
edit
Copy the fingerprint value that’s output to your terminal when Elasticsearch starts, and configure your client to use this fingerprint to establish trust when it connects to Elasticsearch.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate by running the following command. The path is to the auto-generated CA certificate for the HTTP layer.

openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt
The command returns the security certificate, including the fingerprint. The issuer should be Elasticsearch security auto-configuration HTTP CA.

issuer= /CN=Elasticsearch security auto-configuration HTTP CA
SHA256 Fingerprint=<fingerprint>
Use the CA certificate
edit
If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each Elasticsearch node:

/etc/elasticsearch/certs/http_ca.crt
Copy the http_ca.crt file to your machine and configure your client to use this certificate to establish trust when it connects to Elasticsearch.

Directory layout of Debian package
edit
The Debian package places config files, logs, and the data directory in the appropriate locations for a Debian-based system:

Type	Description	Default Location	Setting
home

Elasticsearch home directory or $ES_HOME

/usr/share/elasticsearch

bin

Binary scripts including elasticsearch to start a node and elasticsearch-plugin to install plugins

/usr/share/elasticsearch/bin

conf

Configuration files including elasticsearch.yml

/etc/elasticsearch

ES_PATH_CONF

conf

Environment variables including heap size, file descriptors.

/etc/default/elasticsearch

conf

Generated TLS keys and certificates for the transport and http layer.

/etc/elasticsearch/certs

data

The location of the data files of each index / shard allocated on the node.

/var/lib/elasticsearch

path.data

jdk

The bundled Java Development Kit used to run Elasticsearch. Can be overridden by setting the ES_JAVA_HOME environment variable in /etc/default/elasticsearch.

/usr/share/elasticsearch/jdk

logs

Log files location.

/var/log/elasticsearch

path.logs

plugins

Plugin files location. Each plugin will be contained in a subdirectory.

/usr/share/elasticsearch/plugins

repo

Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here.

Not configured

path.repo

Security certificates and keys
edit
When you install Elasticsearch, the following certificates and keys are generated in the Elasticsearch configuration directory, which are used to connect a Kibana instance to your secured Elasticsearch cluster and to encrypt internode communication. The files are listed here for reference.

http_ca.crt
The CA certificate that is used to sign the certificates for the HTTP layer of this Elasticsearch cluster.
http.p12
Keystore that contains the key and certificate for the HTTP layer for this node.
transport.p12
Keystore that contains the key and certificate for the transport layer for all the nodes in your cluster.
http.p12 and transport.p12 are password-protected PKCS#12 keystores. Elasticsearch stores the passwords for these keystores as secure settings:
https://www.elastic.co/guide/en/elasticsearch/reference/current/secure-settings.html

To retrieve the passwords so that you can inspect or change the keystore contents, use the bin/elasticsearch-keystore tool:
https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-keystore.html

Use the following command to retrieve the password for http.p12:

bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password
Use the following command to retrieve the password for transport.p12:

bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password
Next steps
edit
You now have a test Elasticsearch environment set up. Before you start serious development or go into production with Elasticsearch, you must do some additional setup:

Learn how to configure Elasticsearch:
https://www.elastic.co/guide/en/elasticsearch/reference/current/settings.html

Configure important Elasticsearch settings:
https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html

Configure important system settings:
https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html

#### ###############################################################################################

ser@debian:~/Загрузки$ sudo dpkg -i ./elasticsearch-8.15.2-amd64.deb
Выбор ранее не выбранного пакета elasticsearch.
(Чтение базы данных … на данный момент установлен 429301 файл и каталог.)
Подготовка к распаковке …/elasticsearch-8.15.2-amd64.deb …
Creating elasticsearch group... OK
Creating elasticsearch user... OK
Распаковывается elasticsearch (8.15.2) …
Настраивается пакет elasticsearch (8.15.2) …
--------------------------- Security autoconfiguration information ------------------------------

Authentication and authorization are enabled.
TLS for the transport and HTTP layers is enabled and configured.

The generated password for the elastic built-in superuser is : vJESd5V9XhDktrXa-Eus

If this node should join an existing cluster, you can reconfigure this with
'/usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <token-here>'
after creating an enrollment token on your existing cluster.

You can complete the following actions at any time:

Reset the password of the elastic built-in superuser with 
'/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic'.

Generate an enrollment token for Kibana instances with 
 '/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana'.

Generate an enrollment token for Elasticsearch nodes with 
'/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node'.

-------------------------------------------------------------------------------------------------
### NOT starting on installation, please execute the following statements to configure elasticsearch service to start automatically using systemd
 sudo systemctl daemon-reload
 sudo systemctl enable elasticsearch.service
### You can start elasticsearch service by executing
 sudo systemctl start elasticsearch.service
