# -*- coding: utf-8 -*-
"""
Initial EDA Document
"""

import pandas as pd 
import seaborn as sns 
import matplotlib as plt 

# pulling card data 
cards = pd.read_feather('cards.feather')