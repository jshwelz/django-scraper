import time
import requests
from celery import shared_task
from bs4 import BeautifulSoup
from .scrapers.lazada import get_stats

@shared_task
def create_task(keyword):
    print('over here')
    return get_stats(keyword)    




  
