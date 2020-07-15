# coding=utf8
import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
from celery.result import AsyncResult


def scrape(keyword):
    prods = []
    brands = []    
    url_shopee = 'https://shopee.vn/search?keyword='+keyword        
    page = requests.get('http://api.scraperapi.com?api_key=d7602b450bf01e4f56a99e96a5174f6e&url='+url_shopee+'&render=true')                    
    soup_shopee = BeautifulSoup(page.content, 'html5lib')
    brands_div = soup_shopee.find('div', class_ = 'shopee-filter-group shopee-brands-filter') 
    while brands_div is None:
        page = requests.get('http://api.scraperapi.com?api_key=d7602b450bf01e4f56a99e96a5174f6e&url='+url_shopee+'&render=true')                    
        soup_shopee = BeautifulSoup(page.content, 'html5lib')
        brands_div = soup_shopee.find('div', class_ = 'shopee-filter-group shopee-brands-filter') 

    brands_containers = brands_div.find_all('div', class_ = 'shopee-filter shopee-checkbox-filter')                        
    for i in range(len(brands_containers)):                
        brands.append(str(brands_containers[i].text.strip()))


    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("window-size=1920,1080")
    browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            
    for i in range(2):                
        url_shopee = 'https://shopee.vn/search?keyword='+keyword+'&page='+str(i)         
        browser.get(url_shopee)            
        browser.execute_script("window.scrollTo(0, (document.body.scrollHeight/4));")        
        time.sleep(4)         
        browser.execute_script("window.scrollTo(0, (document.body.scrollHeight/2));")
        time.sleep(4)         
        browser.execute_script("window.scrollTo(0, (document.body.scrollHeight/2)+150);")
        time.sleep(4)         
                
        soup_shopee = BeautifulSoup(browser.page_source, 'html5lib')                                
        table = soup_shopee.find('div', attrs = {'class':'row shopee-search-item-result__items'})
        prod_containers = table.find_all('div', class_ = 'col-xs-2-4 shopee-search-item-result__item')    
                
        for idx,row in enumerate(prod_containers):    
            parent_div = row.div.find('div', class_ = 'O6wiAW')        
            if parent_div is not None:                
                prods.append(parent_div.text)
        
    return {'brands':brands,'prods': prods}


def get_stats_shopee(keyword):
    result = scrape(keyword)
    count = 0
    response = {}
    stats = []
    brands = result['brands']
    response.update({'brands': brands})
    for brand in brands:
        stat = {}
        stat['brand'] = brand
        for n in result['prods'][:100]:
            if n.count(brand) > 0:
                count += 1
        stat['share'] = count
        stats.append(stat)
    response.update({'stats': stats})
    return response
