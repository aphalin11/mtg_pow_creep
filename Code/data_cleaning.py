# -*- coding: utf-8 -*-
"""
Data-Cleaning
"""

import pandas as pd 

# pulling unprocessed card data 
cards = pd.read_feather('Data/cards.feather')



## 
# quality check 1: duplications of cards 
##

# identify if there are any cards with multiple occurances 
quality_check = cards.groupby(['set', 'name']).agg(Occurances = ('name', 'count'))
quality_check.sort_values(by = 'Occurances', ascending = False)

# there's 10 cards with multiple reported prints 
dups = quality_check.query('Occurances > 1')
dups.shape

# since they all from unsets, and those aren't practical for this analysis we should filter them 
cards_without_un= cards[~cards['set'].str.contains('ust|unh|ugl|unf|und')]

# we dropped ~800 instances of cards filtering for 'unsets' 
cards.shape[0] - cards_without_un.shape[0] 

# final check on duplications of cards - we have no more duplications from the scryfall api 
quality_check = cards_without_un.groupby(['set', 'name']).agg(Occurances = ('name', 'count'))
dups = quality_check.query('Occurances > 1')
dups.shape
dups

# reassign cards without unset cards 
cards = cards_without_un 









##
# quality check 2: missing information
## 

# identify any anomalous card name or values 
missing_values = cards.isna().sum()
missing_values 


# important information - name, released_at, and set, do not have any missing information 







##
# quality check 4: colors column is a list 
## 

# the colors column is a listed with the pandas dataframe - for string capturing need to 
# convert this into a concatenated string 
cards['colors'] = cards['colors'].apply(lambda x: ', '.join(map(str, x)) if x is not None else '')







##
# quality check 3: upper-cases on string 
##

# a good portion of strings have some upper-case and some lower case values which can be problematic in captures 
# need to convert to lower-case 
cards = cards.applymap(lambda x: x.lower() if isinstance(x, str) else x)









##
# pushing processed data into feather file 
## 
cards = cards.reset_index() ## run this line if something funky goes on 
cards.to_feather('Data/cards_cleaned.feather')





































































































