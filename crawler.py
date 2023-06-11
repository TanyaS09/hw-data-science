import requests
from bs4 import BeautifulSoup
import json
import time
import csv

API_KEY = 'YOUR_API_KEY'  # API-ключ, заменить на свой
topics = ['Recipes',
          'Video Games and Consoles',
          'Politics',
          'Climate and Environment',
          'Business',
          'Sports',
          'Technology'
          ]


def retrieve_data(topic, writer):
    '''
    Обращаемся к статьям на заданную тему
    param topic: тема
    param writer: объект csv.writer, записывает данные текущей статьи в csv-табличку
    '''
    page = 0  # стартовую страницу можно менять
    # entries = []
    while page < 200:  # условие с NYTimes
        url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json?q={topic}&api-key={API_KEY}&page={page}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        main_par = soup.find('p')
        obj = json.loads(main_par.text)

        try:
            articles = obj['response']['docs']
        except KeyError:
            print(obj)
            page += 1
            continue

        if len(articles) == 0:
            print('no articles!')
            break

        for article in articles:
            headline, abstract, lead = article['headline']['main'], article['abstract'], article['lead_paragraph']
            entry = [topic, headline, abstract, lead]
            # entries.append(entry)
            writer.writerow(entry)
            # print(entry)
        print(f'Successfully retrieved data for topic {topic} on page {page}')
        time.sleep(5) # обманываем rate limiter сайта
        page += 1


def parse_nytimes(filename):
    '''
    Основная функция для парсинга
    param filename: путь до файла, в который будем сохранять данные
    '''
    file = open(filename, 'a')
    writer = csv.writer(file)
    writer.writerow(['topic', 'headline', 'abstract', 'paragraph'])

    for topic in topics:
        retrieve_data(topic, writer)
        print(f'Successfully retrieved data for topic {topic}!')

    file.close()


parse_nytimes('articles.csv')
