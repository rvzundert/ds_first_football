# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:18:53 2020

@author: r.van.zundert
"""

from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
import time

def get_transfers(comp, year=datetime.now().year):
    if year < 1990:
        year = 1990
    
    options = webdriver.ChromeOptions()
    # options.add_argument('headless')

    driver = webdriver.Chrome(executable_path='D:/Projects/ds_first_football/chromedriver.exe', options=options)

    # year = 2015
    # comp='NL1'

    transfers = []
    while year <= datetime.now().year - 1:
        url = "https://www.transfermarkt.com/eredivisie/transfers/wettbewerb/"
        url += comp
        url += "/plus/?saison_id="
        url += str(year)
        url += "&s_w=&leihe=1&intern=0&intern=1"
        
        driver.get(url)
        
        print('Waiting 15 seconds to open season ' + str(year) + '/' + str(year + 1))
        time.sleep(15)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        container = soup.find('div', class_='large-8 columns')
        containerBoxes = container.find_all('div', class_='box', recursive=False)
        
        #loop through these boxes and filter out the ones which do not contain a clubs transfers
        for containerBox in containerBoxes:
            if containerBox.find('div', class_='header-social') != None or containerBox.find('div', class_='wappenleiste-box') != None:
                continue
            
            teamName = containerBox.find('div', class_='table-header').find('h2').find('a', class_='vereinprofil_tooltip').get_text()
            transferTables = containerBox.find_all('div', class_='responsive-table', recursive=False)
            transfersIn = transferTables[0]
            transfersOut = transferTables[1]
            
            for transferInRow in transfersIn.find('tbody').find_all('tr'):
                transfers.append(process_table_row(transferInRow, 'join', teamName, year))

        year += 1  
    return pd.DataFrame(transfers)        
            
def process_table_row(row, joinOrLeave, parsingTeam, year):
    
    columns = row.find_all('td')
    playerId = columns[0].find('a').get('id')
    playerName = columns[0].find('a').get_text()
    playerAge = columns[1].get_text()
    playerNationality = columns[2].find('img').get('alt')
    playerPosition = columns[3].get_text()
    #4th is player position short
    marketValue = columns[5].get_text()
    #6th contains image from team
    teamFromColumn = columns[7].find('a').get_text()
    transferFee = columns[8].find('a').get_text()
    
    fromTeam = teamFromColumn if joinOrLeave == 'leave' else parsingTeam
    toTeam = teamFromColumn if joinOrLeave == 'join' else parsingTeam
    
    return{
    'player_id' : playerId,
    'player_name': playerName,
    'player_position': playerPosition,
    'player_age' : playerAge,
    'player_nat' : playerNationality, 
    'from_team' : fromTeam,
    # 'from_competition' : fromCompetition, country..
    'to_team' : toTeam,
    # 'to_competition' : toCompetition,
    'market_value' : marketValue,
    'transfer_fee' : transferFee,
    'season' : str(year) + '/' + str(year + 1)
    }
