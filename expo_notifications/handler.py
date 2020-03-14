from exponent_server_sdk import PushClient
from exponent_server_sdk import PushMessage
import mysql.connector  # using lib from https://github.com/expo/expo-server-sdk-python
import json
from enum import Enum

isDebug = False


class Priority(Enum):
    DEFAULT = 'default'
    NORMAL = 'normal'
    HIGH = 'high'


class ChannelIDs(Enum):
    REMINDERS = 'reminders'


class MachineStates(Enum):
    FINISHED = 'TERMINE'
    READY = 'DISPONIBLE'
    RUNNING = 'EN COURS'
    BROKEN = 'HS'
    ERROR = 'ERROR'


if isDebug:
    washinsaFile = 'data.json'
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="test",
        passwd="coucou",
        database="test"
    )
else:
    washinsaFile = '../washinsa/washinsa.json'
    db = mysql.connector.connect(
        host="127.0.0.1",
        user="amicale_app",
        passwd="EYiDCalfNj",
        database="amicale_app"
    )


def send_push_message(token, title, body, channel_id, extra=None):
    prio = Priority.HIGH.value if channel_id == ChannelIDs.REMINDERS.value else Priority.NORMAL.value
    print(prio)
    response = PushClient().publish(
        PushMessage(to=token,
                    title=title,
                    body=body,
                    data=extra,
                    sound='default',
                    priority=prio))


def get_machines_of_state(state):
    machines = []
    with open(washinsaFile) as f:
        data = json.load(f)
        for d in data['dryers']:
            if d['state'] == state:
                machines.append(d['number'])
        for d in data['washers']:
            if d['state'] == state:
                machines.append(d['number'])
    return machines


def get_machine_remaining_time(machine_id):
    with open(washinsaFile) as f:
        data = json.load(f)
        for d in data['dryers']:
            if d['number'] == machine_id:
                return int(d['remainingTime'])
        for d in data['washers']:
            if d['number'] == machine_id:
                return int(d['remainingTime'])
    return 0


def send_end_notifications():
    cursor = db.cursor()
    machines = get_machines_of_state(MachineStates.FINISHED.value)
    for machine_id in machines:
        cursor.execute('SELECT * FROM machine_watchlist WHERE machine_id=%s', (machine_id,))
        result = cursor.fetchall()
        for r in result:
            token = r[2]
            translation = get_notification_translation(token, False)
            body = translation["body"].replace("%s", machine_id, 1)
            title = translation["title"].replace("%s", machine_id, 1)
            # Remove from db
            cursor.execute('DELETE FROM machine_watchlist WHERE machine_id=%s AND user_token=%s', (machine_id, token,))
            db.commit()
            send_push_message(token, title, body, ChannelIDs.REMINDERS.value)


def send_reminder_notifications():
    cursor = db.cursor()
    machines = get_machines_of_state(MachineStates.RUNNING.value)
    print(machines)
    for machine_id in machines:
        remaining_time = get_machine_remaining_time(machine_id)
        print(remaining_time)
        cursor.execute('SELECT * FROM machine_watchlist WHERE machine_id=%s', (machine_id,))
        result = cursor.fetchall()
        print(result)
        for r in result:
            if r[3] == 0:  # We did not send a reminder notification yet
                token = r[2]
                user_reminder_time = get_user_reminder_time(token)
                if user_reminder_time >= remaining_time:
                    translation = get_notification_translation(token, True)
                    body = translation["body"].replace("%s", machine_id, 1)
                    title = translation["title"].replace("%s", machine_id, 1)
                    cursor.execute(
                        'UPDATE machine_watchlist SET reminder_sent=%s WHERE machine_id=%s AND user_token=%s',
                        (1, machine_id, token,))
                    db.commit()
                    send_push_message(token, title, body, ChannelIDs.REMINDERS.value)


def get_user_reminder_time(token):
    cursor = db.cursor()
    cursor.execute('SELECT machine_reminder_time FROM users WHERE token=%s', (token,))
    result = cursor.fetchall()
    print(result[0][0])
    return result[0][0]


def get_user_locale(token):
    cursor = db.cursor()
    cursor.execute('SELECT locale FROM users WHERE token=%s', (token,))
    result = cursor.fetchall()
    print(result[0][0])
    locale = 'en'
    if "fr" in result[0][0]:
        locale = 'fr'
    return locale


def get_notification_translation(token, is_reminder):
    locale = get_user_locale(token)
    file_name = locale + '.json'
    print(file_name)
    with open(file_name) as f:
        data = json.load(f)
        if is_reminder:
            translation = data["reminderNotification"]
        else:
            translation = data["endNotification"]
    print(translation)
    return translation


def main():
    send_reminder_notifications()
    send_end_notifications()


main()
