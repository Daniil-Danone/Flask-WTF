import bs4
import requests


def _get_weather():
    url = "https://sinoptik.com.ru/pogoda/omsk"
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.text, "html.parser")
    day_date = soup.findAll('p', class_='_2sm7yHKV _1jSRkJI-')
    day_month = soup.findAll('p', class_='_1hHOVfLg')
    day_day = soup.findAll('p', class_='CitDZms5')
    current_temp = soup.findAll('p', class_='_2LM4MsxZ')

    date = day_date[0].text
    month = day_month[0].text
    day = day_day[0].text
    temp = current_temp[0].text

    today = f'📅 Сегодня:'
    day = f'{day.capitalize()}, {date} {month}'
    temperature = f'🌡 Текущая температура:'
    temperature_value = f'{temp}'
    t = int(temp.rstrip('°C'))
    if t <= 0:
        advice = 'Сегодня холодно❄, поэтому одевайтесь потеплее🧣!'
    elif 0 < t <= 15:
        advice = 'Сегодня не жарко🌬, сильно не раздевайтесь🧥!'
    elif 15 < t < 30:
        advice = 'Сегодня тепло🌡 , можно одеться полегче👕!'
    else:
        advice = 'Сегодня очень жарко🔥 , можно пойти на пляж⛱!'

    return today, day, temperature, temperature_value, advice