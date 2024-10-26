#!/usr/bin/env python
# coding=utf-8
import os
import sys
import pika
import time

from settings import URI

#credentials = pika.PlainCredentials('testuser', 'testpasswd')
#parameters = pika.ConnectionParameters('debian', 5672,"/", credentials)
#connection = pika.BlockingConnection(parameters)
#channel = connection.channel()

params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

##channel.exchange_declare(exchange='logs', exchange_type='fanout', passive=False, durable=True)

channel.queue_declare(queue='task_2', passive=False, durable=True)

message = ' '.join(sys.argv[1:]) or "info: Hello Netology!"
count = 0
while True:
    g = f"{message} - {count}"
    #channel.basic_publish(exchange="logs", routing_key='hello', body=g)
    channel.basic_publish(exchange='', 
                          routing_key='task_2', 
                          body=g,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.DeliveryMode.Persistent
                              )
                          )
    #time.sleep(1)
    time.sleep(g.count('.'))
    count += 1
    print(f" [x] Sent {message} - {count}")


connection.close()