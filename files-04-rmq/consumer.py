#!/usr/bin/env python
# coding=utf-8
import os
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout", passive=False, durable=True)
channel.queue_declare(queue='hello', passive=False, durable=True)

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)
channel.start_consuming(5)