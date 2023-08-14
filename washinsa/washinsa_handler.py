"""
As of april 2023, the washinsa website has been updated to use a new API.
hense the need to rewrite the entire scraper.
"""
from json import JSONDecodeError
import requests
from enum import Enum
import json
from datetime import datetime
from typing.io import TextIO

DUMP_FILE_INSA = "washinsa_data.json"
DUMP_FILE_TRIPODE_B = "tripode_b_data.json"
# 10 min
CUSTOM_MESSAGE_INTERVAL = 10 * 60 * 1000


class State(Enum):
    AVAILABLE = 0
    RUNNING = 1
    RUNNING_NOT_STARTED = 2
    FINISHED = 3
    UNAVAILABLE = 4
    ERROR = 5
    UNKNOWN = 6


def get_machine_state(string: str):
    """
    Gets the current machine state.
    If the state string cannot be recognized, this returns the unknown state.
    """
    if string == "LIBRE" or string == "DISPONIBLE":
        return State.AVAILABLE
    elif string == "OCCUPÉ":
        return State.RUNNING
    elif string == "RÉGLÉ":
        return State.RUNNING_NOT_STARTED
    elif string == "HORS SERVICE":
        return State.UNAVAILABLE
    elif string == "TERMINÉ":
        return State.FINISHED
    else:
        return State.UNKNOWN


def remaining_time(start_time: str, end_time: str) -> int:
    """
    Gets the remaining time in minutes.

    Args:
        start_time (str): The start time of the washer.
        end_time (str): The end time of the washer.

    Returns:
        The remaining time of the washer.
    """
    end_time = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
    remaining_time = end_time - datetime.now()
    remaining_time_minutes = int(remaining_time.total_seconds() / 60)
    return 0 if remaining_time_minutes < 0 else remaining_time_minutes


def craft_url(code: str):
    return f"https://api.cogedia.com/laveries/{code}/machines?machinestype=0&machinesvue=laverie&version=2"


def fetch_data(code: str):
    """Fetch data from the proxiwash website.

    Args:
        code (str): The code of the proxiwash site to fetch data from.

    Returns:
        The raw data from the website.
    """
    url = craft_url(code)
    headers = {
        'Origin': 'https://beta.proxiwash.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0'
    }
    try:
        print('Fetching data from : ' + url)
        response = requests.get(url, headers=headers)
        print('Response status code : ' + str(response.status_code))
        json_data = response.json()
        print('Response json data : ' + str(json_data))
        return json_data
    except:
        print("Error processing following url: " + url)
        return ""


def format_date_time(date: str):
    return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S").strftime("%H:%M")


def format_washers_data(data: dict):
    washers = []
    for washer in data["lavelinge"]:
        washers.append(
            {
                "number": washer["numero"],
                "state": get_machine_state(washer["etat_nom"].upper()).value,
                "maxWeight": washer["capacite"],
                "startTime": format_date_time(washer["date_debut"]),
                "endTime": format_date_time(washer["date_fin"]),
                "donePercent": washer["progression_programme"],
                "remainingTime": remaining_time(
                    washer["date_debut"], washer["date_fin"]
                ),
                "program": washer["programme"],
            }
        )
    return washers


def format_dryers_data(data: dict):
    dryers = []
    for dryer in data["sechelinge"]:
        dryers.append(
            {
                "number": dryer["numero"],
                "state": get_machine_state(dryer["etat_nom"].upper()).value,
                "maxWeight": dryer["capacite"],
                "startTime": format_date_time(dryer["date_debut"]),
                "endTime": format_date_time(dryer["date_fin"]),
                "donePercent": dryer["progression_programme"],
                "remainingTime": remaining_time(dryer["date_debut"], dryer["date_fin"]),
                "program": dryer["programme"],
            }
        )

    return dryers


def get_json(code: str, file: TextIO):
    file_json = {"info": {}, "dryers": [], "washers": []}

    try:
        file_json = json.load(file)
    except JSONDecodeError as e:
        print("Error reading file " + file.name)
        print(e)

    if not ("info" in file_json):
        file_json["info"] = {}

    info = file_json["info"]
    if (
        not ("last_checked" in info)
        or info["last_checked"]
        < datetime.now().timestamp() * 1000 - CUSTOM_MESSAGE_INTERVAL
    ):
        print("Updating proxiwash message")
        # TODO: Update message
        info["message"] = ""
        info["last_checked"] = datetime.now().timestamp() * 1000

    json_data = fetch_data(code)
    file_json["dryers"] = format_dryers_data(json_data)
    file_json["washers"] = format_washers_data(json_data)
    info["last_checked"] = datetime.now().timestamp() * 1000
    return file_json


# print(fetch_data("cf4f39"))


def write_json(data, f: TextIO):
    f.seek(0)
    f.truncate(0)
    json.dump(data, f)


def main():
    with open(DUMP_FILE_INSA, "w+", encoding="utf-8") as f:
        write_json(get_json("cf4f39", f), f)
    with open(DUMP_FILE_TRIPODE_B, "w+", encoding="utf-8") as f:
        write_json(get_json("b310b7", f), f)


main()
