import time
import requests
from celery import shared_task
from .scrapers.lazada import get_stats
from .scrapers.shopee import get_stats_shopee

@shared_task
def create_task_lazada(keyword):
    print('scraping lazada')
    return get_stats(keyword)    

@shared_task
def create_task_shopee(keyword):
    print('scraping shopee')
    return get_stats_shopee(keyword)    
