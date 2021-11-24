from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

CACHE_TIME = 1

urlpatterns = [
    path('', cache_page(CACHE_TIME)(views.index)),
    path('c/<category>', cache_page(CACHE_TIME)(views.category))
]
