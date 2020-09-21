#!/usr/bin/env python
import pika
import requests
import json
import datetime
import pytz
from dateutil import tz

credentials = pika.PlainCredentials('signals', 'insecure')
parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       'vhost',
                                       credentials)

def callback(ch, method, properties, body):
    body = json.loads(body)
    category_level_name1 = "Afval"
    category_level_name2 = "Afvalbakken"
    category_level_name3 = "Afvalbak"
    category_level_name4 = "Vol"

    # created_at = body["reports"][0]["created_at"]
    for report in body["reports"]:
        payload = {
                "location": {"geometrie": {"type":"Point","coordinates": [4.99054263,52.29994823]},
            			     "address": {"openbare_ruimte":"Anne Kooistrahof","huisnummer":"1","postcode":"1106WG","woonplaats":"Amsterdam"},"stadsdeel":"T"},
                "category":{"category_url":f"http://localhost:8000/signals/v1/public/terms/categories/{category_level_name1}/{category_level_name2}/{category_level_name3}/{category_level_name4}" },

                "reporter":{"phone":report["reported_by_data"][0]["mobile"], "email":report["reported_by_data"][0]["email_id"], "sharing_allowed":True},
                "incident_date_start": report["created_at"],
                "text":report["description"],
            }

        response = requests.post('http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/v1/public/signals/', json=payload)
        if response.status_code == 201:
            print("Successfully created a signal in MB : ", response.status_code)
        else:
            print("Error : ", response.status_code)


connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='hello1', durable=True)
channel.basic_consume(queue='hello1', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

