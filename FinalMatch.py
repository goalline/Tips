import requests
import json
from datetime import datetime
import pytz
import tzlocal

url = "https://football-prediction-api.p.rapidapi.com/api/v2/predictions"

querystring = {"market":"classic","iso_date":"2021-07-25","federation":"UEFA"}

headers = {
    'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
    'x-rapidapi-host': "football-prediction-api.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

json_matches = json.loads(response.content)
print(json_matches)
for x in range(0,len(json_matches["data"])):
    home_team = json_matches["data"][x]["home_team"]
    away_team = json_matches["data"][x]["away_team"]
    prediction = json_matches["data"][x]["prediction"]
    status = json_matches["data"][x]["status"]
    start_date = json_matches["data"][x]["start_date"]
    odds = json_matches["data"][x]["odds"][str(prediction)]
    if prediction == "1" or prediction == "2":
        if odds < 1.7:
            print(start_date + " --- " + home_team + " --- " + away_team + " --- " + str(prediction) + " --- " + status+ " --- " +str(odds))
