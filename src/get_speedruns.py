from datetime import datetime, timedelta
import requests
import json

def is_world_record(date):
    wr = datetime.strptime(date, '%Y-%m-%d')
    past = datetime.today() - timedelta(weeks=1)
    return(wr > past)

games = {"sm64": "wkpoo02r",
         "smo": "w20w1lzd",
         "sms": "n2y3r8do"}#, "z27o9gd0"}

# Example URL: "https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1"
base_url = "https://www.speedrun.com/api/v1/leaderboards/"
for k, v in games.items():
    url = f'{base_url}{k}/category/{v}?top=1'
    r = requests.get(url)
    game_info = json.loads(r.text)
    wr_date = game_info.get("data").get("runs")[0].get("run").get("date")

    if is_world_record(wr_date):
        print("NEW WORLD RECORD FOR" + k)
    else:
        print("No new world records for " + k)
