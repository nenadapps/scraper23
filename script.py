from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
from time import sleep
import requests

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp

    try:
        price_elem = html.select('.entry-summary ins .woocommerce-Price-amount')
        if not price_elem:
            price_elem = html.select('.entry-summary .woocommerce-Price-amount')
        price = price_elem[0].get_text().strip()
        stamp['price'] = price.replace('$', '').replace(',', '').strip()
    except: 
        stamp['price'] = None
        
    try:
        title = html.select('.product_title')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None
    
    try:
        dimensions = html.select('.woocommerce-product-attributes-item--dimensions .woocommerce-product-attributes-item__value')[0].get_text().strip()
        stamp['dimensions'] = dimensions
    except:
        stamp['dimensions'] = None    
        
        
    try:
        stock_num = ''
        stock_num_temp = html.select('.stock')[0].get_text().strip()
        if 'in stock' in stock_num_temp:
            stock_num = stock_num_temp.replace('in stock', '').strip()
        stamp['stock_num'] = stock_num
    except:
        stamp['stock_num'] = None    
        
    try:
        category_cont = html.select('.woocommerce-breadcrumb')[0]
        category_temp = category_cont.select('a')[1].get_text().strip()
        if ')' in category_temp:
            category_parts = category_temp.split(')')
            category = category_parts[1].strip()
        else:
            category = category_temp
        stamp['category'] = category
    except:
        stamp['category'] = None     

    try:
        sub_category_cont = html.select('.woocommerce-breadcrumb')[0]
        sub_category = sub_category_cont.select('a')[2].get_text().strip()
        stamp['sub_category'] = sub_category
    except:
        stamp['sub_category'] = None 
        

    stamp['currency'] = "USD"

    # image_urls should be a list
    images = []                    
    try:
        image_items = html.select('.woocommerce-product-gallery__image a')
        for image_item in image_items:
            img = image_item.get('href')
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
    
    try:
        raw_text = html.select('.woocommerce-product-details__short-description')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
        
    if stamp['raw_text'] == None and stamp['title'] != None:
        stamp['raw_text'] = stamp['title']

    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date

    stamp['url'] = url
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.woocommerce-loop-product__link'):
            item_link = item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass

    try:
        next_item = html.select('a.next')[0]
        if next_item:
            next_url = next_item.get('href')
    except:
        pass
    
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories():
    
    url = 'https://ittybittystampcompany.com'
    
    items = {}

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.product-categories > li > a'):
            item_link = item.get('href')
            item_name_temp = item.get_text().strip()
            if ')' in item_name_temp:
                item_name_parts = item_name_temp.split(')')
                item_name = item_name_parts[1].strip()
            else:
                item_name = item_name_temp
            items[item_name] = item_link
    except: 
        pass
    
    return items

categories = get_categories()
for category_name in categories:
    print(category_name + ': ' + categories[category_name])   

selected_category_name = input('Choose category: ')
page_url = categories[selected_category_name]
while(page_url):
    page_items, page_url = get_page_items(page_url)
    for page_item in page_items:
            stamp = get_details(page_item)

