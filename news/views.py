import json
from django.shortcuts import render
from django.conf import settings
from newsapi import NewsApiClient
import pymongo
import datetime

client = pymongo.MongoClient(
    "mongodb+srv://news:newspass@cluster0.bjrgg.mongodb.net/news?retryWrites=true&w=majority")

db = client["news"]

# Init
newsapi = NewsApiClient(api_key=settings.API_KEY)


def category(req, category):
    category_news = newsapi.get_everything(q=category, page_size=8)['articles']
    return render(req, 'category.html', {'category': category, 'headline': category_news[0], 'everything': category_news[1:]})


def index(req):
    currentDate = datetime.datetime.now()
    currentDate = currentDate.replace(
        hour=0, minute=0, second=0, microsecond=0)

    def transform(x):
        x['time'] = int(currentDate.timestamp())
        return x
    indexCol = db['index']
    indexNews = indexCol.find_one()
    if indexNews is None or indexNews.get('time', 0) != int(currentDate.timestamp()):
        top_headlines = newsapi.get_top_headlines(q='covid', page_size=1)
        everything = newsapi.get_everything(q='covid', page_size=4)['articles']
        sports = newsapi.get_everything(q='sports', page_size=5)['articles']
        tech = newsapi.get_everything(q='technology', page_size=5)['articles']
        business = newsapi.get_everything(
            q='business', page_size=5)['articles']
        entertainment = newsapi.get_everything(
            q='entertainment', page_size=5)['articles']
        indexCol.delete_many({})
        indexCol.insert_many(
            list(map(transform, [top_headlines['articles'][0]] + everything + sports + tech + business)))
        headline = top_headlines['articles'][0]
        if top_headlines['status'] != 'ok':
            return render(req, 'error.html')
    else:
        indexNews = indexCol.find()
        newsContent = [x for x in indexNews]
        headline = newsContent[0]
        everything = newsContent[1:5]
        sports = newsContent[5:10]
        tech = newsContent[10:15]
        business = newsContent[15:20]
        entertainment = newsContent[20:]
    return render(req, 'index.html', {'headline': headline, 'everything': everything, 'sports': sports, 'tech': tech, 'business': business, 'entertainment': entertainment})
