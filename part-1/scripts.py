# Imports
from requests import get
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime, timedelta
import pickle

# Constants
#SEARCH_URL = "https://poshmark.com/brand/Naked_&_Famous_Denim-Men-Jeans?sort_by=added_desc"
SEARCH_URL = "https://poshmark.com/brand/Naked_%26_Famous_Denim-Men-Jeans?sort_by=added_desc&size%5B%5D=28&all_size=false&my_size=false"
HEADER = { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
DAYS = 4

# Download and parse Poshmark listings
#this will take the search url we provide, pass it a header, and pull each card into an item_container.
#this actually just pulls the first 48 items, not by date.
def run_search(search_url):
    "Pull down search results and extract out product cards"
    response = get(search_url, headers=HEADER)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    item_container = html_soup.find_all('div', class_ = 'card card--small')
    #pretty sure each listing is a single item_container
    return item_container

product_cards = run_search(SEARCH_URL)
#print(product_cards)

## Extract product listing attributes

def get_attributes(soup_obj):
#   "Extract product values from card"
    url_tag = soup_obj.a

    #poshmarks hides the listing title in the images but doesn't populate the title field
    #so we'll have to pull the title from the image section
    img_tag = url_tag.img
    img = img_tag['src']

    #grab the listing title from the image section of the url_tag
    img_title = url_tag.img
    title = img_title['alt']
    #print("here's title", title)

    #get the text around the listing/retail prices, there's probably a better way to do this
    #but I'm learning so this works for now
    prices = soup_obj.select('div.m--t--1 span')
    #print("prices be:", prices)

    #get the listed price and strip the whitespace around it.
    listed_price=prices[0].text
    listed_price=listed_price.strip()
    #print("this is the listed price with no whitespace", listed_price)
    retail_price=prices[1].text
    retail_price=retail_price.strip()
    #print("this is the listed retail price:", retail_price)


    #Create the url
    url = "https://poshmark.com" + url_tag['href']
    # print("here's a url_Tag", url_tag)

    return (title, listed_price, url, img)

first_card = product_cards[0]
card_attributes = get_attributes(first_card)
print('Title: ', card_attributes[0])
print('Price: ', card_attributes[1])
print('url: ', card_attributes[2])
print('Image: ', card_attributes[3])

# Calculate the time difference
#def get_days(soup_obj):
#    "Convert to EST and return difference in days"
#    created_date = soup_obj['data-created-at']
#
#    pst_date = parse(created_date, ignoretz=True)
#    est_date = pst_date + timedelta(hours=3)

 #   now = datetime.now()
 #   diff = abs((est_date-now).days)

  #  return diff

#days = get_days(first_card)
# print(days)

# Find recent items
#recent_items = []

#for card in product_cards:
 #   difference = get_days(card)

  #  if difference <= DAYS:
   #     card_values = get_attributes(card)
    #    recent_items.append(card_values)
    #else:
     #   break

#summary = 'Found {} items posted in the last {} days'.format(len(recent_items), DAYS)
#print(summary)
#print('')

#for item in recent_items:
#    print('Title: ', item[0])
#    print('Price: ', item[1])
#    print('Link: ', item[2])
#    print('')

#pickle.dump(recent_items, open("naked_and_famous.p", "wb"))
