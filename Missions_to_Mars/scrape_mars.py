# coding: utf-8



##dependencies for Step1
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import time



def init_browser():
    ##path for chrome driver to use in browser
    executable_path = {"executable_path": "chromedriver_win32/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()

    time.sleep(10)    
    # # NASA Mars News
    ## where to get News information from
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)

    ## defined for news search
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

   
    ## need this line, without it news_title finds wrong item
    articles = soup.find_all('li', class_='slide')[0]


   ## select top of list for section named 'content_title'
    news_title = articles.find('div', class_='content_title').text

    ## search top of list for section called 'article_teaser_body'
    news_p = articles.find('div', class_='article_teaser_body').text

    # # JPL Mars Space Images - Featured Image

    ## where to get space images from
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    ## redefine for image search
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    ft_image= soup.find('article', class_="carousel_item")['style']
    image = ft_image.replace("background-image: url('",'')
    full_image = image.replace("');", '')
    

    featured_image_url = (f'https://www.jpl.nasa.gov{full_image}')

    # # Mars Facts

    ## where to get facts from
    url3 = 'https://space-facts.com/mars/'

    ## pandas table scrape
    tables = pd.read_html(url3)
    fact_df = pd.DataFrame(tables[0])

    fact_df.columns=['','Mars']
    facts_df = fact_df.set_index([''])
    
    html_string = fact_df.to_html()
    html_table=html_string.replace('\n','')

    # # Mars Hemispheres

    ## where to get hemisphere info
    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)

    time.sleep(10)
    ## redefine for hemisphere
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    ## what to loop through
    products = soup.find('div', class_='collapsible results')
    hemispheres = products.find_all('div',class_='item')

    ## what all image URLs start with
    url_start = 'https://astropedia.astrogeology.usgs.gov/'

    ## appendable list for "for" loops
    hemisphere_image_urls=[]

    ## loop to get URLs and images from the Products

    for hemisphere in hemispheres:
        dictionary= {}
        title = hemisphere.find('h3').text.strip()
        dictionary['title']= title
        hem_url = hemisphere.a['href']
        hem_url1 = hem_url.replace('/search/map','download')
        hem_url2 = hem_url1.replace('enhanced','enhanced.tif/full.jpg')
        dictionary['img_url']=url_start+ hem_url2
        hemisphere_image_urls.append(dictionary)

    mars_data={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
            }

    browser.quit()

    return mars_data