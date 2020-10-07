import pika
import json
from pymongo import MongoClient
from bson import ObjectId
import dateutil.parser
import schedule
import time
import datetime
import requests
import pytz

tz = pytz.timezone("Europe/Amsterdam")
last_executed_datetime = datetime.datetime.now(tz=tz)


def checkFacilitatorChange():
    global last_executed_datetime

    year = last_executed_datetime.year
    month = last_executed_datetime.month
    day = last_executed_datetime.day
    hour = last_executed_datetime.hour
    minute = last_executed_datetime.minute
    second = last_executed_datetime.second
    startDate = f'{year}-{month}-{day} {hour}:{minute}:{second}'

    now = datetime.datetime.now(tz=tz)
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    second = now.second

    endDate = f'{year}-{month}-{day} {hour}:{minute}:{second}'
    print(startDate)
    print(endDate)

    seda_api = 'http://52.200.189.81:8000/signals/v1/public/signals/'
    api = 'http://facilitator.dev.mcc.kpnappfactory.nl/index.php/apinewchanges/cronapi'

    payload = {'startDate': startDate  , 'endDate': endDate}
    response = requests.post(api, data=payload)
    print(response.status_code)
    print(len(response.json()["data"]))

    seda_arr = {"9a8d6d3f-725f-4c3d-855d-5bb37d386ed3": True}

    objects = response.json()["data"]
    for obj in objects:
        seda_id = obj["sedaId"]
        print(seda_id)

        if seda_id not in seda_arr.keys():
            seda_arr[seda_id] = True
        else:
            continue

        #? Checks if report is closed
        if obj["report_status"] == 2:
            payload = {
                "status": {
                    "state": "o",
                    "state_display": "AFGEHANDELD",
            		"text": "Signal is Closed"
                },
            }

            response = requests.put(f'{seda_api}{seda_id}', json=payload)
            print(response.status_code)
            if response.status_code == 200:
                print("Report is closed ....")

        #? Checks if report is planned
        elif obj["report_status"] == 1:
            payload = {
                "status": {
                    "state": "b",
                    "state_display": "BEHANDELING",
		            "text": "BEHANDELING"
                },
                "report_days": obj["report_days"],
                "plan_time": obj["plan_time"],
                "urgency": obj["urgency"],
                "forman_emp_name": obj["team_emp_name"]
            }

            response = requests.put(f'{seda_api}{seda_id}', json=payload)
            print(response.status_code)
            print(response.text)
            if response.status_code == 200:
                print("Report is Planned .....")


    last_executed_datetime = now
    print("---------------------------------------------------")
    print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")




print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")
schedule.every(2).minutes.do(checkFacilitatorChange)
while True:
    schedule.run_pending()
    time.sleep(1)

