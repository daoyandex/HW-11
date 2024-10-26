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

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
#channel.queue_declare(queue='task_2', passive=False, durable=True)

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'
message = ' '.join(sys.argv[2:]) or "Hello Netology!"
count = 0
while True:
    g = f"{message} - {count}"
    channel.basic_publish(exchange="topic_logs", 
                          routing_key=routing_key, 
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
    print(f" [x] Sent {routing_key} : {message} - {count}")


connection.close()