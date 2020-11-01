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
from urllib.parse import urlparse 
from os.path import splitext
import uuid
import base64
import strgen
import string
import random 
import urllib.request as urllib


tz = pytz.timezone("Europe/Amsterdam")
last_executed_datetime = datetime.datetime.now(tz=tz)


def filter_category(cat):
    cat = cat.lstrip()
    filter_cat = []

    # Case 1: When there is a backslash between category name
    if '/' in cat:
        for cat_split in cat.split('/'):
            cat_split = cat_split.lstrip()
            if not cat_split.isupper():
            	cat_split = cat_split.capitalize()
            
            filter_cat.append(cat_split)

        return '-'.join(filter_cat)


    # Case 3: When there is already a hyphen in name ex. Bouw- en sloopafval
    elif '-' in cat:
    	return cat


    # Case 2: When there is a space between category names 
    else:
        for cat_split in cat.split(' '):
            cat_split = cat_split.lstrip()
            if not cat_split.isupper():
            	cat_split = cat_split.capitalize()
            
            filter_cat.append(cat_split)

        return ' '.join(filter_cat)



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

    payload = {'startDate': startDate  , 'endDate': endDate}


    try:
        api = 'https://admindev.haagsebeheerder.nl/index.php/api/cronapifac' 
        response = requests.get(api, json=payload)                       # api to capture the new reports in MB
        print("New report api : ", response.status_code)
        print("Objects : ", len(response.json()["data"]))

        objects = response.json()["data"]

        for obj in objects:
            print("MB Id : ", obj["_id"])
            cat1 = filter_category(obj["category"])
            cat2 = filter_category(obj["sub_category"])
            cat3 = filter_category(obj["sub_category1"])
            cat4 = filter_category(obj["sub_category2"])

            # if obj["category"] != '':
            #     cat = obj["category"]
            #     category_url = f"http://52.200.189.81:8000/signals/v1/public/terms/categories/{cat}"

            #     if obj["sub_category"] != '':
            #         cat2 = obj["sub_category"]
            #         category_url += "/" + f"{cat2}"

            #         if obj["sub_category1"] != '':
            #             cat3 = obj["sub_category1"]
            #             category_url += "/" + f"{cat3}"

            #             if obj["sub_category2"] != '':
            #                 cat4 = obj["sub_category2"]
            #                 category_url += "/" + f"{cat4}"

            if cat4:
                category_url = f"http://52.200.189.81:8000/signals/v1/public/terms/categories/{cat1}/{cat2}/{cat3}/{cat4}"      # get the category
            else:
                category_url = f"http://52.200.189.81:8000/signals/v1/public/terms/categories/{cat1}/{cat2}/{cat3}"             # get the category


            cat_res = requests.get(category_url)
            # print("Category Url : ", category_url)

            if cat_res.status_code == 200:
                print("Category Url : ", category_url)

            else:
                print("Category Not Found !!")
                print("Category Url : ", category_url)
                category_url = "http://52.200.189.81:8000/signals/v1/public/terms/categories/Other/Other/Other"


            # generate a location object  
            huisnummer = obj["huisnummer"] if "huisnummer" in obj else ''
            postcode = obj["postcode"] if "postcode" in obj else ''
            woonplaats = obj["woonplaats"] if "woonplaats" in obj else ''
            openbare_ruimte = huisnummer+ ' '  + postcode + ' ' +  woonplaats


            # get stadsdeel from postcode
            print("Postcode : ", postcode) 
            res_stadsdeel = requests.get(f'http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/v1/private/get_stadsdeel/{postcode}')
            print("Stadsdeel api response code : ", res_stadsdeel.status_code)
           
            if res_stadsdeel.status_code == 200:
                stadsdeel = res_stadsdeel.json()["stadsdeel"]["name"]
            else:
                stadsdeel = "Centrum"

            print("Stadsdeel : ", stadsdeel)
            coordinates = [obj["coordinates"][1], obj["coordinates"][0]]

            location = {
                        "geometrie": {"type":"Point","coordinates": coordinates},
                        "address"  : {"openbare_ruimte":openbare_ruimte, "huisnummer":huisnummer, "postcode":postcode, "woonplaats": woonplaats}, 
                        "stadsdeel": stadsdeel
                    }


            # creating a new report from MB to SEDA 
            payload = {
                "location": location,
                "category": {"category_url": category_url},
                "reporter": {"phone": obj["reported_by_data"][0]["mobile"], "email": obj["reported_by_data"][0]["email_id"], "sharing_allowed": True},
                "incident_date_start": str(datetime.datetime.now(tz=tz)),
                "text": obj["description"],
                "source": "MB",
                "updated_by": "MB"
            }

            response = requests.post('http://ec2-52-200-189-81.compute-1.amazonaws.com:8000/signals/v1/public/signals/', json=payload)
            print("Signal Created : ", response.status_code)
            if response.status_code != 201:
                print(response.json())
            
            if response.status_code == 201:
                print("Signals Created in SEDA -- ")

                if obj["issue_image"]:
                    url = obj["issue_image"]
                    path = urlparse(url).path
                    ext = splitext(path)[1]
                    # print("Ext : ", ext)

                    img = urllib.urlopen(url)
                    imgHeaders = img.headers
                    # print(imgHeaders)

                    name = str(uuid.uuid4()) + ext
                    seda_id = response.json()["signal_id"]
                    files = {'file': (name, img.read(), img.headers["Content-Type"])}
                    res = requests.post(f'http://52.200.189.81:8000/signals/v1/public/signals/{seda_id}/attachments', files=files)
                    print("Image : ", res.status_code)


                data = {
                    "seda_signal_id": response.json()["signal_id"],
                    "mb_signal_id": obj["_id"]
                }

                seda_id = response.json()["signal_id"]
                response = requests.post(f'http://52.200.189.81:8000/signals/v1/public/idmapping/', data=data)
                print("MB report id status : ", response.status_code)
                # print(response.json())
    
    except Exception as error:
        print("Error : ", error)



    last_executed_datetime = now
    print("---------------------------------------------------")
    print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")




print("  [*] Waiting for some change in Facilitator. To exit press CTRL+C")
schedule.every(1).minutes.do(checkFacilitatorChange)
while True:
    schedule.run_pending()
    time.sleep(1)



