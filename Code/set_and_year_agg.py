# -*- coding: utf-8 -*-
"""
Summarizing the data by set for exploration of several metrics over time. 
"""

import pandas as pd 
import seaborn as sns 
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

# conditional function for total land cards
def total_land(x): 
    return(sum(x == False))

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
    total_lands = ('nonland_spell', total_land),
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
last_date = max(set_agg['release_date'])
plt.gca().set_xticks([ticks[0], ticks[-1]])
plt.gca().set_xticklabels([first_date, last_date])

plt.xlabel('Set Release Date')
plt.ylabel('Total Cards Printed')
plt.ylim(0, 400)
plt.title('Cards Printed by Set Date')
plt.xticks(rotation = 45)
plt.show() 




##
# aggregating to a year-level 
##
year_agg = cards.groupby('year').agg(
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
    total_lands = ('nonland_spell', total_land),
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





##
#  card prints by year 
##

# plotting all cards, including reprints 
sns.lineplot(data = year_agg, x = 'year', y = 'total_cards')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('Total Cards Printed')
plt.title('Cards Printed by Set Date')
plt.xticks(rotation = 45)
plt.show() 


# plotting excluding reprints 
sns.lineplot(data = year_agg, x = 'year', y = 'total_non_reprints')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('Total Cards Printed')
plt.title('Cards Printed by Set Date')
plt.xticks(rotation = 45)
plt.show() 

# plotting average cmc 
sns.lineplot(data = year_agg, x = 'year', y = 'average_nonland_cmc')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('CMC')
plt.title('Average CMC of Non-Land Spells by Set Year')
plt.xticks(rotation = 45)
plt.show() 

# plotting color of spells by year 
plt.plot(year_agg.index, year_agg['total_white'], label = 'White Cards')
plt.plot(year_agg.index, year_agg['total_blue'], label = 'Blue Cards')
plt.plot(year_agg.index, year_agg['total_red'], label = 'Red Cards') 
plt.plot(year_agg.index, year_agg['total_green'], label = 'Green Cards')
plt.plot(year_agg.index, year_agg['total_black'], label = 'Black Cards')
plt.xlabel('Set Year')
plt.ylabel('Total Cards Released')
plt.title('Total Cards Printed by Color and Set Year')
plt.legend()
plt.show()

# plotting card types by year 
plt.plot(year_agg.index, year_agg['total_creatures'], label = 'Creatures')
plt.plot(year_agg.index, year_agg['total_enchantments'], label = 'Enchantments')
plt.plot(year_agg.index, year_agg['total_artifacts'], label = 'Artifacts') 
plt.plot(year_agg.index, year_agg['total_planeswalkers'], label = 'Planeswalkers')
plt.plot(year_agg.index, year_agg['total_instant_sorceries'], label = 'Instants/Sorceries')
plt.plot(year_agg.index, year_agg['total_lands'], label = 'Lands')
plt.xlabel('Set Year')
plt.ylabel('Total Cards Released')
plt.title('Total Cards Printed by Card Type and Set Year')
plt.legend()
plt.show()

# card types by year - resizing axes 
sns.set_style("dark", {'axes.grid' : True})
plt.plot(year_agg.index, year_agg['total_creatures'], label = 'Creatures')
plt.plot(year_agg.index, year_agg['total_enchantments'], label = 'Enchantments')
plt.plot(year_agg.index, year_agg['total_artifacts'], label = 'Artifacts') 
plt.plot(year_agg.index, year_agg['total_planeswalkers'], label = 'Planeswalkers')
plt.plot(year_agg.index, year_agg['total_instant_sorceries'], label = 'Instants/Sorceries')
plt.plot(year_agg.index, year_agg['total_lands'], label = 'Lands')
plt.xlabel('Set Year')
plt.ylabel('Total Cards Released')
plt.xlim(2015, 2023)
plt.title('Total Cards Printed by Card Type and Set Year (Recent Years)')
plt.legend()
plt.show()

# card types by year - resizing axes 
sns.set_style("dark", {'axes.grid' : True})
plt.plot(year_agg.index, year_agg['average_edhrec_legendaries'], label = 'Average Rank')
plt.plot(year_agg.index, year_agg['highest_edhrec_legendaries'], label = 'Highest Rank')
plt.xlabel('Set Year')
plt.ylabel('EDHREC Rank')
plt.xlim(2010, 2023)
plt.title('Current EDHREC Rank of Legendaries by Set Year (Highest and Average)')
plt.legend()
plt.show()


cards.query('edhrec_rank > 0 & year == 2015')[['name', 'edhrec_rank', 'type_line']].sort_values(by = 'edhrec_rank').head(50)




##
# aggregating to a year-level and removing reprints 
##
year_agg_nrp = cards.query('reprint == False').groupby('year').agg(
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
    total_lands = ('nonland_spell', total_land),
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

# edhrec rankings (excluding reprints)
sns.set_style("dark", {'axes.grid' : True})
plt.plot(year_agg_nrp.index, year_agg_nrp['average_edhrec_legendaries'], label = 'Average Rank')
plt.plot(year_agg_nrp.index, year_agg_nrp['highest_edhrec_legendaries'], label = 'Highest Rank')
plt.xlabel('Set Year')
plt.ylabel('EDHREC Rank')
plt.xlim(2010, 2023)
plt.title('Current EDHREC Rank of Cards by Set Year (Highest and Average) - Reprints Excluded')
plt.legend()
plt.show()

# non-land cmc averages (excluding reprints)
sns.lineplot(data = year_agg_nrp, x = 'year', y = 'average_nonland_cmc')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('CMC')
plt.title('Average CMC of Non-Land Spells by Set Year')
plt.xticks(rotation = 45)
plt.show() 

# plotting edhrec averages and total number of cards 
plt.plot(year_agg_nrp.index, year_agg_nrp['total_cards'], label = 'Total Cards Printed')
plt.plot(year_agg_nrp.index, year_agg_nrp['average_edhrec_legendaries'], label = 'Average EDHREC Rank')
plt.xlabel('Set Year')
plt.ylabel('Total Cards Released')
plt.title('Total Cards Printed by Card Type and Set Year')
plt.xlim(2015, 2023)
plt.legend()
plt.show()

# plotting all cards printed 
sns.lineplot(data = year_agg_nrp, x = 'year', y = 'total_cards')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('Total Cards Printed')
plt.title('Cards Printed by Set Date, Excluding Reprints and Only Recent Years')
plt.xlim(2015, 2023)
plt.xticks(rotation = 45)
plt.show() 

# plotting average edhrec 
sns.lineplot(data = year_agg_nrp, x = 'year', y = 'average_edhrec_legendaries')
sns.set_style("dark", {'axes.grid' : False})
plt.xlabel('Set Year')
plt.ylabel('EDHREC Rank')
plt.title('Average EDHREC Rank by Set Date, Excluding Reprints and Only Recent Years')
plt.xlim(2015, 2023)
plt.xticks(rotation = 45)
plt.show() 























































































