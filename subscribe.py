#!/usr/bin/env python
import pika
import requests
import json

credentials = pika.PlainCredentials('signals', 'insecure')
parameters = pika.ConnectionParameters('ec2-52-200-189-81.compute-1.amazonaws.com',
                                       5672,
                                       'vhost',
                                       credentials)


def callback(ch, method, properties, body):
    # print(" [x] Received %r" % json.loads(body))
    print("Creating a signal in MB ....")
    user_credentials = {
        "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsIl9pZCI6IjVkYWNiOTQ0MTdhOGRjN2U2NTdiMjNjNyIsImRldmljZSI6bnVsbCwidG9rZW4iOm51bGwsImxhbmd1YWdlIjoiMSJ9",
        "email" : "prashant.shukla.in@gmail.com",
        "password": "123456",
    }

    headers = {"Authorization": user_credentials["token"]}
    data = json.loads(body)['signals']
    files = json.loads(body)['signals'].pop('issue_image')

    response = requests.post("https://admin.haagsebeheerder.nl/index.php/api/submit_report/", data=data, headers=headers)
    print(response.status_code)
    print(response.json())
    print("\n")


connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='SEDA-MB', durable=True)
channel.basic_consume(queue='SEDA-MB', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

