#!/usr/bin/env python
# coding=utf-8
import os
import sys
import pika
import time

from settings import URI

#credentials = pika.PlainCredentials('testuser', 'testpasswd')
#parameters = pika.ConnectionParameters('debian', 5672, "/", credentials)
#connection = pika.BlockingConnection(parameters)
#channel = connection.channel()

params = pika.URLParameters(URI)
connection = pika.BlockingConnection(params)
channel = connection.channel()

#channel.exchange_declare(exchange="logs", exchange_type="fanout", passive=False, durable=True)
result_queue = channel.queue_declare(queue='task_2', passive=False, durable=True)
queue_name = result_queue.method.queue

#channel.queue_bind(exchange='logs', queue=queue_name)

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    #time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback
                      )
channel.start_consuming()


##############################
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)