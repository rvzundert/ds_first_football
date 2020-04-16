# -*- coding: utf-8 -*-
"""
Created on Thu Apr 16 18:06:00 2020

@author: r.van.zundert
"""

import pandas as pd
import math
data = pd.read_csv('D:/Projects/ds_first_football/transfers_per_comp/transfermarkt_transfers_premier_league_1900-2020.csv')

data.columns

data['market_value_number'] = data['market_value'].apply(lambda x: x[1:])
data['market_value_number'] = data['market_value_number'].apply(lambda x: x if 'm' in x or x == None or x == '' else int(x[:-1]))
data['market_value_number'] = data['market_value_number'].apply(lambda x: float(x[:-1]) * 1000 if isinstance(x, str) and 'm' in x and x != None and x != '' else x)
data['market_value_number'] = data['market_value_number'].apply(lambda x: int(0) if x == None or isinstance(x, str) and x == '' else x)
data = data.drop(columns='market_value')


data['transfer_fee_number'] = data['transfer_fee'].apply(lambda x: float(x[1:][:-1]) * 1000 if str(x).startswith('€') and str(x).endswith('m') else x)
data['transfer_fee_number'] = data['transfer_fee_number'].apply(lambda x: float(x[1:][:-1]) if isinstance(x, str) and x.startswith('€') and x.endswith('k') else x)
data['transfer_fee_other'] = data['transfer_fee_number'].apply(lambda x: x if isinstance(x, str) else '')
data['transfer_fee_number'] = data['transfer_fee_number'].apply(lambda x: int(0) if isinstance(x, str) or math.isnan(x) else int(x))
data = data.drop(columns='transfer_fee')
data['player_age'] = data['player_age'].apply(lambda x: int(x) if str(x).isnumeric() else int(0))
data.to_csv('D:/Projects/ds_first_football/transfers_per_comp/transfermarkt_transfers_premier_league_1900-2020.csv-cleaned.csv')