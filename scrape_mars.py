
#load dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
import time

def scrape():


    #open google browser
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # # NASA MARS NEWS

    #connect to url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    # results are returned as an iterable list
    news_title = []
    news_p = []
    results = soup.find_all('li', class_='slide')

    # Loop through returned results
    for result in results:
        # Error handling
        try:
            titles = result.find('div', class_='content_title').text
            time.sleep(.2)
            ps = result.find('div', class_='article_teaser_body').text
            news_title.append(titles)
            news_p.append(ps)

        except AttributeError as e:
            print('')


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    img = soup.find("a", class_ = "button fancybox")['data-fancybox-href']
    featured_image_url = f'https://www.jpl.nasa.gov/{img}'

    # # Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = []

    for tag in soup.find_all(class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
        info = tag.text
        mars_weather.append(info)

    # # Mars Facts

    # Scrape the table of Mars facts
    facts_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(facts_url)
    df = tables[0]
    df.columns = ['fact', 'info']
    df = pd.DataFrame(data = df)
    df = df.set_index('fact')

    # Convert to HTML table string
    df = df.to_html()
    facts_table = df
    
    # # Mars Hemispheres

    base_hemisphere_url = "https://astrogeology.usgs.gov" #store this for later in the forloop
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
        
    hemisphere_image_urls = []

    results = soup.find_all("div", class_="item")
    hemisphere_image_urls = []

    for result in results:
        img_dict = {}
        title = result.find("h3").text
        next_link = result.find("div", class_="description").a["href"]
        full_next_link = base_hemisphere_url + next_link
        
        browser.visit(full_next_link)
        
        img_html = browser.html
        img_soup = BeautifulSoup(img_html, 'html.parser')
        
        url = img_soup.find("img", class_="wide-image")["src"]

        img_dict["title"] = title
        img_dict["img_url"] = base_hemisphere_url + url
        
        hemisphere_image_urls.append(img_dict)


        # Store data in a dictionary
    mars_data = {
    "news_title": news_title,
    "news_p": news_p,
    "featured_image_url": featured_image_url,
    "mars_weather": mars_weather,
    "facts_table" : facts_table,
    "hemisphere_urls": hemisphere_image_urls

    }   

            # Close the browser after scraping
    browser.quit()

         # Return results
    return mars_data




