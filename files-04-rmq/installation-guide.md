# FROM https://www.rabbitmq.com/docs/install-debian

## Install Essential Dependencies
```  bash
sudo apt-get update -y
sudo apt-get install curl gnupg -y
```
## Enable apt HTTPS Transport
In order for apt to be able to download RabbitMQ and Erlang packages from the Cloudsmith.io mirror or Launchpad, the 
apt-transport-https package must be installed:
``` bash
sudo apt-get install apt-transport-https
```
## Add Repository Signing Keys
Cloudsmith signs distributed packages using their own GPG keys, one per repository. Team RabbitMQ's mirrors have the same contents, therefore, the packages are signed using the same key.

In order to use the repositories, their signing keys must be added to the system. This will enable apt to trust packages signed by that key.
``` bash
sudo apt-get install curl gnupg apt-transport-https -y
```
#### Team RabbitMQ's main signing key
``` bash
curl -1sLf "https://keys.openpgp.org/vks/v1/by-fingerprint/0A9AF2115F4687BD29803A206B73A36E6026DFCA" | sudo gpg --dearmor | sudo tee /usr/share/keyrings/com.rabbitmq.team.gpg > /dev/null
```
#### Community mirror of Cloudsmith: modern Erlang repository
``` bash
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-erlang.E495BB49CC4BBE5B.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg > /dev/null
```
#### Community mirror of Cloudsmith: RabbitMQ repository
``` bash
curl -1sLf https://github.com/rabbitmq/signing-keys/releases/download/3.0/cloudsmith.rabbitmq-server.9F4587F226208342.key | sudo gpg --dearmor | sudo tee /usr/share/keyrings/rabbitmq.9F4587F226208342.gpg > /dev/null
```

See the guide on signatures to learn more.

## Add a Repository (Apt Source List) File
important
The contents of the file described in this section will vary slightly based on the target Debian-based distribution. Make sure to switch to the appropriate tab.

As with all 3rd party apt repositories, a file describing the RabbitMQ and Erlang package repositories must be placed under the /etc/apt/sources.list.d/ directory. /etc/apt/sources.list.d/rabbitmq.list is the recommended location.

The contents of the file will vary slightly based on the distribution used.

Ubuntu 24.04
Ubuntu 22.04
Ubuntu 20.04
Debian Bookworm
Debian Bullseye
Debian Buster
Debian Trixie and Debian Sid

``` bash
sudo tee /etc/apt/sources.list.d/rabbitmq.list <<EOF
## Provides modern Erlang/OTP releases from a Cloudsmith mirror
##
deb [arch=amd64 signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.rabbitmq.com/rabbitmq/rabbitmq-erlang/deb/debian bookworm main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa1.rabbitmq.com/rabbitmq/rabbitmq-erlang/deb/debian bookworm main
# another mirror for redundancy
deb [arch=amd64 signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.rabbitmq.com/rabbitmq/rabbitmq-erlang/deb/debian bookworm main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.E495BB49CC4BBE5B.gpg] https://ppa2.rabbitmq.com/rabbitmq/rabbitmq-erlang/deb/debian bookworm main
## Provides RabbitMQ from a Cloudsmith mirror
##
deb [arch=amd64 signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.rabbitmq.com/rabbitmq/rabbitmq-server/deb/debian bookworm main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa1.rabbitmq.com/rabbitmq/rabbitmq-server/deb/debian bookworm main
# another mirror for redundancy
deb [arch=amd64 signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.rabbitmq.com/rabbitmq/rabbitmq-server/deb/debian bookworm main
deb-src [signed-by=/usr/share/keyrings/rabbitmq.9F4587F226208342.gpg] https://ppa2.rabbitmq.com/rabbitmq/rabbitmq-server/deb/debian bookworm main
EOF
```

## Install Packages
After updating the list of apt sources it is necessary to run apt-get update:
``` bash
sudo apt-get update -y
```
Then install the package with
``` bash
## Install Erlang packages
sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl
```
---
``` bash
## Install rabbitmq-server and its dependencies
sudo apt-get install rabbitmq-server -y --fix-missing
```

## Debian Package Version and Repository Pinning
Version pinning is an optional step. If not used, apt will install the most recent version available.

When the same package (e.g. erlang-base) is available from multiple apt repositories operators need to have a way to indicate what repository should be preferred. It may also be desired to restrict Erlang version to avoid undesired upgrades. apt package pinning feature can be used to address both problems.

Package pinning is configured with a file placed under the /etc/apt/preferences.d/ directory, e.g. /etc/apt/preferences.d/erlang. After updating apt preferences it is necessary to run apt-get update:
``` bash
sudo apt-get update -y
```

The following preference file example will configure apt to install erlang-* packages from the Cloudsmith mirror used in the examples above:
``` bash
# /etc/apt/preferences.d/erlang
Package: erlang*
Pin: origin ppa1.rabbitmq.com
# Note: priority of 1001 (greater than 1000) allows for downgrading.
# To make package downgrading impossible, use a value of 999
Pin-Priority: 1001
```
The following is similar to the example above but prefers Launchpad:
``` bash
# /etc/apt/preferences.d/erlang
Package: erlang*
Pin: origin ppa.launchpad.net
# Note: priority of 1001 (greater than 1000) allows for downgrading.
# To make package downgrading impossible, use a value of 999
Pin-Priority: 1001
```
Effective package pinning policy can be verified with
``` bash
sudo apt-cache policy
```

The following preference file example will pin all erlang-* packages to 25.3 (assuming package epoch for the package is 1):
``` bash
# /etc/apt/preferences.d/erlang
Package: erlang*
Pin: version 1:26.2.5.2-1
# Note: priority of 1001 (greater than 1000) allows for downgrading.
# To make package downgrading impossible, use a value of 999
Pin-Priority: 1001
```

The following preference file example will pin rabbitmq-server package to 4.0.2 (assuming package epoch for the package is 1):
``` bash
# /etc/apt/preferences.d/rabbitmq
Package: rabbitmq-server
Pin: version 1:4.0.2-1
# Note: priority of 1001 (greater than 1000) allows for downgrading.
# To make package downgrading impossible, use a value of 999
Pin-Priority: 1001
```

## Install plugin for web-interface

```bash
sudo rabbitmq-plugins enable rabbitmq_management
```

## Install Python with virtual environment and RaabitMQ module 'pika' for programming for

``` bash
$ python3 -m venv ~/python-venv
$ ~/python-venv/bin/pip install pika
```


