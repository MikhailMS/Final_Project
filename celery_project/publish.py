import pika
import json

properties = pika.BasicProperties(content_type = 'application/json', delivery_mode = 1)
cred       = pika.PlainCredentials('segal', 'segal')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       'segal',
                                       cred)

body = json.dumps({
	"id": "4cc7438e-afd4-4f8f-a2f3-f46567e7ca77",
	"task": "tasks.music_composition_wrapper",
	"args": ['1', '2', '3', '4', '1'],
	"kwargs": {},
	"retries": 0
})

print body

connection = pika.BlockingConnection(parameters)
channel    = connection.channel()
channel.basic_publish(exchange = 'celery', routing_key = 'celery',
                      body = body, properties = properties)

channel.close()
