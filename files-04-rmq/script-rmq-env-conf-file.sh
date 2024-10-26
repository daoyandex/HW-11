#!/bin/bash

PATH_GLOB_ENV_FILE=/etc/environment
PATH_RMQ_CONF_ENV_FILE=/etc/rabbitmq/rabbitmq-env.conf
STR_PATH_RMQ_CONF_ENV_FILE_QUOTES=$(echo \'${PATH_RMQ_CONF_ENV_FILE}\')

sudo grep -Rw -F -e 'RABBITMQ_CONF_ENV_FILE="/etc/rabbitmq/rabbitmq-env.conf"' $PATH_GLOB_ENV_FILE >/dev/null 2>&1
A=$?
echo A

if [[ ! $A -eq 0 ]]; then

## если внезапно в определение переменной зашла строка пути к rabbitmq-env.conf в одинарных кавычках
## RABBITMQ_CONF_ENV_FILE='/etc/rabbitmq/rabbitmq-env.conf'
## it turns out it's a big problem to delete a string with single quotes using sed

sudo sed -i -E "s|^RABBITMQ_CONF_ENV_FILE=$STR_PATH_RMQ_CONF_ENV_FILE_QUOTES$||g" $PATH_GLOB_ENV_FILE
sudo sed -i '/^$/d' $PATH_GLOB_ENV_FILE

sudo tee -a $PATH_GLOB_ENV_FILE <<EOF
RABBITMQ_CONF_ENV_FILE="$PATH_RMQ_CONF_ENV_FILE"
EOF

fi

source $PATH_GLOB_ENV_FILE
