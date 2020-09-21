import pika
import json
from pymongo import MongoClient
# from bson import ObjectId
# import dateutil.parser
import datetime
import requests
from bson.objectid import ObjectId
import pytz
import schedule
import time

tz = pytz.timezone("Europe/Amsterdam")
last_executed_datetime = datetime.datetime(2020, 9, 17, 8, 51, 36, 812056, tzinfo=tz)

# Function to publish data to rabbitmq
def connectRabbitMQ(data):
    credentials = pika.PlainCredentials('signals', 'insecure')
    parameters = pika.ConnectionParameters('localhost', 5672, 'vhost', credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hello1', durable=True)

    channel.basic_publish(exchange='hello-exchange', routing_key='hello', body=json.dumps(data, indent=4, sort_keys=True, default=str))

    print("Success: Data is published to queue", len(data["reports"]))
    connection.close()


# Function to connect to MongoDB
def connect():
    global last_executed_datetime
    client = MongoClient("mongodb://localhost:8001/facilitator")
    db = client["facilitator"]
    data = {"reports": [], "users": [], "category": {}, "signals_plan": []}

    now = datetime.datetime.now(tz=pytz.timezone("Europe/Amsterdam"))
    print(last_executed_datetime)
    print(now)
    for document in db.reports.find({ "$and": [{"created_at": { "$lt": now, "$gte": last_executed_datetime}},
                                               {"status": 3}]}):
        # print(document)
        created_at = document["created_at"]
        # print(created_at)
        data["reports"].append(document)

    for document in db.reports.find({ "$and": [{"updated_at": { "$lt": now, "$gte": last_executed_datetime}},
                                               {"status": 3}]}):
        # print(document)
        created_at = document["created_at"]
        # print(created_at)
        data["reports"].append(document)

    last_executed_datetime = now - datetime.timedelta(microseconds=1)
    connectRabbitMQ(data)

# connectMongo()

print("  [*] Waiting for new signals. To exit press CTRL+C")
schedule.every(1).minutes.do(connect)
while True:
    schedule.run_pending()
    time.sleep(1)

