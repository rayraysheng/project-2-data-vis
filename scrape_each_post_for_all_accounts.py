
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
    'toryburch',
    'michaelkors',
    'bananarepublic',
    'aliceandolivia',
    'coach',
    'ferragamo',
    'chloe',
    'gucci'
]


# In[ ]:


# Iterate through each account and let the code do its thang
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

    # This section of the code fetches likes or views count

        # Keep placeholders for like and view counts
        like_count = None
        view_count = None

        # Check to see if the post has likes or views
        like_area_as_list = driver.find_elements_by_class_name('_nt9ow')
        view_area_as_list = driver.find_elements_by_class_name('_sokb7')

        # For posts that have likes
        if len(like_area_as_list) > 0:
            # Post shows like count only if there are enough likes
            like_count_as_list = driver.find_elements_by_class_name('_nzn1h')

            # If there's a like count shown, just scrape and parse
            if len(like_count_as_list) > 0:
                like_count_str = driver.find_elements_by_class_name('_nzn1h')[0].text
                like_count = int(like_count_str.split(' ')[0].replace(',', ''))
            # If not enough likes, count how many users clicked like
            else:
                liked_users_list = driver.find_elements_by_class_name('_de460')
                like_count = len(liked_users_list)

        # For posts that have views
        elif len(view_area_as_list) > 0:

            # As long as there are views, a numeric value will show
            view_count_as_list = driver.find_elements_by_class_name('_m5zti')

            # Just scrape and parse
            if len(view_count_as_list) > 0:
                view_count_str = driver.find_elements_by_class_name('_m5zti')[0].text
                view_count = int(view_count_str.split(' ')[0].replace(',', ''))

    # This section of the code checks for post type

        # See if the post is an album, by looking for the next button
        next_button_as_list = driver.find_elements_by_class_name('coreSpriteRightChevron')
        
        # See if the post if a video, by looking for the play button
        play_button_as_list = driver.find_elements_by_class_name('_7thjo')
        
        # Assign post type
        if len(next_button_as_list) > 0:   # Check for next button
            post_type = 'album'
        elif len(play_button_as_list) > 0:   # Check for play button
            post_type = 'video'
        else:
            post_type = 'photo'
        
    # This section of the code fetches post datetime

        # Use BeautifulSoup to find the hidden datetime attribute
        post_datetime_str = None

        try:
            post_time_broth = driver.find_elements_by_class_name('_djdmk')[0].get_attribute('innerHTML')
            post_time_soup = bs(post_time_broth, 'html.parser')
            post_datetime_str = post_time_soup.find('time')['datetime']
        except:
            pass
        
    # This section of the code gets the caption word count and number of hastags/@s

        # Set up an empty caption word list in case if the '_ezgzd' div doesn't exist
        # i.e. there's nothing in the catpion area
        caption_word_list = []

        # Fetch everything in the caption area if one exists
        caption_as_list = driver.find_elements_by_class_name('_ezgzd')

        if len(caption_as_list) > 0:
            caption_str = caption_as_list[0].text
            ## Split the whole string into a list of words
            caption_word_list = caption_str.replace('\n', ' ').replace('.', '')        .replace(',', '').replace('!', '').replace('?', '').split(' ')
            
        caption_length = len(caption_word_list)
            
        # Derive the hashtag and @ data
        has_hashtag = False
        hashtag_count = 0

        has_at = False
        at_count = 0
        
        # Iterate through the caption words to count hashtags and @s
        for each in caption_word_list:
            if '#' in each:
                hashtag_count += 1
            elif '@' in each:
                at_count += 1
            else:
                pass

        # Record whether or the post has hashtags and @s
        if hashtag_count > 0:
            has_hashtag = True
        
        if at_count > 0:
            has_at = True

    # This section of the codes saves the record

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
        post_data_list.append(post_data_dict)
        
    # This section of the code keeps track of progress
        already_recorded = len(post_data_list)
        total_to_record = len(post_urls_list)
        time_check = datetime.strftime(datetime.now(), '%I: %M: %S.%f')
        print(f'{account_name} -- {time_check}: {already_recorded} of {total_to_record} -- {post_type}')

    # CLose the browser at the end
    driver.close()


    # In[ ]:


    # Append account data dictionary and save to new json file
    account_data_dict = json.load(open(f'data/{account_name}.json'))
    account_data_dict['post_data_list'] = post_data_list

    with open(f'data/appended/appended_{account_name}.json', 'w') as file:
        json.dump(account_data_dict, file)

