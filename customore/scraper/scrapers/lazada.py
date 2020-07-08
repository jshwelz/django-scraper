# coding=utf8
import requests
from bs4 import BeautifulSoup


def scrape(keyword):
    prods = []
    brands = []
    url_lazada = 'https://www.lazada.vn/catalog/?q='+keyword
    page = requests.get(
        'http://api.scraperapi.com?api_key=ff75da59d446351439f996b501ed6f87&url='+url_lazada+'&render=true')    
    soup_lazada = BeautifulSoup(page.content, 'html5lib')

    brands_div = soup_lazada.find_all('div', class_='c2cYd1')[1]
    brands_containers = brands_div.find_all(
        'label', class_='c3NQn0 ant-checkbox-wrapper')
    for i in range(len(brands_containers)):
        brands.append(str(brands_containers[i].text.strip()))

    for i in range(3):
        url_lazada = 'https://www.lazada.vn/catalog/?q=' + \
            keyword+'&page='+str(i)
        page = requests.get(
            'http://api.scraperapi.com?api_key=ff75da59d446351439f996b501ed6f87&url='+url_lazada+'&render=true')
        soup_shopee = BeautifulSoup(page.content, 'html5lib')

        table = soup_lazada.find('div', attrs={'class': 'c1_t2i'})
        prod_containers = table.find_all('div', class_='c2prKC')
        for idx, row in enumerate(prod_containers):
            parent_div = row.div.find('div', class_='c16H9d')
            prods.append(parent_div.text)

    return {'brands': brands, 'prods': prods}


def get_stats(keyword):
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
