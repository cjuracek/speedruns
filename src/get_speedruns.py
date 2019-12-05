from bs4 import BeautifulSoup
import requests
import json

url = "https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1"
r = requests.get(url)
game_info = json.loads(r.text)
wr_date = game_info.get("data").get("runs")[0].get("run").get("date")