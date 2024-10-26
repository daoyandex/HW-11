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

channel.exchange_declare(exchange='direct_logs', exchange_type='direct', passive=False, durable=True)
#channel.queue_declare(queue='task_2', passive=False, durable=True)

severity = sys.argv[1] if len(sys.argv) > 1 else 'info'
message = ' '.join(sys.argv[2:]) or "Hello Netology!"
count = 0
while True:
    g = f"{message} - {count}"
    channel.basic_publish(exchange="direct_logs", 
                          routing_key=severity, 
                          body=g)
    
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