from datetime import datetime

import requests
import time


def get_fromdate_in_unix_format(days):
    current_date = datetime.now().date()
    start_current_day = datetime.strptime(str(current_date), '%Y-%m-%d')
    start_current_day_unix = round(start_current_day.timestamp())
    fromdate_unix = start_current_day_unix - (days-1)*86400
    return fromdate_unix


def get_todate_in_unix_format():
    todate = datetime.now()
    todate_unix = round(todate.timestamp())
    return todate_unix


def get_questions_database(fromdate, todate, tag):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        'pagesize': 100,
        'fromdate': fromdate,
        'todate': todate,
        'order': 'desc',
        'sort': 'creation',
        'tagged': tag,
        'site': 'stackoverflow',
        'filter': '!Oev7Wy_R1V2(FCx0dk)EMHuEYlzRTuqVwJGa2kVi*Kp'
    }
    database = requests.get(url, params=params).json()
    database_c = database
    page = 1
    while database_c['has_more']:
        page += 1
        url = "https://api.stackexchange.com/2.3/questions"
        params = {
            'page': page,
            'pagesize': 100,
            'fromdate': fromdate,
            'todate': todate,
            'order': 'desc',
            'sort': 'creation',
            'tagged': tag,
            'site': 'stackoverflow',
            'filter': '!Oev7Wy_R1V2(FCx0dk)EMHuEYlzRTuqVwJGa2kVi*Kp'
        }
        database_c = requests.get(url, params=params).json()
        for item in database_c['items']:
            database['items'].append(item)
        time.sleep(0.1)
    return database


def get_questions(days, tag):
    fromdate = get_fromdate_in_unix_format(days)
    todate = get_todate_in_unix_format()
    questions_database = get_questions_database(fromdate, todate, tag)
    count = 0
    for question in questions_database['items']:
        print(
            f"Вопрос: {question['title']}\n"
            f"Тэги: {', '.join(question['tags']).title()}\n"
            f"ID вопроса: {question['question_id']}\n"
            f"Дата создания: {datetime.fromtimestamp(question['creation_date'])}\n"
        )
        count += 1
    print(f"Общее количество вопросов c тэгом '{tag}' за последние {days} дн: {count}")


if __name__ == '__main__':
    get_questions(2, 'Python')
