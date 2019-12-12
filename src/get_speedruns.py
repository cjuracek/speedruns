from datetime import datetime, timedelta
import requests
import json
import time
import smtplib, ssl


game_categories = {'sm64': ['120_Star', '70_Star', '16_Star', '1_Star', '0_Star'],
                   'smo': ['Any'],
                   'sms': ['120_Shines', 'Any'],
                   'smb1': ['Any'],
                   'botw': ['Any'],
                   'supermonkeyball': ['Expert'],
                   'supermonkeyball2': ['Story_Mode'],
                   'twwhd': ['Any'],
                   'oot': ['Any'],
                   'celeste': ['Any'],
                   'smb3': ['100']}


def is_new_wr(wr_date):
    past = datetime.today() - timedelta(weeks=1)
    return wr_date > past


def get_wr_date(json):
    return json.get('data').get('runs')[0].get('run').get('date')


def get_full_game_name(abbreviation):
    url = f"https://www.speedrun.com/api/v1/games/{abbreviation}"
    r = requests.get(url)
    game_info = json.loads(r.text)
    game_name = game_info.get('data').get('names').get('international')
    return(game_name)

if __name__ == '__main__':

    # Example URL: 'https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1'
    base_url = 'https://www.speedrun.com/api/v1/leaderboards/'
    for game, categories in game_categories.items():
        game_name = get_full_game_name(game)
        for category in categories:
            url = f'{base_url}{game}/category/{category}?top=1'
            print()
            r = requests.get(url)
            wr_info = json.loads(r.text)
            wr_date_str = get_wr_date(wr_info)
            wr_date = datetime.strptime(wr_date_str, '%Y-%m-%d')

            if is_new_wr(wr_date):
                print(f'NEW WORLD RECORD FOR {game_name} ON {wr_date_str}')
            else:
                time_diff = datetime.today() - wr_date
                print(f'{game_name}: {category} No new world records since '
                      f'{wr_date_str} ({time_diff.days} Days)')

            time.sleep(2)

    # Send email
    # https://realpython.com/python-send-email/
    port = 465
    password = input('Type your password then press enter: ')

    # Create a secure SSL context
    context = ssl.create_default_context()

    email = 'cjuracektest@gmail.com'
    subject = 'Speed Runs'
    body = 'This is a Python message'
    message = f'Subject: {subject} \n\n {body}'
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(email, password)
        server.sendmail(email, email, message)