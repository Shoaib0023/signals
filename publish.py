import psycopg2
from psycopg2 import sql
import psycopg2.extras
import pika
import json
from urllib.request import urlopen
import schedule
import time
import datetime
from decouple import config
import os

# if 'LAST_TIME_EXECUTED' not in os.environ:
#     os.environ['LAST_TIME_EXECUTED'] = datetime.datetime(2020, 9, 11, 0, 0, tzinfo=datetime.timezone.utc)
# else:
#     LAST_TIME_EXECUTED = os.environ.get('LAST_TIME_EXECUTED')
last_executed_datetime = datetime.datetime(2020, 9, 11, 10, 7, 35, 428078, tzinfo=datetime.timezone.utc)

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
            print(signal)
            # return
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
            location_id = signal.location_id
            postgreSQL_select_Query = f"Select * from signals_attachment where _signal_id={signal.id}"
            cursor.execute(postgreSQL_select_Query)
            image = cursor.fetchone()
            # print(images)
            # if image:
            #     image_url = f"http://localhost:8000/signals/media/{image.file}"
            #     image_file = urlopen(image_url).read()
            #     # print(image_file)

            # else:
            #     image_file = ''

            # ? Constructing data format needed for MB to create Signal
            signal_data["description"] = signal.text
            signal_data["category"] = category.category_level_name1
            signal_data["sub_category"] = category.category_level_name2
            signal_data["sub_category1"] = category.category_level_name3
            signal_data["sub_category2"] = category.category_level_name4
            # signal_data["user_id"] = signal.text
            signal_data["address"] = location.address_text
            signal_data["is_edit"] = "true"
            signal_data["locations"] = coordinates
            signal_data["report_type"] = "SEDA"
            signal_data["language"] = "1"
            signal_data["issue_image"] = ''

            connectRabbitMQ(data)


    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)

    finally:
        if(connection):
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

    print("---------------------------------------------------")
    print("  [*] Waiting for new signals. To exit press CTRL+C")
    return

# Function to publish data to rabbitmq
def connectRabbitMQ(data={}):
    # print("RabbitMq called : ", data)
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
schedule.every(1).minutes.do(connect)
while True:
    schedule.run_pending()
    time.sleep(1)

