# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 21:00:23 2020

@author: r.van.zundert
"""


import pandas as pd
from datetime import datetime

data = pd.read_csv('transfermarkt_latest.csv')

data.columns

data['first_nationality'] = data['player_nats'].apply(lambda x: x.split(',')[0])
data['second_nationality'] = data['player_nats'].apply(lambda x: '' if len(x.split(',')) == 1 else x.split(',')[1])
data = data.drop(columns='player_nats')
data['market_value_number'] = data['market_value'].apply(lambda x: x[1:])
data['market_value_number'] = data['market_value_number'].apply(lambda x: x if 'm' in x or x == None or x == '' else int(x[:-1]))
data['market_value_number'] = data['market_value_number'].apply(lambda x: float(x[:-1]) * 1000 if isinstance(x, str) and 'm' in x and x != None and x != '' else x)
data['market_value_number'] = data['market_value_number'].apply(lambda x: int(0) if x == None or isinstance(x, str) and x == '' else x)
data = data.drop(columns='market_value')
data['transfer_date'] = data['transfer_date'].apply(lambda x: datetime.strptime(x.replace(',',''), '%b %d %Y'))
data['transfer_fee_number'] = data['transfer_fee'].apply(lambda x: float(x[1:][:-1]) * 1000 if x.startswith('€') and x.endswith('m') else x)
data['transfer_fee_number'] = data['transfer_fee_number'].apply(lambda x: float(x[1:][:-1]) if isinstance(x, str) and x.startswith('€') and x.endswith('k') else x)
data['transfer_fee_other'] = data['transfer_fee_number'].apply(lambda x: x if isinstance(x, str) else '')
data['transfer_fee_number'] = data['transfer_fee_number'].apply(lambda x: int(0) if isinstance(x, str) else int(x))
data = data.drop(columns='transfer_fee')
data.to_csv('D:/Projects/ds_first_football/transfermarkt_latest_cleaned.csv')
