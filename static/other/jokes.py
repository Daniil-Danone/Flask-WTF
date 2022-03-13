with open(r'C:\Users\mrsup\PycharmProjects\python_yandex_lessons\WEB + API\Flask-WTF\static\other\Schtirliz.txt', 'r', encoding='UTF-8') as jokes:
    jokes_list = jokes.read().split('https://anekdoty.ru/pro-shtirlica/')
    print(jokes_list)