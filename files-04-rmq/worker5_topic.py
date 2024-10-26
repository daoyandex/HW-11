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

channel.exchange_declare(exchange="topic_logs", exchange_type="topic")

result_queue = channel.queue_declare(queue='', exclusive=True)
queue_name = result_queue.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_keys]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', 
                       queue=queue_name,
                       routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(f" [x] {method.routing_key}:{body}")
    #print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    #print(" [x] Done")
    #ch.basic_ack(delivery_tag = method.delivery_tag)


#channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name,
                      on_message_callback=callback,
                      auto_ack=True)
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