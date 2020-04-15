# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:36:17 2020

@author: r.van.zundert
"""
import sys
sys.path.append("D:/Projects/ds_first_football/")

import transfermarkt as tf
import transfermarkt_transfer_scraper as ts
data = tf.get_players("NL1", 250)
data.to_csv('D:/Projects/ds_first_football/transfermarkt_latest.csv', index=False)


transferData = ts.get_transfers('NL1', 2018)
transferData.to_csv('D:/Projects/ds_first_football/transfermarkt_transfers.csv', index=False)
