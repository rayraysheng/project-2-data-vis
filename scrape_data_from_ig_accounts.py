
# coding: utf-8

# In[ ]:


# Import dependencies
from bs4 import BeautifulSoup
import time
import numpy as np
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from collections import Counter


# In[ ]:


def scrape(account_name):
    
    # Fill in the brand account name to assemble the url
    brand_account_name = account_name
    url = f'https://instagram.com/{brand_account_name}/'
    
    # Visit the profile page
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Record the account info
    
    ## Get post count, follower count, following count
    stat_elements = driver.find_elements_by_class_name('_t98z6')

    post_count = int(stat_elements[0].text.split('posts')[0].replace(',', ''))
    following_count = int(stat_elements[2].text.split('following')[0].replace(',', ''))

    follower_count_broth = stat_elements[1].get_attribute('innerHTML')
    follower_soup = BeautifulSoup(follower_count_broth, 'html.parser')
    follower_count = int(follower_soup.find('span')['title'].replace(',', ''))
    
    # Set up list to contain post urls
    post_urls_list = []

    # Scrape the topmost posts that show up immediately
    # and save the urls to the list
    # Locate the gallery region of the page
    gallery = driver.find_elements_by_css_selector('._havey')[0]
    # Save the anchor tags for posts in a list
    posts_list = gallery.find_elements_by_css_selector('a')

    
    for post in posts_list:

        post_link = post.get_attribute('href')

        if post_link not in post_urls_list:
            post_urls_list.append(post_link)
    
    # Scroll through the rest of the profile to scrape every post
    while len(post_urls_list) < post_count:

        # Scroll to the bottom to and wait to load more posts
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

        # When the browser has trouble loading, 
        # there may be a pop up to click to retry
        try:
            driver.find_element_by_link_text('Retry').click()
        except:
            pass

        # To compare the url list before and after appending
        previous_list_length = len(post_urls_list)

        # Scrape and append
        # Locate the gallery region of the page
        gallery = driver.find_elements_by_css_selector('._havey')[0]
        # Save the anchor tags for posts in a list
        posts_list = gallery.find_elements_by_css_selector('a')

    
        for post in posts_list:

            post_link = post.get_attribute('href')

            if post_link not in post_urls_list:
                post_urls_list.append(post_link)

        # To compare the url list before and after appending
        current_list_length = len(post_urls_list)

        # If the list didn't change:
        ## Scroll up a little and wait, there may be a timeout
        if current_list_length == previous_list_length:
            driver.execute_script("window.scrollBy(0, -1000);")
            time.sleep(10)

        # Check progress
        time_check = datetime.strftime(datetime.now(), '%I: %M: %S.%f')
        print(f'{account_name} -- {time_check}: {current_list_length} of {post_count}')
    
    # Return the data if the profile doesn't have a bio link
    return {
        'account_name': account_name,
        'instagram_url': url,
        'post_count': post_count,
        'follower_count': follower_count,
        'following_count': following_count,
        'post_urls_list': post_urls_list
    }


# In[ ]:


# Here are the account names
accounts_list = [
    'burberry',
    'gucci',
    'toryburch',
    'michaelkors',
    'bananarepublic',
    'majeofficiel',
    'aliceandolivia',
    'coach',
    'ferragamo',
    'chloe'
]


# In[ ]:


# Iterate through the accounts and scrape
for account in accounts_list:
    
    data_dict = scrape(account)
    
    with open(f'{account}.json', 'w') as file:
        json.dump(data_dict, file)

