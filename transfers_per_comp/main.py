# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:36:17 2020

@author: r.van.zundert
"""
import sys
sys.path.append("D:/Projects/ds_first_football/transfers_per_comp/")

import transfermarkt_transfer_scraper as ts

#https://www.transfermarkt.com/eredivisie/transfers/wettbewerb/NL1
#https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1
#https://www.transfermarkt.com/1-bundesliga/transfers/wettbewerb/L1
url = 'https://www.transfermarkt.com/eredivisie/transfers/wettbewerb/NL1'   
league = 'eredivisie'
year = 1900

transferData = ts.get_transfers(url, year)
transferData.to_csv('D:/Projects/ds_first_football/transfers_per_comp/transfermarkt_transfers_' + league + '_' + str(year) + '-2020.csv', index=False)
