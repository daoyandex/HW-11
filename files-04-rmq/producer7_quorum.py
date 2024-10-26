#!/usr/bin/env python
# coding=utf-8
import os
import sys
import pika
import time

from settings import URI

credentials = pika.PlainCredentials('admin', 'adminpasswd')
params = pika.ConnectionParameters('DebianVM1', 5672, "/", credentials)
#connection = pika.BlockingConnection(params)
#channel = connection.channel()

#params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='exch_quorum', exchange_type='fanout', durable=True)
#channel.queue_declare(queue='task_2', passive=False, durable=True)

#routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[1:]) or "Hello Netology!"
count = 0
while True:
    g = f"{message} - {count}"
    channel.basic_publish(exchange="exch_quorum", 
                          routing_key="quorum", 
                          body=g,
                          properties=pika.BasicProperties(
                              delivery_mode=pika.DeliveryMode.Persistent
                              )
                          )
    
    #channel.basic_publish(exchange='', 
    #                      routing_key='task_2', 
    #                      body=g,
    #                      properties=pika.BasicProperties(
    #                          delivery_mode=pika.DeliveryMode.Persistent
    #                          )
    #                      )
        
    time.sleep(g.count('.'))
    count += 1
    print(f" [x] Sent {message} - {count}")


connection.close()