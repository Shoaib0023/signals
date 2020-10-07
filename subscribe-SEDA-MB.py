#!/usr/bin/env python
import pika
import requests
import json
import base64

credentials = pika.PlainCredentials('signals', 'insecure')
parameters = pika.ConnectionParameters('ec2-52-200-189-81.compute-1.amazonaws.com',
                                       5672,
                                       'vhost',
                                       credentials)


def callback(ch, method, properties, body):
    print("Called ......")
    return 

    # print(" [x] Received %r" % json.loads(body))
    print("Creating a signal in MB ....")
    user_credentials = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsIl9pZCI6IjVkYWNiOTQ0MTdhOGRjN2U2NTdiMjNjNyIsImRldmljZSI6bnVsbCwidG9rZW4iOm51bGwsImxhbmd1YWdlIjoiMSJ9",
        "email" : "prashant.shukla.in@gmail.com",
        "password": "123456",
    }

    data = json.loads(body)['signals']
    url = data.pop('image_url')
    # print(url)
    # url = 'http://localhost:8000/signals/media/attachments/2020/09/16/test.png'
    if url:
        response = requests.get(url)
        uri = ("data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8")))
        data["issue_image"] = [uri]

    response = requests.post("https://admin.haagsebeheerder.nl/index.php/api/submit_mor", json=data)
    print(response.status_code)
    print("\n")


connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='SEDA-MB', durable=True)
channel.basic_consume(queue='SEDA-MB', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

