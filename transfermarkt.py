# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 11:50:47 2020

@author: r.van.zundert
"""

from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import time

def get_players(comp, top):
    if top < 0:
        top = 100

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(executable_path='D:/Projects/ds_first_football/chromedriver.exe', options=options)

    url = "https://www.transfermarkt.com/transfers/neuestetransfers/statistik/plus/?plus=1&wettbewerb_id="
    url += comp
    url += "&land_id=&minMarktwert=0&maxMarktwert=200.000.000"

    driver.get(url)
    
    time.sleep(15)

    players = []
    while len(players) < top:
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        playerRows = soup.find("table",  class_='items').find("tbody").find_all("tr", recursive=False)
        
        #throw away the header
        playerRows.pop(0)
        #loop through the players and get all data from columns
        for player in playerRows:
            allColumns = player.find_all('td', recursive=False)
            
            #add player name
            playerName = player.find('a').get_text()
            print(playerName)        

            #add player age
            playerAge = allColumns[1].get_text()
                
            #nationalities parsing
            playerNationalitiesTags = allColumns[2].find_all('img')
            playerNationalityArray = []
            for nat in playerNationalitiesTags:
                playerNationalityArray.append(nat.get('alt'))
            
            #from team parsing
            fromTeamColumn = allColumns[3]
            fromTeamTableBody = fromTeamColumn.find("table",  class_='inline-table').find('tbody')
            if fromTeamTableBody == None:
                fromTeamRows = fromTeamColumn.find("table",  class_='inline-table').find_all("tr", recursive=False)
            else:
                fromTeamRows = fromTeamColumn.find("table",  class_='inline-table').find('tbody').find_all("tr", recursive=False)
            
            fromTeam = fromTeamRows[0].find('td', class_='hauptlink').find('a').get_text()
            if fromTeam.lower() != 'without club':
                teamRowAnchorTag = fromTeamRows[1].find('a')
                if teamRowAnchorTag == None:
                    fromCompetition = fromTeamRows[1].find('td').get_text()
                else:
                    fromCompetition = teamRowAnchorTag.get_text()
            else:
                fromCompetition = 'None'
            
            #to team parsing
            toTeamColumn = allColumns[4]
            
            toTeamTableBody = toTeamColumn.find("table",  class_='inline-table').find('tbody')
            if toTeamTableBody == None:
                toTeamRows = toTeamColumn.find("table",  class_='inline-table').find_all("tr", recursive=False)
            else:
                toTeamRows = toTeamColumn.find("table",  class_='inline-table').find('tbody').find_all("tr", recursive=False)
            
            toTeam = toTeamRows[0].find('td', class_='hauptlink').find('a').get_text()
            if toTeam.lower() != 'without club':
                teamRowAnchorTag = toTeamRows[1].find('a')
                if teamRowAnchorTag == None:
                    toCompetition = toTeamRows[1].find('td').get_text()
                else:
                    toCompetition = teamRowAnchorTag.get_text()
            else:
                toCompetition = 'None'
            
            #add transfer date
            transferDate = allColumns[5].get_text()
            
            #add market value
            marketValue = allColumns[6].get_text()
            
            #add transfer fee
            transferFee = allColumns[7].find('a').get_text()
            
            #add the player to the collection
            players.append({
                'player_name': playerName,
                'player_age' : playerAge,
                'player_nats' : ','.join(playerNationalityArray), 
                'from_team' : fromTeam,
                'from_competition' : fromCompetition,
                'to_team' : toTeam,
                'to_competition' : toCompetition,
                'market_value' : marketValue,
                'transfer_date' : transferDate,
                'transfer_fee' : transferFee
            })
            
            if len(players) >= top:
                break

        try:
            driver.find_element_by_xpath('.//li[@class="naechste-seite"]//a').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(top, len(players)))
            break

            
    return pd.DataFrame(players)
