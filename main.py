import requests
import json
import pandas
from datetime import datetime
import pytz
import tzlocal

def get_score_result(match):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"id": str(match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_response_predict = json.loads(response.content)

    home_score = json_response_predict["response"][0]["goals"]["home"]
    away_score = json_response_predict["response"][0]["goals"]["away"]

    return str(home_score) + " - " + str(away_score)

def get_time_match(match):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"id": str(match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_response_predict = json.loads(response.content)

    time_match = json_response_predict["response"][0]["fixture"]["date"]

    local_timezone = tzlocal.get_localzone()
    utc_time = datetime.strptime(time_match[0:19], "%Y-%m-%dT%H:%M:%S")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time

url = "https://api-football-v1.p.rapidapi.com/v2/fixtures/date/2021-07-21"

querystring = {"timezone": "Europe/London"}

headers = {
    'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

json_response = json.loads(response.content)

fixtures_id = []

for x in json_response["api"]["fixtures"]:
    fixtures_id.append(str(x["fixture_id"]))

url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

headers = {
    'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
    'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
}

num = 0

for x in fixtures_id:
    try:
        querystring = {"fixture": "" + str(x)}
        response_predict = requests.request("GET", url, headers=headers, params=querystring)
        json_response_predict = json.loads(response_predict.content)
        if float(json_response_predict["response"][0]["predictions"]["under_over"])>1:
            print(x)
            print(str(json_response_predict["response"][0]["teams"]["home"]["name"]) + " - "
                  + str( json_response_predict["response"][0]["teams"]["away"]["name"])+ " - " + str(get_time_match(x))
                        + " - " + str( json_response_predict["response"][0]["predictions"]["under_over"])
                            + " - " + get_score_result(x))
    except:
        continue