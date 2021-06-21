import json
import csv
import requests
import time
import random
from random import randint

from faker import Faker

def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)

def makeReviews():
    with open('./reviews.csv', 'a', encoding='utf-8', newline='\n') as f:
        fake = Faker('ko_KR')
        wr = csv.writer(f)
        wr.writerow('')

        for i in range(100):
            user_id = random.randint(1, 100)
            book_id = random.randint(1, 500)
            comment = f'멋지네요 from {fake.city()} [{fake.job()}]'
                    
            wr.writerow([user_id, book_id, ''.join(comment)])

def makeLikes():
    with open('./likes.csv', 'a', encoding='utf-8', newline='\n') as f:
        wr = csv.writer(f)
        wr.writerow('')

        for i in range(100):
            review_id = random.randint(1, 100)
            user_id = random.randint(1, 100)
                    
            wr.writerow([review_id, user_id])


def makeBooks():
    with open('./response.json', 'r') as f:
        response = f.read()
        data = json.loads(response)
        result = []

        for book in data['books']:
            items = book['items']
            
            for item in items:
                volumeInfo = item['volumeInfo']

                append_data = []
                
                title = volumeInfo.get('title', '')
                append_data.append(title)

                subtitle = volumeInfo.get('subtitle', '')
                append_data.append(subtitle)

                if 'imageLinks' in volumeInfo:
                    image_url = volumeInfo['imageLinks'].get('thumbnail', '')
                    append_data.append(image_url)
                else:
                    append_data.append('')

                company = volumeInfo.get('publisher', '')
                append_data.append(company)

                authors = ','.join(volumeInfo.get('authors', ''))
                append_data.append(authors)

                about_author = volumeInfo.get('about_author', '')
                append_data.append(about_author)

                company_review =volumeInfo.get('company_review', '')
                append_data.append(company_review)

                #category = '.'.join(volumeInfo.get('categories', ''))
                append_data.append(randint(1,20))

                page = volumeInfo.get('pageCount', randint(100, 340))
                append_data.append(page)

                publication_date = volumeInfo.get('publishedDate', '')
           
                if len(publication_date) < 8:
                    date = random_date("2020-12-15", "2020-12-31", random.random())
                    append_data.append(date)
                else:
                    append_data.append(publication_date)

                description = volumeInfo.get('description', '')
                append_data.append(description)
                
                append_data.append(random.randint(1, 7))
                result.append(append_data)

        f = open('books.csv', 'a', encoding='utf-8', newline='\n')
        
        wr = csv.writer(f)
        wr.writerow('')
        for data in result:
            wr.writerow(data)

        
    
