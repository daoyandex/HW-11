#!/usr/bin/env python
# coding=utf-8
import os
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs', exchange_type='fanout', passive=False, durable=True)
channel.queue_declare(queue='hello', passive=False, durable=True)

message = ' '.join(sys.argv[1:]) or "info: Hello Netology!"

channel.basic_publish(exchange='logs', routing_key='hello', body=message)

print(f" [x] Sent {message}")

connection.close()