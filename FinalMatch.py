import requests
import json
from datetime import datetime
import pytz
import tzlocal

def get_id_live_matches(login,token,sport="icehockey"):
    url = "https://spoyer.ru/api/get.php?login="+login+"&token="+token+"&task=livedata&sport="+sport

    response = requests.request("GET", url)

    json_matches = json.loads(response.content)

    arr_id=[]

    for x in json_matches["games_live"]:
        arr_id.append(x['game_id'])

    return arr_id

def get_time_has_passed(login,token,id):
    url = "https://spoyer.ru/api/get.php?login=" + login + "&token=" + token + "&task=eventdata&game_id=" + id

    response = requests.request("GET", url)

    json_match = json.loads(response.content)

    return json_match['results']

def get_matches_today(login,token,sport="icehockey"):
    url = "https://spoyer.ru/api/get.php?login=" + login + "&token=" + token + "&task=predata&sport="+sport+"&day=today"

    response = requests.request("GET", url)

    json_matches = json.loads(response.content)

    arr_id = []
    print((json_matches))
    print(len(json_matches['games_pre']))




odd_pre_match("iclicks","58664-Uw1Jz4CY445b51m")
#get_matches_today("iclicks","58664-Uw1Jz4CY445b51m")
# arr=get_id_live_matches("iclicks","58664-Uw1Jz4CY445b51m")
# print(arr)
# for x in arr:
#     print(get_time_has_passed("iclicks","58664-Uw1Jz4CY445b51m",x))