import json
from datetime import date, datetime

FILE = 'menu_data.json'


def string_to_date(date_string):
    datetime_object = datetime.strptime(date_string, '%Y-%m-%d')
    return datetime_object.date()


def get_cleaned_data():
    with open(FILE) as f:
        data = json.load(f)
        indexes_to_delete = []
        for i in range(0, len(data)):
            current_date = string_to_date(data[i]['date'])
            if current_date < date.today():
                indexes_to_delete.append(i)
        print('Indexes to delete:')
        print(indexes_to_delete)
        for i in indexes_to_delete:
            del data[i]
        return data


def write_cleaned_data(data):
    with open(FILE, 'w') as f:
        json.dump(data, f)


def main():
    write_cleaned_data(get_cleaned_data())
    print('DONE')

main()
