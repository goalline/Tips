import requests
import json
from datetime import datetime
import pytz
import tzlocal
import numpy

#additional function
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
        return str("-") + " - " + str("-")

def average_score_last5(id_match):


    home_score = median_goal(get_team_id(id_match).get("home")).get("goal")
    away_score = median_goal(get_team_id(id_match).get("away")).get("goal")

    home_skip = median_goal(get_team_id(id_match).get("home")).get("concead")
    away_skip = median_goal(get_team_id(id_match).get("away")).get("concead")

    print(home_score)

    return str(home_score) + " - " + str(away_score) +"----"+str(home_skip) + " - " + str(away_skip)

def prediction_bid(id_match):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

    querystring = {"fixture": str(id_match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_match = json.loads(response.content)

    result = json_match["response"][0]["predictions"]["advice"]

    return result

def goal_more_1_5(id_match):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

    querystring = {"fixture": str(id_match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_match = json.loads(response.content)

    home_score = json_match["response"][0]["teams"]["home"]["last_5"]["goals"]["for"]["average"]
    away_score = json_match["response"][0]["teams"]["away"]["last_5"]["goals"]["for"]["average"]

    home_skip = json_match["response"][0]["teams"]["home"]["last_5"]["goals"]["against"]["average"]
    away_skip = json_match["response"][0]["teams"]["away"]["last_5"]["goals"]["against"]["average"]

    if float(home_score) > 1.5 or float(away_score) > 1.5:
        if float(home_skip) >= 1.5 or float(away_skip) >= 1.5:
            return 1
        else:
            return 0
    else:
        return 0

def goal_more_1_5_ver2(id_match):

    matches = get_team_id(id_match=id_match)

    team_home = median_goal(matches.get("home"))
    team_away = median_goal(matches.get("away"))

    if float(team_home.get("goal")) >= 1.5 and float(team_away.get("goal")) >= 1.5:
        if float(team_home.get("concead")) >= 1.5 or float(team_away.get("concead")) >= 1.5:
            return 1
        else:
            return 0
    else:
        return 0
    return 0

def goal_less_1_5(id_match):
    url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

    querystring = {"fixture": str(id_match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_match = json.loads(response.content)

    home_score = json_match["response"][0]["teams"]["home"]["last_5"]["goals"]["for"]["average"]
    away_score = json_match["response"][0]["teams"]["away"]["last_5"]["goals"]["for"]["average"]

    home_skip = json_match["response"][0]["teams"]["home"]["last_5"]["goals"]["against"]["average"]
    away_skip = json_match["response"][0]["teams"]["away"]["last_5"]["goals"]["against"]["average"]

    if float(home_score) < 1.5 and float(away_score) < 1.5:
        if float(home_skip) < 1.5 and float(away_skip) < 1.5:
            return 1
        else:
            return 0
    else:
        return 0

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

def goal_time(id_match):
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"id": str(id_match)}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_match = json.loads(response.content)

    match_events = json_match["response"][0]["events"]
    score=[]
    for x in range(0, len(match_events)):
        if match_events[x]["type"]=="Goal" and (match_events[x]["detail"]=="Normal Goal" or match_events[x]["detail"]=="Penalty"):
           score.append(match_events[x]["time"]["elapsed"])

    return score

def h2h(id_match):

        url = "https://api-football-v1.p.rapidapi.com/v3/predictions"

        querystring = {"fixture": str(id_match)}

        headers = {
            'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_match = json.loads(response.content)

        result = json_match["response"][0]["h2h"]

        arr_score=[]

        for x in range(0,len(result)):

            try:

                if float(result[x]["goals"]["home"])>0 or float(result[x]["goals"]["away"])>0:

                        score=float(result[x]["goals"]["home"])+float(result[x]["goals"]["away"])

                        arr_score.append(score)

            except:

                arr_score.append(0)

        if len(arr_score)>=1:

            return numpy.median(arr_score)

        else:

            return 0

def median_goal(team):

    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"team": str(team), "last": "5"}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_team = json.loads(response.content)

    json_team=json_team["response"]
    arr_goals=[]
    arr_concead=[]
    dict_goals={}

    for x in range(0, len(json_team)):

        if type(json_team[x]["goals"]["home"]) == int:

            if json_team[x]["teams"]["home"]["id"] == team:
                arr_goals.append(json_team[x]["goals"]["home"])

            if json_team[x]["teams"]["away"]["id"] == team:
                arr_goals.append(json_team[x]["goals"]["away"])

            if json_team[x]["teams"]["home"]["id"] != team:
                arr_concead.append(json_team[x]["goals"]["home"])

            if json_team[x]["teams"]["away"]["id"] != team:
                arr_concead.append(json_team[x]["goals"]["away"])


    dict_goals={"goal":numpy.median(arr_goals),"concead":numpy.median(arr_concead)}

    return dict_goals

def get_team_id(id_match):
    try:
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

        querystring = {"id": str(id_match)}

        headers = {
            'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_match = json.loads(response.content)

        home = json_match["response"][0]["teams"]["home"]["id"]
        away = json_match["response"][0]["teams"]["away"]["id"]
        dic_id_teams={"home":home,"away":away}
        return dic_id_teams
    except SyntaxError:
        return str("-") + " - " + str("-")

#main function
def from_betting():
    for y in range(1,100):
        url = "https://api-football-v1.p.rapidapi.com/v3/odds"

        querystring = {"date":"2021-07-25","page":str(y),"bet":"2"}

        headers = {
            'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
            'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        json_betting = json.loads(response.content)

        for x in range(0,9):
            try:
                home = json_betting["response"][x]["bookmakers"][0]["bets"][0]["values"]
                id_fixture= json_betting["response"][x]["fixture"]["id"]
                if goal_more_1_5(id_fixture) > 0:
                    print(str(home)+"-"+ str(id_fixture)+" - " + str(get_time_match(id_fixture)) +" - " + name_matches(id_fixture)+ " - "+average_score_last5(id_fixture)+" - "+str(goal_time(id_fixture)))
            except UnicodeEncodeError:
                print("error")

def from_fixture():
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"

    querystring = {"date": "2021-07-30"}

    headers = {
        'x-rapidapi-key': "7b3a1604c1msh29e37f4ff094a22p190becjsn363c36fc7ada",
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    json_fixture = json.loads(response.content)

    for x in range(0,len(json_fixture["response"])):

        id_fixture = json_fixture["response"][x]["fixture"]["id"]

        date = json_fixture["response"][x]["fixture"]["date"]

        competitors = name_matches(id_fixture)

        try:
            if goal_more_1_5_ver2(id_fixture)>0:
                print(h2h(id_fixture))
                print(id_fixture)
                print(str(get_time_match(id_fixture))+ " -- "+competitors + " -- "+ str(goal_time(id_fixture))+ " -- "+ str(average_score_last5(id_fixture)))
                #print("------------------------------------------------------------------------------------------------")
        except:
            print("Error"+competitors)
            continue


from_fixture()