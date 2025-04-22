import time
from datetime import datetime, timedelta

import requests


def get_questions(fromdate, todate, tag):
    url = 'https://api.stackexchange.com/2.3/questions'
    questions = []
    page = 1
    while True:
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
        data = requests.get(url, params=params).json()
        questions.extend(data['items'])
        if not data['has_more']:
            break
        page += 1
        time.sleep(0.1)
    return questions


def display_questions(days, tag):
    todate = int(datetime.now().timestamp())
    fromdate = todate - int(timedelta(days=days).total_seconds())
    questions = get_questions(fromdate, todate, tag)
    count = 0
    for question in questions:
        print(
            f'Вопрос: {question["title"]}\n'
            f'Тэги: {", ".join(question["tags"]).title()}\n'
            f'ID вопроса: {question["question_id"]}\n'
            f'Дата создания: {datetime.fromtimestamp(question["creation_date"]).strftime("%d.%m.%Y %H:%M:%S")}\n'
        )
        count += 1
    print(f'Общее количество вопросов c тэгом "{tag}" за последние {days} дн: {count}')


if __name__ == '__main__':
    display_questions(2, 'Python')
