import requests
import json
import pandas
from datetime import datetime
import pytz
import tzlocal


def name_matches(id_match):
    try:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        querystring = {"id": str(id_match)}

        headers = {
            'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_match = json.loads(response.content)

        home_score = json_match["response"][0]["goals"]["home"]
        away_score = json_match["response"][0]["goals"]["away"]

        home_name = json_match["response"][0]["teams"]["home"]["name"]
        away_name = json_match["response"][0]["teams"]["away"]["name"]
        return str(home_name)+ " ("+str(home_score) +") " + " - " + str(away_name)+"("+str(away_score)+")"
    except SyntaxError:
        return str("-") + " - " + str("-")\

