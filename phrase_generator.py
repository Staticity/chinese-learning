import pandas as pd

from random import randrange
from datetime import timedelta, datetime
from chinese_words import Word, practice
from typing import List

NUMBERS = {
    '0': 'ling2',
    '1': 'yi1',
    '2': 'er4',
    '3': 'san1',
    '4': 'si4',
    '5': 'wu3',
    '6': 'liu4',
    '7': 'qi1',
    '8': 'ba1',
    '9': 'jui3',
    '10': 'shi2',
    '11': 'shi2yi1',
    '12': 'shi2er4',
    '100': 'bai3',
    '1000': 'qian1'
}


def pretty_date(time):
    return time.strftime('%B %d, %Y %I:%M %p')


def random_date(start=pd.to_datetime('1970-01-01'), end=pd.to_datetime('2070-01-01')):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def translate_number(num: int):
    assert num >= 0
    assert num < 10000

    s = ''
    if num >= 1000:
        s += NUMBERS[str(num)[0]].replace('yi1', '')
        s += NUMBERS['1000']
        num = int(str(num)[1:])
    if num >= 100:
        s += NUMBERS[str(num)[0]].replace('yi1', '')
        s += NUMBERS['100']
        num = int(str(num)[1:])
    if num >= 10:
        s += NUMBERS[str(num)[0]].replace('yi1', '')
        s += NUMBERS['10']
        num = int(str(num)[1:])
    if num > 0:
        s += NUMBERS[str(num)[0]].replace('yi1', '')

    return s


def translate_date(
    time: datetime,
    use_year=True,
    use_month=True,
    use_day=True,
    use_timeofday=True,
    use_hour=True,
    use_minute=True) -> str:
    year = ''
    for c in str(time.year):
        year += NUMBERS[c]
    year += ' nian2'

    month = f'{NUMBERS[str(time.month)]} yue4'

    day = translate_number(time.day) + ' hao4'

    time_of_day = ''
    if time.hour == 12 and time.minute == 0:
        time_of_day = 'zhong1wu3'
    elif time.hour == 24 and time.minute == 0:
        time_of_day = 'ban4ye4'
    elif time.hour >= 0 and time.hour <= 4:
        time_of_day = 'ling2chen2'
    elif time.hour >= 4 and time.hour <= 9:
        time_of_day = 'zao3shang5'
    elif time.hour >= 9 and time.hour <= 12:
        time_of_day = 'shang4wu3'
    elif time.hour >= 12 and time.hour <= 12 + 6:
        time_of_day = 'xia4wu3'
    elif time.hour >= 12 + 6 and time.hour <= 12 + 12:
        time_of_day = 'shang4wu3'

    hour = translate_number(time.hour) + ' dian3'
    minute = translate_number(time.minute) + ' fen1'
    if minute == 0:
        minute = ''
    elif minute == 30:
        minute = 'ban4'

    return ' '.join([
        year if use_year else '',
        month if use_month else '',
        day if use_day else '',
        time_of_day if use_timeofday else '',
        hour if use_hour else '',
        minute if use_minute else ''
    ])


def main():
    N = int(input("How many dates to translate? "))
    dates = [random_date() for _ in range(N)]
    words = [Word(None, pinyin_numerical=translate_date(d), english=pretty_date(d)) for d in dates]
    practice(words)


if __name__ == '__main__':
    main()
