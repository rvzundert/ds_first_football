# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 23:18:53 2020
https://www.transfermarkt.com/eredivisie/transfers/wettbewerb/NL1/plus/?saison_id=1987&s_w=&leihe=1&intern=0&intern=1
@author: r.van.zundert
"""

from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def get_transfers(url, year = datetime.now().year):
    
    if year < 1900:
        year = 1900
        
    # year = 2019
    baseUrl = url
    # baseUrl = 'https://www.transfermarkt.com/premier-league/transfers/wettbewerb/GB1'   

    transfers = []
    while year <= datetime.now().year:
        season = str(year) + '/' + str(year + 1)
        url = baseUrl
        url += "/plus/?saison_id="
        url += str(year)
        url += "&s_w=&leihe=1&intern=0&intern=1"
        headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}
        
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'html.parser')    
        
        country = soup.find('table', class_='profilheader').find('img').get('title')
        
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
            
            transferInRows = transfersIn.find('tbody').find_all('tr')
            if len(transferInRows) == 1:
                continue
            
            transferOutRows = transfersOut.find('tbody').find_all('tr')
            if len(transferOutRows) == 1:
                continue
            
            for transferInRow in transferInRows:
                transfers.append(process_table_row(transferInRow, True, teamName, season, country))
            
            for transferOutRow in transferOutRows:
                transfers.append(process_table_row(transferOutRow, False, teamName, season, country))
                
        print('Processed transfers of season: ' + season + ' current total transfers: ' + str(len(transfers)))
        year += 1
        data = pd.DataFrame(transfers)        
    return pd.DataFrame(transfers)        
            
def process_table_row(row, incoming, parsingTeam, season, country):
    
    columns = row.find_all('td')
    playerId = columns[0].find('a').get('id')
    playerName = columns[0].find('a').get_text()
    playerAge = columns[1].get_text()
    nationalityColumn = columns[2].find('img')
    if nationalityColumn != None:
        playerNationality = nationalityColumn.get('alt')
    else:
        playerNationality = ''
    playerPosition = columns[3].get_text()
    #4th is player position short
    marketValue = columns[5].get_text()
    #6th contains image from team
    teamColumn = columns[7].find('a').get_text()
    teamColumnImage = columns[7].find('img')
    if teamColumnImage != None:
        teamColumnCountry = teamColumnImage.get('title')
    else:
        teamColumnCountry = ''
    transferFee = columns[8].find('a').get_text()
    
    fromTeam = teamColumn if not incoming else parsingTeam
    toTeam = teamColumn if incoming else parsingTeam
    
    toCountry = country if not incoming else teamColumnCountry
    fromCountry = country if incoming else teamColumnCountry
    
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
    'season' : season,
    'transfer_direction' : 'in' if incoming else 'out',
    'international_transfer' : teamColumnCountry != country,
    'from_country' : fromCountry,
    'to_country' : toCountry
    }
