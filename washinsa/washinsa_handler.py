# Parser made with BeautifulSoup4
# https://www.crummy.com/software/BeautifulSoup/bs4/doc
from json import JSONDecodeError

from bs4 import BeautifulSoup
import urllib.request
from enum import Enum
import re
import json
from datetime import datetime

from typing.io import TextIO

'''
PAGE STRUCTURE
as of july 2021

A table with a row (tr html tag) for each machine
Each machine row is composed of 6 columns
 - 1 - Type ("SECHE LINGE 14 KG" or "LAVE LINGE 6 KG")
 - 2 - Number ("No X" with X the current number)
 - 3 - Status (A string showing the status or a table showing the progress)
 - 4 - Program (Name of the program or empty)
 - 5 - Start time (The start time in format HH:MM or empty)
 - 6 - End time (The end time in format HH:MM or empty)

Custom message (errors displayed on the website)
Must use the non-raw url to see it.
In the <font> under the <div> of id msg-permanent
example message: Perturbations operateur, laverie non connectee a internet depuis le 12/07/2021 a 19h45
'''

DUMP_FILE_INSA = "washinsa_data.json"
DUMP_FILE_TRIPODE_B = "tripode_b_data.json"
WASHINSA_RAW_URL = "https://www.proxiwash.com/weblaverie/component/weblaverie/?view=instancesfiche&format=raw&s="
WASHINSA_URL = "https://www.proxiwash.com/weblaverie/ma-laverie-2?s="
DRYER_STRING = "SECHE LINGE"
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


# Table used to convert state string given by the page into State enum
STATE_CONVERSION_TABLE = {
    "DISPONIBLE": State.AVAILABLE,
    "TERMINE": State.FINISHED,
    "REGLE": State.RUNNING_NOT_STARTED,
    "HORS SERVICE": State.UNAVAILABLE,
    "ERREUR": State.ERROR,
}

TIME_RE = re.compile("^\d\d:\d\d$")


def get_json(code: str, file: TextIO):
    file_json = {
        "info": {},
        "dryers": [],
        "washers": []
    }
    try:
        file_json = json.load(file)
    except JSONDecodeError as e:
        print("Error reading file " + file.name)
        print(e)

    if not ("info" in file_json):
        file_json["info"] = {}

    info = file_json["info"]
    if not ("last_checked" in info) or info[
        "last_checked"] < datetime.now().timestamp() * 1000 - CUSTOM_MESSAGE_INTERVAL:
        print("Updating proxiwash message")
        info["message"] = get_message(code)
        info["last_checked"] = datetime.now().timestamp() * 1000
    parsed_data = get_machines(code)
    file_json["dryers"] = parsed_data["dryers"]
    file_json["washers"] = parsed_data["washers"]
    return file_json


def get_machines(code: str):
    soup = BeautifulSoup(download_page(code), 'html.parser')
    rows = get_rows(soup)
    return get_parsed_data(rows)


def get_message(code: str):
    soup = BeautifulSoup(download_page(code, False), 'html.parser')
    msg = soup.find(id="msg-permanent")
    if msg:
        return soup.find(id="msg-permanent").font.string
    return None


def download_page(code: str, raw=True):
    """
    Downloads the page from proxiwash website
    """
    url = WASHINSA_RAW_URL + code
    if not raw:
        url = WASHINSA_URL + code

    try:
        with urllib.request.urlopen(url) as response:
            return response.read().decode()
    except:
        print("Error processing following url: " + url)
        return ""


def get_rows(soup: BeautifulSoup):
    """
    Gets rows corresponding to machines on the page
    """
    rows = soup.table.contents
    del rows[0]
    return rows


def is_machine_dryer(row):
    """
    Checks if the given machine is a dryer. If it is not, it means it is a washer.

    To check this, we look if the test string is included in the state string
    """
    return DRYER_STRING in row.contents[0].text


def get_machine_weight(row):
    """
    Find the maximum weight supported by the machine.
    """
    return int(re.search("LINGE (.*?) KG", row.contents[0].text).group(1))


def get_machine_number(row):
    """
    Gets the current machine number.

    To find it, we look in the Number cell and remove the "No" prefix to keep only the number.
    We do not rely on the index in the list as it could get lost in parsing.
    Plus, this method allows for non numeric machine identifiers.
    """
    return row.contents[1].text.split()[1]


def get_machine_state(row):
    """
    Gets the current machine state.

    The state is usually written in plain text inside the State cell.
    In this case, we simply check it against the state translation table,
    to turn it into a State Enum, which is easier to manipulate.

    In some cases, this plain text is replace by a progress bar.
    This the machine is running.

    If the state string cannot be recognized, this returns the unknown state.
    """
    content = row.contents[2].contents[0]
    state = State.UNKNOWN
    if content.name == "table":
        state = State.RUNNING
    else:
        for key in STATE_CONVERSION_TABLE:
            if key in content.text:
                state = STATE_CONVERSION_TABLE[key]
                break
    return state


def get_machine_program(row):
    """
    Gets the machine program as written in plain text in the Program cell
    """
    return row.contents[3].text.strip()


def get_machine_times(row):
    """
    Gets the start and end time for the machine.

    If one of these times is invalid (does not respect the HH:MM format), an empty string is returned
    """
    start_time = row.contents[4].text
    end_time = row.contents[5].text
    if TIME_RE.match(start_time) and TIME_RE.match(end_time):
        return start_time, end_time
    else:
        return "", ""


def get_machine_done_percent(row):
    """
    Gets the machine done percentage.

    This percent is given in the width property of the first column, in the table inside the State cell.
    This only applies if the machine is running.
    """
    content = row.contents[2].contents[0]
    percent = ""
    if content.name == "table":
        percent = content.td["width"].replace("%", "")
        if float(percent) > 100:  # because the website is not doing this check...
            percent = '100'
    return percent


def get_machine_remaining_time(row):
    """
    Gets the remaining time in minutes.

    The time is written in the title property of the table inside the State cell.
    It is written inside a phrase, so we need to extract it.
    This only applies if the machine is running.
    """
    content = row.contents[2].contents[0]
    time = 0
    if content.name == "table":
        time = content["title"].split("=")[1].split()[0]
    return time


def is_machine_parsed(dryers, washers, number: int):
    for m in dryers:
        if m["number"] == number:
            return True
    for m in washers:
        if m["number"] == number:
            return True
    return False


def get_parsed_data(rows):
    """
    Gets the parsed data from the web page, formatting it in a easy to use object
    """
    dryers = []
    washers = []
    for row in rows:
        machine_number = get_machine_number(row)
        if not is_machine_parsed(dryers, washers, machine_number):
            state = get_machine_state(row)
            machine = {
                "number": machine_number,
                "state": state.value,
                "maxWeight": get_machine_weight(row),
                "startTime": "",
                "endTime": "",
                "donePercent": "",
                "remainingTime": "",
                "program": "",
            }
            if state == State.RUNNING:
                machine_times = get_machine_times(row)
                machine["startTime"] = machine_times[0]
                machine["endTime"] = machine_times[1]
                if len(machine_times[0]) == 0:
                    state = State.RUNNING_NOT_STARTED
                    machine["state"] = state.value
                machine["program"] = get_machine_program(row)
                machine["donePercent"] = get_machine_done_percent(row)
                machine["remainingTime"] = get_machine_remaining_time(row)

            if is_machine_dryer(row):
                dryers.append(machine)
            else:
                washers.append(machine)
    return {
        "dryers": dryers,
        "washers": washers
    }


def write_json(data, f: TextIO):
    f.seek(0)
    f.truncate(0)
    json.dump(data, f)


def main():
    dump_data = {}
    with open(DUMP_FILE_INSA, 'r+', encoding='utf-8') as f:
        write_json(get_json("cf4f39", f), f)
    with open(DUMP_FILE_TRIPODE_B, 'r+', encoding='utf-8') as f:
        write_json(get_json("b310b7", f), f)


main()
