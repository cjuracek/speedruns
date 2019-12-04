from bs4 import BeautifulSoup
import requests

url = "https://www.speedrun.com/games"
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")