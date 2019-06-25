import pandas as pd
import requests
from bs4 import BeautifulSoup

import datetime
right_now = datetime.datetime.now()
date_string = right_now.strftime("%Y-%m-%d-%-I%p")

# specify top-secret API keys
from dotenv import load_dotenv
load_dotenv()
import os

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")

response = requests.get('https://www.politico.com')
doc = BeautifulSoup(response.text)

headlines = doc.find_all(class_='headline')
rows = []
message = ""
for headline in headlines:
    row = {}
    try:
        if "{" not in headline.text.strip():
            row['Headline'] = headline.text.strip()
            message += ('\n' + headline.text.strip()+'\n')
    except:
        pass
    try:
        if "{" not in headline.text.strip():
            row['URL'] = headline.find('a')['href']
            message += "Link: " + (headline.find('a')['href']+'\n')
    except:
        row['URL'] = headline.parent.parent.parent['href']
        message += "Link: " + (headline.parent.parent.parent['href']) + '\n'
    authors = headline.parent.find_all(class_='vcard')
    if len(authors) > 0:
        row['Byline'] = " and ".join([author.text.strip() for author in authors])
        message += "By: " + " and ".join([author.text.strip() for author in authors]) + '\n'
    else:
        pass
    try:
        row['Sub_header'] = headline.parent.find(class_='tease').text.strip()
        message += "Quick summary: " + headline.parent.find(class_='tease').text.strip() + '\n'
    except:
        pass
    rows.append(row)
    message += "\n------\n"
df = pd.DataFrame(rows[:-1]) # last isn't actually article
df.to_csv('briefing-'+date_string+'.csv',index=False)

time = right_now.strftime("%-I%p")
subject = f"Here is your {time} briefing from Politico"

response = requests.post(
        "https://api.mailgun.net/v3/sandbox4591da35f7e9429989169172d04cb10d.mailgun.org/messages",
        auth=("api", MAILGUN_API_KEY),
        files=[("attachment", open("briefing-"+date_string+".csv"))],
        data={"from": "Excited User <mailgun@sandbox4591da35f7e9429989169172d04cb10d.mailgun.org>",
              "to": ["aseem.a.shukla@gmail.com"],
              "subject": subject,
              "text": message}) 