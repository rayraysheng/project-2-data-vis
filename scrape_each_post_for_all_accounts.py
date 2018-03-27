
# coding: utf-8

# In[1]:


# Import dependencies
from bs4 import BeautifulSoup
import time
import numpy as np
from datetime import datetime
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as bs


# In[2]:


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


# Iterate through each account and let the code do its thang

# Use this to check whether or not the page has refreshed
# in case of running into rate-limiting issues
refresh_check = 'initial string, does not matter'

for account_name in accounts_list:
    
    # Load the json file to read the urls list
    account_data_dict = json.load(open(f'data/{account_name}.json'))
    post_urls_list = account_data_dict['post_urls_list']

    # Initiate a list to keep the post data
    post_data_list = []

    #Initiate browser
    driver = webdriver.Chrome()

    # Loop through the posts and scrape data
    for post_url in post_urls_list:

        # Visit post
        driver.get(post_url)

        # Fetch like or view count
        ## Keep placeholders for like and view counts
        like_count = None
        view_count = None

        try:
            # If the page has a '_nzn1h' class div, then it's a photo
            ## Find the tag that contains the like count string
            like_count_str = driver.find_elements_by_class_name('_nzn1h')[0].text
            ## Parse the string to get a numeric like count
            like_count = int(like_count_str.split(' ')[0].replace(',', ''))
        except:
            # If it doesn't, then it's a video
            ## Find the tag that contains the view count string
            view_count_str = driver.find_elements_by_class_name('_m5zti')[0].text
            ## Parse the string to get a numeric view count
            view_count = int(view_count_str.split(' ')[0].replace(',', ''))

        # See if the post is a album, by looking for the next button
        next_button_list = driver.find_elements_by_class_name('coreSpriteRightChevron')

        if len(next_button_list) > 0:   # Check for next button
            post_type = 'album'
        elif like_count in locals():   # Check for like count
            post_type = 'photo'
        else:
            post_type = 'video'

        # Fetch post datetime
        ## Use BeautifulSoup to find the hidden datetime attribute
        post_time_broth = driver.find_elements_by_class_name('_djdmk')[0].get_attribute('innerHTML')
        post_time_soup = bs(post_time_broth, 'html.parser')
        post_datetime_str = post_time_soup.find('time')['datetime']

        # Record the caption word count and number of hastags/@s
        ## Fetch everything in the caption area
        caption_str = driver.find_elements_by_class_name('_ezgzd')[0].text
        ## Split the whole string into a list of words
        caption_word_list = caption_str.replace('\n', ' ').replace('.', '')        .replace(',', '').replace('!', '').replace('?', '').split(' ')
        caption_length = len(caption_word_list)
        ## Derive the hashtag and @ data
        has_hashtag = False
        hashtag_count = 0

        has_at = False
        at_count = 0

        ## Iterate through the caption words to count hashtags and @s
        for each in caption_word_list:
            if '#' in each:
                hashtag_count += 1
            elif '@' in each:
                at_count += 1
            else:
                pass

        ## Record whether or the post has hashtags and @s
        if hashtag_count > 0:
            has_hashtag = True

        if at_count > 0:
            has_at = True

        # Construct the dictionary to hold post data
        post_data_dict = {
            'post_url': post_url,
            'like_count': like_count,
            'view_count': view_count,
            'post_type': post_type,
            'post_datetime_str': post_datetime_str,
            'has_hashtag': has_hashtag,
            'hashtag_count': hashtag_count,
            'has_at': has_at,
            'at_count': at_count
        }

        # Update post data list
        # but only if it's not a repeat.
        # A repeat would indicate the new page did not load,
        # meaning that we're being rate-limited
        if post_data_dict not in post_data_list:
            post_data_list.append(post_data_dict)
        # Wait for 10 minutes if rate-limited
        else:
            time.sleep(60 * 10)

        # Keep track of progress
        already_recorded = len(post_data_list)
        total_to_record = len(post_urls_list)
        time_check = datetime.strftime(datetime.now(), '%I: %M: %S.%f')
        print(f'{account_name} -- {time_check}: {already_recorded} of {total_to_record}')

    # CLose the browser at the end
    driver.close()

    # Append account data dictionary and save to new json file
    account_data_dict = json.load(open(f'data/{account_name}.json'))
    account_data_dict['post_data_list'] = post_data_list

    with open(f'appended_{account_name}.json', 'w') as file:
            json.dump(account_data_dict, file)

