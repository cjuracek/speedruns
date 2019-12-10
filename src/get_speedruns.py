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

game_names = {'sm64': 'Super Mario 64',
              'smo': 'Super Mario Odyssey',
              'sms': 'Super Mario Sunshine',
              'smb1': 'Super Mario Bros.',
              'botw': 'Breath of the Wild',
              'supermonkeyball': 'Super Monkey Ball',
              'supermonkeyball2': 'Super Monkey Ball 2',
              'twwhd': 'Wind Waker HD',
              'oot': 'Ocarina of Time',
              'celeste': 'Celeste',
              'smb3': 'Super Mario Bros. 3'}


def is_new_wr(wr_date):
    past = datetime.today() - timedelta(weeks=1)
    return wr_date > past


def get_wr_date(json):
    return json.get('data').get('runs')[0].get('run').get('date')


if __name__ == '__main__':

    # Example URL: 'https://www.speedrun.com/api/v1/leaderboards/o1y9wo6q/category/7dgrrxk4?top=1'
    base_url = 'https://www.speedrun.com/api/v1/leaderboards/'
    for game, categories in game_categories.items():
        for category in categories:
            url = f'{base_url}{game}/category/{category}?top=1'
            r = requests.get(url)
            wr_info = json.loads(r.text)
            wr_date_str = get_wr_date(wr_info)
            wr_date = datetime.strptime(wr_date_str, '%Y-%m-%d')

            if is_new_wr(wr_date):
                print(f'NEW WORLD RECORD FOR {game} ON {wr_date_str}')
            else:
                time_diff = datetime.today() - wr_date
                print(f'{game_names.get(game)}: {category} No new world records since '
                      f'{wr_date_str} ({time_diff.days} Days)')

            time.sleep(1)

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