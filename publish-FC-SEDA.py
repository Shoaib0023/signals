import pika
import json
from pymongo import MongoClient
from urllib.request import urlopen
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

    objects = response.json()["data"]
    for obj in objects:
        # print(obj["plan_time"])
        # print(obj["team_emp_name"])
        seda_id = obj["sedaId"]
        print(seda_id)
        if seda_id == '':
            continue

        res_seda = requests.get(f'http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/v1/public/signals/{seda_id}')
        signal = res_seda.json()

        #? Seda Signal details
        text = signal["text"]
        updates = signal["updates"]
        state = signal["status"]["state"]
        plan_time = signal["plan_time"]
        report_days = signal["report_days"]
        urgency = signal["urgency"]
        forman_emp_name = signal["forman_emp_name"]

        #? Facilitator Report details
        descriptions = obj["description"]
        images = obj["issue_image"]


        #? Checks if report is planned
        if obj["report_status"] == 1:
            if state != 'b':
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
                # print(response.text)
                if response.status_code == 200:
                    print("Report is Planned in Facilitator")


        i = len(updates) + 1
        j = len(descriptions)
 
        while i < j:
            print(i, j)
            new_description = descriptions[i]
            new_image = images[i]

            payload = {
                'signal_id': seda_id,
                'description': new_description
            }

            img_url = 'http://facilitator.dev.mcc.kpnappfactory.nl/uploadimages/reportedIssue/' + new_image
            print("Image Url : ", img_url)
            img = urlopen(img_url)
            files = {'image': img.read()} 
            res = requests.post('http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/v1/public/signal_plan/update/', data=payload, files=files)
            print("Updated : ", res.status_code)
            print(res.text)

            i += 1

        #? Checks if report is closed
        if obj["report_status"] == 2:
            payload = {
                "status": {
                    "state": "o",
                    "state_display": "AFGEHANDELD",
            		"text": "Signal is Closed"
                }
            }

            response = requests.put(f'{seda_api}{seda_id}', json=payload)
            print(response.status_code)
            if response.status_code == 200:
                print("Report is closed in Facilitator")



    last_executed_datetime = now
    print("---------------------------------------------------")
    print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")




print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")
schedule.every(2).minutes.do(checkFacilitatorChange)
while True:
    schedule.run_pending()
    time.sleep(1)

