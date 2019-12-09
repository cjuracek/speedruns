from datetime import datetime, timedelta
import requests
import json


game_categories = {"sm64": "120_Star",
                   "smo": "Any",
                   "sms": "120_Shines",
                   "smb1": "Any",
                   "botw": "Any"}

game_names = {"sm64": "Super Mario 64",
              "smo": "Super Mario Odyssey",
              "sms": "Super Mario Sunshine",
              "smb1": "Super Mario Bros.",
              "botw": "Breath of the Wild"}

def is_new_wr(wr_date):
    past = datetime.today() - timedelta(weeks=1)
    return wr_date > past


def get_wr_date(json):
    return json.get("data").get("runs")[0].get("run").get("date")


if __name__ == '__main__':

    # Example URL: "https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1"
    base_url = "https://www.speedrun.com/api/v1/leaderboards/"
    for game, category in game_categories.items():
        url = f'{base_url}{game}/category/{category}?top=1'
        r = requests.get(url)
        game_info = json.loads(r.text)
        wr_date_str = get_wr_date(game_info)
        wr_date = datetime.strptime(wr_date_str, '%Y-%m-%d')

        if is_new_wr(wr_date):
            print(f'NEW WORLD RECORD FOR {game} ON {wr_date_str}')
        else:
            time_diff = datetime.today() - wr_date
            print(f'{game_names.get(game)}: {category} No new world records since {wr_date_str} ({time_diff.days} Days)')
