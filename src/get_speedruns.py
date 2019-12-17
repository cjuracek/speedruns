import string
from datetime import datetime, timedelta
import requests
import json
import time
import smtplib, ssl


game_categories = {'Super Mario 64': ['120_Star', '70_Star', '16_Star', '1_Star', '0_Star'],
                   'Super Mario Odyssey': ['Any'],
                   'Super Mario Sunshine': ['120_Shines', 'Any'],
                   'Super Mario Bros.': ['Any', 'Warpless'],
                   'The Legend of Zelda: Breath of the Wild': ['Any'],
                   'Super Monkey Ball': ['Expert'],
                   'Super Monkey Ball 2': ['Story_Mode'],
                   'The Legend of Zelda: The Wind Waker HD': ['Any'],
                   'The Legend of Zelda: Ocarina of Time': ['Any'],
                   'Celeste': ['Any'],
                   'Super Mario Bros. 3': ['100'],
                   'Castlevania (NES)': ['Any'],
                   'Super Meat Boy': ['Any']}


def is_new_wr(wr_date):
    past = datetime.today() - timedelta(weeks=1)
    return wr_date > past


def get_wr_date(json):
    return json.get('data').get('runs')[0].get('run').get('date')


def get_full_game_name(abbreviation):
    url = f"https://www.speedrun.com/api/v1/games/{abbreviation}"
    r = requests.get(url)
    game_info = json.loads(r.text)
    game_id = game_info.get('data')[0].get('id')
    return game_id

def get_game_id(game_name):
    game_name_url = game_name.replace(" ", "%20")
    url = f"https://www.speedrun.com/api/v1/games?name={game_name_url}"
    r = requests.get(url)
    game_info = json.loads(r.text)
    game_id = game_info.get('data')[0].get('id')
    return game_id


if __name__ == '__main__':

    # Example URL: 'https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1'
    base_url = 'https://www.speedrun.com/api/v1/leaderboards/'
    all_wr_info = []
    for game, categories in game_categories.items():
        game_id = get_game_id(game)
        for category in categories:
            url = f'{base_url}{game_id}/category/{category}?top=1'
            r = requests.get(url)
            wr_info = json.loads(r.text)
            wr_date_str = get_wr_date(wr_info)
            wr_date = datetime.strptime(wr_date_str, '%Y-%m-%d')

            if is_new_wr(wr_date):
                wr_message = f'NEW WORLD RECORD FOR {game} ON {wr_date_str}'
                all_wr_info.append(wr_message)
            else:
                time_diff = datetime.today() - wr_date
                wr_message = f'{game}: {category} - No new world records since 'f'{wr_date_str} ({time_diff.days} Days)'
                all_wr_info.append(wr_message)

            time.sleep(1)

    # Send email
    # https://realpython.com/python-send-email/
    port = 465
    password = input('Type your password then press enter: ')

    # Create a secure SSL context
    context = ssl.create_default_context()

    email = 'cjuracektest@gmail.com'
    subject = 'Speed Runs'
    body = '\n'.join(all_wr_info)
    message = f'Subject: {subject} \n\n {body}'
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)