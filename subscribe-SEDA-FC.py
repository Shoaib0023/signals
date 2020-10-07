#!/usr/bin/env python
#!/usr/bin/env python
import pika
import requests
import json
import base64
import psycopg2
from urllib.request import urlopen
from urllib.parse import urlparse
from os.path import splitext
import uuid

HOST = "ec2-52-200-189-81.compute-1.amazonaws.com"
credentials = pika.PlainCredentials('signals', 'insecure')
parameters = pika.ConnectionParameters(HOST, 5672, 'vhost', credentials)


def callback(ch, method, properties, body):
    print("Creating a report in Facilitator ....")
    data = json.loads(body)['signals']
    url = data.pop('url', None)
    img_present = False

    if url:
        img_present = True
        img = urlopen(url)
        path = urlparse(url).path
        # print("Path : ", path)
        ext = splitext(path)[1]
        # print("Ext : ", ext)
        print(img.headers)
        name = str(uuid.uuid4()) + ext
        # files = [
        #     ('report_pic', img.read())
        # ]
        files = {'report_pic': (name, img.read(), "multipart/form-data")}

    api = 'http://facilitator.dev.mcc.kpnappfactory.nl/index.php/apinewchanges/submit_report/'
    headers = {"Authorization": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiIsIl9pZCI6IjVjZDI4M2JmMmI5MDRmNTUyYmIwMGJkNiIsImRldmljZSI6IkFuZHJvaWQiLCJ0b2tlbiI6ImNKS3lDajRtRjNjOkFQQTkxYkVNeDlEcVFDSFZ0NV90MV9oUUc0N204UE9HU1BlT3oxZ05JSlRMR3hyTzJOSWZCTWpUVENHejQ3ZmVEandLVFlOdW53d0xtX3JMN2psa3ZNZjNxNnNvaFk5V25odThtLUN1WmdUMVlBUzdudHhla2JCVGpKWmNRMUg2ckJ5MHFaMTFsM3pHIiwibGFuZ3VhZ2UiOiIxIn0"}

    try:
        if img_present:
            response = requests.post(api, headers=headers, data=data, files=files)
        else:
            response = requests.post(api, data=data, headers=headers)

        print(response.status_code)
        print(response.text)
        if response.status_code == 201:
            print("Created.....")

    except:
        print("Image is not passed !!!")

    print("\n")


connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='SEDA-FC', durable=True)
channel.basic_consume(queue='SEDA-FC', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

