# -*- coding: utf-8 -*-
"""
Summarizing the data by set for exploration of several metrics over time. 
"""

import pandas as pd 
import seaborn as sns 
import numpy as np 
from matplotlib import pyplot as plt 


# enable show all columns for data check 
pd.set_option('display.max_columns', None)


# pulling card data 
cards = pd.read_feather('Data/cards_cleaned.feather')
cards.info()



##
# making temporary binary feature for aggregation
##

# card types binaries 
cards['nonland_spell'] = cards['type_line'].str.contains('land') == False 
cards['creature'] = cards['type_line'].str.contains('creature')
cards['enchantment'] = cards['type_line'].str.contains('enchantment') 
cards['artifact'] = cards['type_line'].str.contains('artifact') 
cards['instant_sorcery'] = cards['type_line'].str.contains('instant|sorcery') 
cards['planeswalkers'] = cards['type_line'].str.contains('planeswalk')

# card color binaries 
cards['blue'] = cards['colors'].str.contains('u') 
cards['black'] = cards['colors'].str.contains('b')
cards['white'] = cards['colors'].str.contains('w')
cards['green']= cards['colors'].str.contains('g')
cards['red'] = cards['colors'].str.contains('r')





##
# aggregating into a set-level table using conditional functions and agg 
## 

# conditional function for total non-reprints (sum of bool is a count)
def total_non_reprints(x): 
    return(sum(x == False))

# conditional function for total non-land cards 
def total_non_land(x): 
    return(sum(x == True))

# generating a set-level summary table 
set_agg = cards.groupby('set').agg(
    release_date = ('released_at', max), 
    total_cards = ('name', 'nunique'), 
    total_non_reprints = ('reprint', total_non_reprints), 
    total_non_lands = ('nonland_spell', total_non_land),
    average_nonland_cmc = ('cmc', 'mean'),  # need logic to define non-land 
    highest_nonland_cmc = ('cmc', max), 
    total_creatures = ('creature', sum), 
    total_enchantments = ('enchantment', sum), 
    total_artifacts = ('artifact', sum), 
    total_instant_sorceries = ('instant_sorcery', sum), 
    total_planeswalkers = ('planeswalkers', sum), 
    total_foils = ('foil', sum), # total count of cards with foil prints
    total_white = ('white', sum), 
    total_blue = ('blue', sum), 
    total_black = ('black', sum), 
    total_red = ('red', sum), 
    total_green = ('green', sum), 
    average_edhrec_legendaries = ('edhrec_rank', 'mean'), 
    highest_edhrec_legendaries = ('edhrec_rank', max), 
    lowest_edhrec_legendaries = ('edhrec_rank', min)  
)

set_agg.sort_values(by = 'release_date').head(10)


# secondary aggregation step to calculate % of totals 
set_agg
set_agg[['percent_creatures', 'percent_foils',
         'percent_white', 'percent_blue', 'percent_black', 
         'percent_green', 'percent_red']] =   [(set_agg['total_creatures'] / set_agg['total_cards']) * 100, 
     (set_agg['total_foils'] / set_agg['total_cards']) * 100, 
     (set_agg['total_white'] / set_agg['total_cards']) * 100, 
     (set_agg['total_blue'] / set_agg['total_cards']) * 100, 
     (set_agg['total_green'] / set_agg['total_cards']) * 100, 
     (set_agg['total_red'] / set_agg['total_cards']) * 100]




## 
# visualizing total cards by set and release date 
## 

set_agg.info()
set_agg.head(2)

sns.lineplot(data = set_agg, x = 'release_date', y = 'total_cards')
sns.set_style("dark", {'axes.grid' : False})

ticks = plt.gca().get_xticks()
first_date = min(set_agg['release_date'])
date_quart = np.quantile(set_agg['release_date'], 0.25)
last_date = max(set_agg['release_date'])
plt.gca().set_xticks([ticks[0], ticks[-1]])
plt.gca().set_xticklabels([first_date, last_date])

plt.xlabel('Set Release Date')
plt.ylabel('Total Cards Printed')
plt.title('Cards Printed by Set Date')
plt.xticks(rotation = 45)

































































































