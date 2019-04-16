#!/bin/bash

set -e

#
#
#
/usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached

# Do the cluster dance here
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@rabbitmq1

#
#
#
rabbitmqctl stop

# Wait for rabbitmq service to actually stop
sleep 2s

# Start RabbitMQ service
rabbitmq-server
