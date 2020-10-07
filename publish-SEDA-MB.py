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
import pytz

tz = pytz.timezone("Europe/Amsterdam")
last_executed_datetime = datetime.datetime.now(tz=tz)
HOST = "ec2-52-200-189-81.compute-1.amazonaws.com"
PORT = 5432


def publish():
    global last_executed_datetime
    current = datetime.datetime.now(tz=tz)
    print("Last time : ", last_executed_datetime)
    print("Current Time : ", current)

    connection = False
    try:
        connection = psycopg2.connect(user='signals', password='insecure', host=HOST, port=PORT, database="signals")
        cursor = connection.cursor(cursor_factory = psycopg2.extras.NamedTupleCursor)
        data = {"signals": {}}
        signal_data = data["signals"]

        # ? Fetching a Signal from PostgreSQL
        cursor.execute(sql.SQL('SELECT * FROM signals_signal WHERE created_at BETWEEN (%s) AND (%s) AND source != (%s) '), [last_executed_datetime, current, "MB"])
        signals = cursor.fetchall()

        for signal in signals:
            # print(signal)
            # ? Fetching Category, Department from PostgreSQL
            categoryassignment_id = signal.category_assignment_id
            postgreSQL_select_Query = f"Select * from signals_categoryassignment where id={categoryassignment_id}"
            cursor.execute(postgreSQL_select_Query)
            categoryassignment = cursor.fetchone()
            #  print(categoryassignment)
            category_id = categoryassignment.category_id
            postgreSQL_select_Query = f"Select * from signals_categorydepartment where category_id={category_id}"
            cursor.execute(postgreSQL_select_Query)
            categorydepartment = cursor.fetchone()
            # print(categorydepartment)
            department_id = categorydepartment.department_id
            postgreSQL_select_Query = f"Select * from signals_department where id={department_id}"
            cursor.execute(postgreSQL_select_Query)
            department = cursor.fetchone()
            # print(department)

            # ? Fetching Location from PostgreSQL
            location_id = signal.location_id
            postgreSQL_select_Query = f"Select * from signals_location where id={location_id}"
            cursor.execute(postgreSQL_select_Query)
            location = cursor.fetchone()
            coordinates = [location.geometrie[0], location.geometrie[1]]

            # ? Fetching image from PostgreSQL
            postgreSQL_select_Query = f"Select * from signals_attachment where _signal_id={signal.id}"
            cursor.execute(postgreSQL_select_Query)
            attachment = cursor.fetchone()
            if attachment and attachment.file:
                url = f'http://{HOST}:8000/signals/media/' + attachment.file
            else:
                url = ''

            # ? Check for APP routing ----
            if department.app == "MB":
                signal_data["seda_id"] = signal.signal_id
                signal_data["image_url"] = url
                signal_data["address"] = location.address_text
                signal_data["category"] = "Afval"
                signal_data["sub_category"] = "Afvalbakken"
                signal_data["sub_category1"] = ""
                signal_data["sub_category2"] = ""
                signal_data["category_id"] = "5d8f1da6decf62a41c00002d"
                signal_data["description"] = signal.text
                signal_data["sub_category_id"] = ""
                signal_data["sub_category1_id"] = ""
                signal_data["sub_category2_id"] = ""
                signal_data["location"] = ["", ""]
                signal_data["user_id"] = "5dacb94417a8dc7e657b23c7"
                signal_data["source"] = "seda"

                connect_rabbitmq_MB(data)


            elif department.app == "FC":
                signal_data["sedaId"] = signal.signal_id
                signal_data["source"] = "Seda"
                signal_data["team_id"] = 0
                signal_data["tool_id"] = "5c5aada3b068ca4411000029"
                signal_data["locations"] = '52.08119905078634&4.2853899827481134'
                signal_data["report_type"] = "1,2,3"
                signal_data["used_map_type"] = "2",
                signal_data["language"] = "1"
                signal_data["description"] = signal.text
                signal_data["location_type"] = "1"
                signal_data["map_image_name"] = ""
                signal_data["url"] = url

                connect_rabbitmq_FC(data)


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()

    last_executed_datetime = current - datetime.timedelta(microseconds=1)
    print("---------------------------------------------------")
    print("  [*] Waiting for new signals. To exit press CTRL+C")



# Function to publish data to rabbitmq
def connect_rabbitmq_MB(data):
    print("Data Published : ", data)
    credentials = pika.PlainCredentials('signals', 'insecure')
    parameters = pika.ConnectionParameters(HOST, 5672, 'vhost', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue='SEDA-MB', durable=True)
    channel.basic_publish(exchange='SEDA-MB-exchange', routing_key='hello1', body=json.dumps(data, indent=4, sort_keys=True, default=str))

    print("Data is successfully published to MB queue !!")
    connection.close()



# Function to publish data to rabbitmq
def connect_rabbitmq_FC(data):
    print("Data Published : ", data)
    try:
        credentials = pika.PlainCredentials('signals', 'insecure')
        parameters = pika.ConnectionParameters(HOST, 5672, 'vhost', credentials)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue='SEDA-FC', durable=True)
        channel.basic_publish(exchange='SEDA-FC-exchange', routing_key='hello', body=json.dumps(data, indent=4, sort_keys=True, default=str))

        print("Data is successfully published to FC queue !!")
        connection.close()

    except:
        print("ERROR occured in rabbitmq ... !!!! ")


print("  [*] Waiting for new signals. To exit press CTRL+C")
schedule.every(2).minutes.do(publish)
while True:
    schedule.run_pending()
    time.sleep(1)

