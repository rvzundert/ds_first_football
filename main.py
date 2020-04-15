# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 16:36:17 2020

@author: r.van.zundert
"""
import transfermarkt as tf

data = tf.get_players("NL1", 250)
data.to_csv('D:/Projects/ds_first_football/transfermarkt_latest.csv', index=False)
