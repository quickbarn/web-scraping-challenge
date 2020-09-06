#!/usr/bin/env python
# coding: utf-8

# In[1]:


##dependencies for Step1
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
from splinter.exceptions import ElementDoesNotExist
import time


# In[2]:


##path for chrome driver to use in browser
executable_path = {"executable_path": "chromedriver_win32/chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)


# # NASA Mars News

# In[3]:


## where to get News information from
url1 = 'https://mars.nasa.gov/news/'
browser.visit(url1)


# In[4]:


## defined for news search
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


## make an article list, set index to zero for first item of list, start searching where articles start <ul>
## need this line, without it news_title finds wrong item
article = soup.find_all('ul', class_='item_list')[0]


# In[6]:


## search top of list for section called 'content_title'
news_title = article.find(class_='content_title').text


# In[7]:


## search top of list for section called 'article_teaser_body'
news_p = article.find(class_='article_teaser_body').text


# In[8]:


print(f'news_title= "{news_title}"')
print(f'news_p= "{news_p}"')


# # JPL Mars Space Images - Featured Image

# In[9]:


## where to get space images from
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)


# In[10]:


## redefine for image search
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[11]:


ft_image= soup.find('a', class_='button fancybox')['data-fancybox-href']
full_image = ft_image.replace('mediumsize','largesize')
full_image


# In[12]:


featured_image_url = (f'https://www.jpl.nasa.gov{full_image}')
featured_image_url


# # Mars Facts

# In[13]:


## where to get facts from
url3 = 'https://space-facts.com/mars/'
# browser.visit(url3)


# In[14]:


## pandas table scrape
tables = pd.read_html(url3)
fact_df = pd.DataFrame(tables[0])
fact_df


# In[15]:


html_string = fact_df.to_html()
html_table=html_string.replace('\n','')


# In[16]:


html_table


# # Mars Hemispheres

# In[17]:


## where to get hemisphere info
url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url4)


# In[18]:


## redefine for hemisphere
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[19]:


## what to loop through
products = soup.find('div', class_='collapsible results')
hemispheres = products.find_all('div',class_='item')


# In[20]:


## what all image URLs start with
url_start = 'https://astrogeology.usgs.gov/'


# In[21]:


## appendable list for "for" loops
hemisphere_image_urls=[]


# In[22]:


## loop to get URLs and images from the Products
time.sleep(5)
for hemisphere in hemispheres:
    dictionary= {}
    title = hemisphere.find('h3').text.strip()
    dictionary['title']= title
    hem_url = hemisphere.find('img')['src']
    hemi_url = hem_url.replace('thumb','full')
    dictionary['img_url']=url_start+ hemi_url
    hemisphere_image_urls.append(dictionary)


# In[23]:


hemisphere_image_urls


# In[ ]:




