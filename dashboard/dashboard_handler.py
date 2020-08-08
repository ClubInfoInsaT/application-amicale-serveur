import json
from datetime import date
import urllib.request
import os.path

WASHINSA_FILE = '../washinsa/washinsa_data.json'
MENU_FILE = '../menu/menu_data.json'
FACEBOOK_FILE = '../facebook/facebook_data.json'


WASHINSA_LOCK = '../washinsa/lock'
MENU_LOCK = '../menu/lock'
FACEBOOK_LOCK = '../facebook/lock'

PROXIMO_URL = 'https://etud.insa-toulouse.fr/~proximo/data/stock-v2.json'
TUTORINSA_URL = 'https://etud.insa-toulouse.fr/~tutorinsa/api/get_data.php'
PLANNING_URL = 'https://amicale-insat.fr/event/json/list'

DASHBOARD_FILE = 'dashboard_data.json'


def get_news_feed():
    """
    Get facebook news and truncate the data to 15 entries for faster loading

    :return: an object containing the facebook feed data
    """
    # Prevent concurrent access to file
    while os.path.isfile(FACEBOOK_LOCK):
        print("Waiting for Facebook lock")
    try:
        with open(FACEBOOK_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        print("Could not find " + FACEBOOK_FILE)
        return {'data': []}


def get_available_machines():
    """
    Get the number of available washing/drying machines

    :return: a tuple containing the number of available dryers and washers
    """
    # Prevent concurrent access to file
    while os.path.isfile(WASHINSA_LOCK):
        print("Waiting for washinsa lock")
    try:
        with open(WASHINSA_FILE) as f:
            data = json.load(f)
            available_dryers = 0
            available_washers = 0
            for machine in data['dryers']:
                if machine['state'] == 0:
                    available_dryers += 1
            for machine in data['washers']:
                if machine['state'] == 0:
                    available_washers += 1
    except FileNotFoundError:
        print("Could not find " + WASHINSA_FILE)
        return 0, 0
    return available_dryers, available_washers


def get_today_menu():
    """
    Check if the menu for the current day is available

    :return: a list containing today's menu
    """
    # Prevent concurrent access to file
    while os.path.isfile(MENU_LOCK):
        print("Waiting for menu lock")
    try:
        with open(MENU_FILE) as f:
            data = json.load(f)
            menu = []
            for i in range(0, len(data)):
                if data[i]['date'] == date.today().strftime('%Y-%m-%d'):
                    menu = data[i]['meal'][0]['foodcategory']
                    break
            return menu
    except FileNotFoundError:
        print("Could not find " + MENU_FILE)
        return []


def get_proximo_article_number():
    """
    Get the number of articles on sale at proximo

    :return: an integer representing the number of articles
    """
    try:
        with urllib.request.urlopen(PROXIMO_URL) as response:
            data = json.loads(response.read().decode())
            count = 0
            for article in data['articles']:
                if int(article['quantity']) > 0:
                    count += 1
            return count
    except:
        print("Error processing following url: " + PROXIMO_URL)
        return 0


def get_tutorinsa_tutoring_number():
    """
    Get the number of tutoring classes available

    :return: an integer representing the number of tutoring classes
    """
    try:
        with urllib.request.urlopen(TUTORINSA_URL) as response:
            data = json.loads(response.read().decode())
            return int(data['tutorials_number'])
    except:
        print("Error processing following url: " + TUTORINSA_URL)
        return 0


def get_today_events():
    """
    Get today's events

    :return: an array containing today's events
    """
    try:
        with urllib.request.urlopen(PLANNING_URL) as response:
            data = json.loads(response.read().decode())
            today_events = []
            for event in data:
                if event['date_begin'].split(' ')[0] == date.today().strftime('%Y-%m-%d'):
                    today_events.append(event)
            return today_events
    except:
        print("Error processing following url: " + PLANNING_URL)
        return []

def generate_dashboard_json():
    """
    Generate the actual dashboard

    :return: an object containing the dashboard's data
    """
    available_machines = get_available_machines()
    available_tutorials = get_tutorinsa_tutoring_number()
    return {
        'dashboard': {
            'today_events': get_today_events(),
            'available_dryers': available_machines[0],
            'available_washers': available_machines[1],
            'available_tutorials': available_tutorials,
            'today_menu': get_today_menu(),
            'proximo_articles': get_proximo_article_number()
        },
        'news_feed': get_news_feed()
    }


def main():
    with open(DASHBOARD_FILE, 'w') as f:
        json.dump(generate_dashboard_json(), f)


main()
