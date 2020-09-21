import psycopg2
from psycopg2 import sql
import psycopg2.extras
import pika
import json
from urllib.request import urlopen
import schedule
import time
import datetime
import os
import base64
import requests

last_executed_datetime = datetime.datetime(2020, 9, 17, 8, 15, 3, 358496, tzinfo=datetime.timezone.utc)

def connect():
    try:
        global last_executed_datetime
        print("Last time : ", last_executed_datetime)
        connection = psycopg2.connect(user='signals', password='insecure', host="ec2-52-200-189-81.compute-1.amazonaws.com", port=5432, database="signals")
        cursor = connection.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
        data = {"signals": {}}
        signal_data = data["signals"]

        # ? Fetching a Signal from PostgreSQL
        current = datetime.datetime.now(datetime.timezone.utc)
        print("Current Time : ", current)
        cursor.execute(sql.SQL('SELECT * FROM signals_signal WHERE created_at BETWEEN (%s) AND (%s)'), [last_executed_datetime, current])
        signals = cursor.fetchall()
        last_executed_datetime = current - datetime.timedelta(microseconds=1)
        for signal in signals:
            # print(signal)
            # ? Fetching a Category from PostgreSQL
            categoryassignment_id = signal.category_assignment_id
            postgreSQL_select_Query = f"Select * from signals_categoryassignment where id={categoryassignment_id}"
            cursor.execute(postgreSQL_select_Query)
            categoryassignment = cursor.fetchone()
            # print(categoryassignment)
            category_id = categoryassignment.category_id
            postgreSQL_select_Query = f"Select * from signals_category where id={category_id}"
            cursor.execute(postgreSQL_select_Query)
            category = cursor.fetchone()
            # print(category)


            # ? Fetching a Location from PostgreSQL
            location_id = signal.location_id
            postgreSQL_select_Query = f"Select * from signals_location where id={location_id}"
            cursor.execute(postgreSQL_select_Query)
            location = cursor.fetchone()
            coordinates = [location.geometrie[0], location.geometrie[1]]
            # print(location.address_text)

            # ? Fetching image from PostgreSQL
            postgreSQL_select_Query = f"Select * from signals_attachment where _signal_id={signal.id}"
            cursor.execute(postgreSQL_select_Query)
            attachment = cursor.fetchone()
            if attachment and attachment.file:
                url = 'http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/media/' + attachment.file
            else:
                url = ' '

            # ? Constructing data format needed for MB to create Signal
            signal_data["image_url"] = url
            signal_data["address"] = location.address_text
            signal_data["category"] = "Afval"
            signal_data["sub_category"] = ""
            signal_data["sub_category1"] = ""
            signal_data["sub_category2"] = ""
            signal_data["category_id"] = "5d8f1da6decf62a41c00002d"
            signal_data["description"] = signal.text
            signal_data["sub_category_id"] = ""
            signal_data["sub_category1_id"] = ""
            signal_data["sub_category2_id"] = ""
            signal_data["location"] = ["", ""]
            signal_data["user_id"] = "5dacb94417a8dc7e657b23c7"

            connectRabbitMQ(data)


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()

    print("---------------------------------------------------")
    print("  [*] Waiting for new signals. To exit press CTRL+C")
    return

# Function to publish data to rabbitmq
def connectRabbitMQ(data):
    print("Data Published : ", data)
    credentials = pika.PlainCredentials('signals', 'insecure')
    parameters = pika.ConnectionParameters('localhost', 5672, 'vhost', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='SEDA-MB', durable=True)
    channel.basic_publish(exchange='SEDA-MB-exchange', routing_key='hello', body=json.dumps(data, indent=4, sort_keys=True, default=str))

    # print("SEND: ", data)
    print("Data is successfully published to the queue !!")
    connection.close()

# connect()
print("  [*] Waiting for new signals. To exit press CTRL+C")
schedule.every(2).minutes.do(connect)
while True:
    schedule.run_pending()
    time.sleep(1)

