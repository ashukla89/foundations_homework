import pandas as pd
import requests
from bs4 import BeautifulSoup

import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%B %-d, %Y")

# specify top-secret API keys
from dotenv import load_dotenv
load_dotenv()
import os

DARKSKY_API_KEY = os.getenv("DARKSKY_API_KEY")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

url = 'https://api.darksky.net/forecast/'+DARKSKY_API_KEY+'/40.7128,-74.0060'
response = requests.get(url)
data = response.json()

currently = data['currently']
today = data['daily']['data'][0]
temp_feeling = ""
if today['temperatureHigh'] >= 80:
    temp_feeling = "hot"
elif today['temperatureHigh'] >= 65:
    temp_feeling = "pleasant"
elif today['temperatureHigh'] >= 50:
    temp_feeling = "cool"
elif today['temperatureHigh'] >= 32:
    temp_feeling = "cold"
else:
    temp_feeling = "freezing cold"
    
rain_warning = ""
if today['precipProbability'] > 0.3:
    rain_warning = "Bring an Umbrella or rain jacket."
else:
    rain_warning = "Have fun out there!"

subject = f"8AM Weather Forecast: {date_string}."
message = f"Right now it is {currently['temperature']} degrees out and {currently['summary']}. Today will be {temp_feeling} with a high of {today['temperatureHigh']} and a low of {today['temperatureLow']}. {rain_warning}"

response = requests.post(
        "https://api.mailgun.net/v3/sandbox4591da35f7e9429989169172d04cb10d.mailgun.org/messages",
        auth=("api", MAILGUN_API_KEY),
        data={"from": "Excited User <mailgun@sandbox4591da35f7e9429989169172d04cb10d.mailgun.org>",
              "to": ["aseem.a.shukla@gmail.com"],
              "subject": subject,
              "text": message}) 