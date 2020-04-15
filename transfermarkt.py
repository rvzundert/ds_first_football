# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:50:47 2020

@author: r.van.zundert
"""
import requests
from bs4 import BeautifulSoup

url = "https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&wettbewerb_id=NL1&land_id=&minMarktwert=0&maxMarktwert=200.000.000"
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
playerRows = soup.find("table",  class_='items').find("tbody").find_all("tr", recursive=False)
playerRows.pop(0)

for player in playerRows:
    allColumns = player.find_all('td', recursive=False)
    playerName = player.find('a').get_text()
    playerAge = allColumns[1].get_text()
    playerNationalities = allColumns[2].find_all('img')[0]#.getattr('alt')
    print(playerName + ' ' + playerAge + ' ' + playerNationalities)