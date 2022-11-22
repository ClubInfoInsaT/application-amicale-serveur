from typing import TextIO
import urllib.request
import json
from datetime import datetime
from bs4 import BeautifulSoup


DUMP_FILE_PLANEX = "planex.json"
PLANEX_URL = "http://planex.insa-toulouse.fr/"
# 10 min
CUSTOM_MESSAGE_INTERVAL = 10 * 60 * 1000


def parse_html(html_string: str) -> BeautifulSoup:
    return BeautifulSoup(html_string, "html.parser")

def is_planex_down() -> bool:
    try:
        with urllib.request.urlopen(PLANEX_URL) as response:
            if response.getcode() != 200:
                return True
            else:
                html = parse_html(response.read())
                title = html.find("title")
                # Note that there's no title tag in the HTML when planex is working normally
                return title != None and title.text == "503 Service Unavailable"
    except:
        print("Error processing following url: " + PLANEX_URL)
        return True


def get_json(file: TextIO) -> dict:
    file_json = {
        "info": {},
        "isPlanexDown": None
    }
    file.seek(0)
    content = file.read()
    if content:
        file_json = json.loads(content)

    if not ("info" in file_json):
        file_json["info"] = {}

    info = file_json["info"]
    if not ("last_checked" in info) or info[
            "last_checked"] < datetime.now().timestamp() * 1000 - CUSTOM_MESSAGE_INTERVAL:
        info["last_checked"] = int(datetime.now().timestamp() * 1000)
    file_json["info"] = info
    file_json["isPlanexDown"] = is_planex_down()
    return file_json


def write_json(data: dict, f: TextIO):
    f.seek(0)
    f.truncate(0)
    json.dump(data, f)


def main():
    # w+ : Opens a file for both writing and reading. Overwrites the existing
    # file if the file exists. If the file does not exist, it creates a new
    # file for reading and writing
    with open(DUMP_FILE_PLANEX, "w+", encoding='utf-8') as f:
        write_json(get_json(f), f)


main()
