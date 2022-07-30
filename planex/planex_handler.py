from typing import TextIO
import urllib.request
import json
from datetime import datetime


DUMP_FILE_PLANEX = "planex.json"
PLANEX_URL = "http://planex.insa-toulouse.fr/"
# 10 min
CUSTOM_MESSAGE_INTERVAL = 10 * 60 * 1000


def is_planex_down() -> bool:
    try:
        with urllib.request.urlopen(PLANEX_URL) as response:
            is_down = response.getcode() != 200
            return is_down
    except:
        print("Error processing following url: " + PLANEX_URL)
        return True


def get_json(file: TextIO) -> dict:
    file_json = {
        "info": {},
        "isPlanexDown": None
    }
    try:
        file_json = json.load(file)
    except json.JSONDecodeError as e:
        print("Error reading file " + file.name)
        print(e)

    if not ("info" in file_json):
        file_json["info"] = {}

    info = file_json["info"]
    if not ("last_checked" in info) or info[
            "last_checked"] < datetime.now().timestamp() * 1000 - CUSTOM_MESSAGE_INTERVAL:
        info["last_checked"] = datetime.now().timestamp() * 1000
    file_json["isPlanexDown"] = is_planex_down()
    return file_json


def write_json(data: dict, f: TextIO):
    f.seek(0)
    f.truncate(0)
    json.dump(data, f)


def main():
    with open(DUMP_FILE_PLANEX, 'w+', encoding='utf-8') as f:
        write_json(get_json(f), f)


main()
