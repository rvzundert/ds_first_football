# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:50:47 2020

@author: r.van.zundert
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&wettbewerb_id=NL1&land_id=&minMarktwert=0&maxMarktwert=200.000.000"
headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

page = requests.get(url, headers=headers)
soup = BeautifulSoup(page.content, 'html.parser')
playerRows = soup.find("table",  class_='items').find("tbody").find_all("tr", recursive=False)

#throw away the header
playerRows.pop(0)

x = 0

playerNames = []
playerAges = []
playerNationalities = []
fromTeams = []
fromCompetitions = []
toTeams = []
toCompetitions = []
marketValues = []
transferDates = []
transferFees = []

#loop through the players and get all data from columns
for player in playerRows:
    allColumns = player.find_all('td', recursive=False)
    
    #add player name
    playerName = player.find('a').get_text()
    playerNames.append(playerName)
    
    #add player age
    playerAge = allColumns[1].get_text()
    playerAges.append(playerAge)
        
    #nationalities parsing
    playerNationalitiesTags = allColumns[2].find_all('img')
    playerNationalityArray = []
    for nat in playerNationalitiesTags:
        playerNationalityArray.append(nat.get('alt'))
    playerNationalities.append(','.join(playerNationalityArray))
    
    #from team parsing
    fromTeamColumn = allColumns[3]
    fromTeamRows = fromTeamColumn.find("table",  class_='inline-table').find_all("tr", recursive=False)
    fromTeam = fromTeamRows[0].find('td', class_='hauptlink').find('a').get_text()
    if fromTeam.lower() != 'without club':
        fromCompetition = fromTeamRows[1].find('a').get_text()
    else:
        fromCompetition = 'None'
    fromTeams.append(fromTeam)
    fromCompetitions.append(fromCompetition)
    
    #to team parsing
    toTeamColumn = allColumns[4]
    toTeamRows = toTeamColumn.find("table",  class_='inline-table').find_all("tr", recursive=False)
    toTeam = toTeamRows[0].find('td', class_='hauptlink').find('a').get_text()
    if toTeam.lower() != 'without club':
        toCompetition = toTeamRows[1].find('a').get_text()
    else:
        toCompetition = 'None'
    toTeams.append(toTeam)
    toCompetitions.append(toCompetition)
    
    #add transfer date
    transferDate = allColumns[5].get_text()
    transferDates.append(transferDate)
    
    #add market value
    marketValue = allColumns[6].get_text()
    marketValues.append(marketValue)
    
    #add transfer fee
    transferFee = allColumns[7].find('a').get_text()
    transferFees.append(transferFee)
    
    x+=1
    # if x == 5:
    #     break

#add all data to a table
players = pd.DataFrame({
    'player_name': playerNames,
    'player_age' : playerAges,
    'player_nats' : playerNationalities, 
    'from_team' : fromTeams,
    'from_competition' : fromCompetitions,
    'to_team' : toTeams,
    'to_competition' : toCompetitions,
    'market_value' : marketValues,
    'transfer_date' : transferDates,
    'transfer_fee' : transferFees
})