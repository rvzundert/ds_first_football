# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:36:17 2020

@author: r.van.zundert
"""
import sys
sys.path.append("D:/Projects/ds_first_football/transfers_per_comp/")

import transfermarkt_transfer_scraper as ts

transferData = ts.get_transfers('NL1', 2018)
transferData.to_csv('D:/Projects/ds_first_football/transfers_per_comp/transfermarkt_transfers.csv', index=False)
