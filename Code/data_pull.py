"""
Initial API Pull to Scryfall API 
Output: All Magic! The Gathering Cards pulled from Scryfall's API, stored as cards.feather
"""

# Documentation on Scryfall's Card Object:  
# https://scryfall.com/docs/api/cards

import requests
import pandas as pd 
import os
      

# url used for API - a general search parameter to capture all cards (CMC >= 0) is used        
url = 'https://api.scryfall.com/cards/search?order=name&q=cmc>=0&page=' #request url for API

# initializing a list to compile all individual API page pulls and a count for loop
count = 1 #initial count used in loop 
datalist = list([])

# pulls all cards from API and prints card names each page (150 pages total as of 6/5/2023)
while True: 
    response = requests.get(url + str(count))
    data = response.json() #generates dictionary from json 

    if data['has_more'] == False:
        datalist = datalist + data['data'] 
        print('Pulled Page ' + str(count) + ' From results')
        cards = [data['name'] for data in data['data']]
        print(cards)
        print('Final Page was: ' + str(count))
        break 
    else: 
        datalist = datalist + data['data']
        print('Pulled Page ' + str(count) + ' From results')
        cards = [data['name'] for data in data['data']]
        print(cards)
        count += 1    
        
# processing json into a pandas dataframe 
df = pd.json_normalize(datalist)

# subsetting to only relevant columns 
only_good_stuff = df[['id', 'name', 'released_at', 'mana_cost', 'cmc', 
                      'type_line', 'oracle_text', 'power', 
                      'toughness', 'colors', 
                      'color_identity', 'keywords',
                      'foil', 'nonfoil', 'reprint', 'set', 
                      'set_name', 'set_type', 'rarity', 'artist', 
                      'edhrec_rank', 'legalities.commander', 'loyalty']]
    
# writing dataframe into a feather file for storage 
only_good_stuff.to_feather('cards.feather')





