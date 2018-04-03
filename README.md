# Project-2-data-vis

Topic: Analyses of Fashion Brands on Instagram

# Data Set: 
Web scraping from instagram website into json files for ten hand-picked fashion brand accounts, including both premier and contemporary brands

# Time scope for post analyses:  
01/01/2014 - 03/01/2018

# Inspirations / Questions: 
Assume that we are a marketing consultant company who is going to help a new big fashion brand company to establish their social media strategy. The goal of this project is to analyze how to build an instagram account with more followers / more likes (assumption: more followers / more likes of posting → brings more business to the company) 
## Why some brands have more user followers on instagrams than others?
The factors that might matter:
Posting schedule: including the post frequency / time of the day of postings
Total post counts (the number of user followers might be linear to the total amount of post - this also depends on the history of the brand of using instagram)
Hashtags
Posting contents?  - eg: celebrities in the pics? / more vibrant colors?  

## Why some posts get more likes than others？
Comparison between different accounts - Some interesting findings: for example, Michael Kors has got almost the same amount of followers as Burberry, but almost every post of MK gets like 2-3 times more “likes” than Burberry. What is the reason? usage of hashtags? # of hashtags?
Comparison within the account: 
Assumptions - will explore the correlations of these factors with the “likes”
relatively a video posting would bring more likes / views
multiple picture posting would get more likes 
pics with the founder of the brand would get more likes 
pics with more descriptions would get more likes
pics with usage of hashtags would bring more likes

# Ideal Visuals:

## Plots:

Bubble chart - each account is assigned for one bubble 
X-axis: post frequency 
Y-axis: # of likes in total or per follower
Use bubble size to present the number of followers for each account
Conclusion: would more active posting lead to more likes? 
Note: total likes per follower is the normalization process, which would show that how active your user followers (or the percentage of your followers) actually interact with your posts. 

## Bar chart:
X-axis: Day of the week
Y-axis: number of the posts
Dropdown menu to switch brands

## Bar chart #2: 
The same one as last one, but Y-axis is the total number of “likes”
We can do by each brand, or by the aggregated number of likes in total, so as to see if the day of posting would affect the user interactions? 
Conclusion: would certain days of week be a better choice for posting? - > more interactions with your users? 

## Scatter chart:
X-axis: # of hashtags
Y-axis: # of likes or  # of likes / # of followers 
drop -down menu for each brand
Conclusion: would more hashtags lead to more "likes"?

## Bar chart:
X-axis: Album vs. Video vs. 1 Picture 
Y-axis: # of likes or # of likes / # of flowers 
Conclusion: would Album or videos attract more attentions than 1 photo post?

## Color analysis: 
Visualize the “color palette/distribution” for the most recent posts of each brand: 
We plan to extract images from the instagram account of these brands (the recent 2018 ones), and based on that, we want to be able to tell the color trends for the 2018 spring/summer. Further more, if possible, we would like to link the number of “likes” to the color pattern we extract, so that we would tell what type of color is more favored this year. The platte(bubble) size will be different according to the frequent usage or popularity; if we hover on each color it will show the percentage of “likes”, and how often the brands are using this color on instagram. 

### Summary of useful color analysis JS libraries: 
Get-image-colors: https://www.npmjs.com/package/get-image-colors 
The most comprehensive library tool that outputs the hex of all colors in each image
Colorify: http://colorify.rocks/index.html#getMainColor 
A mini color tool that can realize different functions, including extracting the main color in the image
Rgbaster: https://www.npmjs.com/package/rgbaster  
A more straightforward tool to just get the dominant color in the image
Vibrant: http://jariz.github.io/vibrant.js/  
A library that can output the vibrant/muted/dark colors etc..

Links to explore: 
http://mkweb.bcgsc.ca/color-summarizer/?examples
