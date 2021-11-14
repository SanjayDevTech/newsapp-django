import json
from django.shortcuts import render
from django.conf import settings
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=settings.API_KEY)


def index(req):
    top_headlines = newsapi.get_top_headlines(
        q='covid', page_size=1)

    everything = newsapi.get_everything(q='covid', page_size=4)['articles']
    sports = newsapi.get_everything(q='sports', page_size=5)['articles']
    tech = newsapi.get_everything(q='technology', page_size=5)['articles']
    business = newsapi.get_everything(
        q='business', page_size=5)['articles']
    entertainment = newsapi.get_everything(
        q='entertainment', page_size=5)['articles']
    headline = top_headlines['articles'][0]
    if top_headlines['status'] != 'ok':
        return render(req, 'error.html')
    return render(req, 'index.html', {'headline': headline, 'everything': everything, 'sports': sports, 'tech': tech, 'business': business, 'entertainment': entertainment})
