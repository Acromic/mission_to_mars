# Import Splinter, BeautifulSoup, and Pandas
from more_itertools import sample
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
import requests

# Initiate headless driver for deployment
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=True)

# ------------add url for #2--------------------------------

#url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
url = 'https://marshemispheres.com/'

def scrape_all():
    # ------------------- Added challenge info -----------------
    # 2 Create a new dictionary to hold a list of dictionaries with the URL string and title of each hemishphere image
    browser.visit(url)
    #browser.visit(url + 'index.html')

    # 2 list

    hemisphere_image_urls = []

    # 2 find image to click and link
    posts = browser.find_by_css('a.product-item img') # a tag > img
    #print("Posts: ", posts)
    list_of_images = []

    #print("Post Length: ", len(posts))

    #hemisphere = {}

    2  # create 4 loop for the adds
    for post in range(len(posts)):

        # 2 dictionaries
        hemisphere = {}

        # 2 iterating thru post and add click
        browser.find_by_css('a.product-item img')[post].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']

        # Get hemisphere title
        title = browser.find_by_css('h2.title').text

        # Get Hemisphere title
        hemisphere['title'] = title
        print("Single Post: ", hemisphere)

        # append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)

         # finally navigate backwards
        browser.back()

# -------------------- Added challenge info -----------------

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": hemisphere_image_urls[0]['img_url'],
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemisphere_image_urls": hemisphere_image_urls
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")


if __name__ == "__main__":

    # If running as script, print scraped data
    print("All Data: ", scrape_all())

    # browser.quit()
