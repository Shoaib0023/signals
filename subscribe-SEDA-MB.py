#!/usr/bin/env python
import pika
import requests
import json
import base64
import psycopg2

HOST = "ec2-52-200-189-81.compute-1.amazonaws.com"

credentials = pika.PlainCredentials('signals', 'insecure')
parameters = pika.ConnectionParameters(HOST, 5672, 'vhost', credentials)


def callback(ch, method, properties, body):
    print("Creating a signal in MB ....")
    print(json.loads(body)['signals'])
    print("-----------------------------------------------------")

    data = json.loads(body)['signals']
    url = data.pop('image_url', None)
    if not url:
        url = f'http://{HOST}:8000/signals/media/attachments/2020/10/18/nophoto.jpg'

    response = requests.get(url)
    uri = "data:" + response.headers['Content-Type'] + ";" + "base64," + str(base64.b64encode(response.content).decode("utf-8"))
    data["issue_image"] = [uri]
    # print(data)

    category_data = {
        "category": data['category'] if data['category'] != '' or data['category'] != 'Other' or data['category'] != None else '',
        "sub_category": data['sub_category'] if data['sub_category'] != '' or data['sub_category'] != 'Other' or data['sub_category'] != None else '',
        "sub_category1": data['sub_category1'] if data['sub_category1'] != '' or data['sub_category1'] != 'Other' or data['sub_category1'] != None else '',
        "sub_category2": data['sub_category2'] if data['sub_category2'] != '' or data['sub_category2'] != 'Other' or data['sub_category2'] != None else ''
    }

    print("Category Data : ", category_data)

    res = requests.post('https://admindev.haagsebeheerder.nl/index.php/api/get_category_api', json=category_data)
    print("Category Route : ", res.status_code)

    if res.status_code == 201:
        data["category_id"] = res.json()["category_data"]["value"] if "category_data" in res.json() else ""
        data["sub_category_id"] = res.json()["sub_category_data"]["value"] if "sub_category_data" in res.json() else ""
        data["sub_category1_id"] = res.json()["sub_category_data1"]["value"] if "sub_category_data1" in res.json() else ""
        data["sub_category2_id"] = res.json()["sub_category_data2"]["value"] if "sub_category_data2" in res.json() else ""


    response = requests.post("https://admindev.haagsebeheerder.nl/index.php/api/submit_mor_api", json=data)
    print(response.status_code)
    # print(response.json())
    if response.status_code == 201:
        print("Created.....")

    print("\n")


connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='SEDA-MB', durable=True)
channel.basic_consume(queue='SEDA-MB', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

