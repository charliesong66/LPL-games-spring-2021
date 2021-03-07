import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from tqdm import tqdm

import mysql.connector
from mysql.connector import Error
import numpy as np


def retrieve_lpl_game(target_date):
    
    ################################
    LPL_games_table = pd.DataFrame()
    ################################
    
    option = webdriver.ChromeOptions()
    option.add_argument('headless')

    DRIVER_PATH = 'D:\ChromeDriver\chromedriver.exe'
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=option)
    driver.get('https://gol.gg/tournament/tournament-matchlist/LPL%20Spring%202021/')


    # the date in need
    
    matchups = driver.find_elements_by_xpath(f'//td[contains(text(),"{target_date}")]')

    # intialize list
    match_up = []
    week = []
    patch = []

    list_url_matches = []


    # for each match up, get url of each matchup
    # then use 2nd loop for main data
    for match in matchups:
        # all td for that ROW
        tds = match.find_elements_by_xpath('.//preceding-sibling::td')

        match_up.append(tds[0].text)
        week.append(tds[4].text)
        patch.append(tds[5].text)

        # link for the game, from td[0], that is first column, get url    
        url_match = tds[0].find_element_by_xpath('.//a').get_attribute('href')
        list_url_matches.append(url_match)



    # intialize list 
    match_up_1 = []
    week_1 = []
    patch_1 = []

    # game round number
    game_no = []    

    # side team name, win side
    blue_side = []
    red_side = []
    win_side = []

    # general game stats
    blue_kill = []
    blue_tower = []
    blue_dragon = []
    blue_baron = []
    blue_gold = []

    red_kill = []
    red_tower = []
    red_dragon = []
    red_baron = []
    red_gold = []

    # champions
    blue_top_champion = []
    blue_jug_champion = []
    blue_mid_champion = []
    blue_adc_champion = []
    blue_sup_champion = []

    red_top_champion = []
    red_jug_champion = []
    red_mid_champion = []
    red_adc_champion = []
    red_sup_champion = []

    # player names
    blue_top_player = []
    blue_jug_player = []
    blue_mid_player = []
    blue_adc_player = []
    blue_sup_player = []

    red_top_player = []
    red_jug_player = []
    red_mid_player = []
    red_adc_player = []
    red_sup_player = []


    for url_match, matchup, week, pch in tqdm(zip(list_url_matches, match_up, week, patch)):
        driver.get(url_match)

        # now on games page
        game_bar = driver.find_elements_by_xpath('//div[contains(@id, "gameMenuToggler")]//a[contains(text(), "Game")]')

        # save url for rounds within matchup
        game_round_url = []

        for game in game_bar:

            match_up_1.append(matchup)
            week_1.append(week)
            patch_1.append(pch)   

            game_no.append(game.text)

            temp_url = game.get_attribute('href')
            game_round_url.append(temp_url)


        # game page for individual game
        for temp_url in game_round_url:

            driver.get(temp_url)

            #########################################################################################
            # blue side, red side, win side
            blue_header = driver.find_element_by_xpath('//div[contains(@class,"blue-line-header")]')
            red_header = driver.find_element_by_xpath('//div[contains(@class,"red-line-header")]')

            blue_header = blue_header.text.split(' - ')
            red_header = red_header.text.split(' - ')

            blue_side.append(blue_header[0])
            red_side.append(red_header[0])

            if 'WIN' in blue_header:
                win_side.append('BLU')
            else:
                win_side.append('RED')

            #########################################################################################
            # stats, kills, towers, dragon, baron, gold
            blue_stats = driver.find_elements_by_xpath('//span[contains(@class, "blue_line")]')
            red_stats = driver.find_elements_by_xpath('//span[contains(@class, "red_line")]')

            blue_kill.append(blue_stats[0].text)
            blue_tower.append(blue_stats[1].text)
            blue_dragon.append(blue_stats[2].text)
            blue_baron.append(blue_stats[3].text)
            blue_gold.append(blue_stats[4].text.replace('k',''))

            red_kill.append(red_stats[0].text)
            red_tower.append(red_stats[1].text)
            red_dragon.append(red_stats[2].text)
            red_baron.append(red_stats[3].text)
            red_gold.append(red_stats[4].text.replace('k',''))    
            #########################################################################################
            # champions
            champions = driver.find_elements_by_xpath('//img[contains(@class, "champion_icon rounded-circle")]')

            blue_top_champion.append(champions[0].get_attribute('alt'))
            blue_jug_champion.append(champions[1].get_attribute('alt'))
            blue_mid_champion.append(champions[2].get_attribute('alt'))
            blue_adc_champion.append(champions[3].get_attribute('alt'))
            blue_sup_champion.append(champions[4].get_attribute('alt'))

            red_top_champion.append(champions[5].get_attribute('alt'))
            red_jug_champion.append(champions[6].get_attribute('alt'))
            red_mid_champion.append(champions[7].get_attribute('alt'))
            red_adc_champion.append(champions[8].get_attribute('alt'))
            red_sup_champion.append(champions[9].get_attribute('alt'))   
            #########################################################################################
            # players    
            players = driver.find_elements_by_xpath('//a[contains(@class, "link-blanc")]')

            blue_top_player.append(players[0].text)
            blue_jug_player.append(players[1].text)
            blue_mid_player.append(players[2].text)
            blue_adc_player.append(players[3].text)
            blue_sup_player.append(players[4].text)

            red_top_player.append(players[5].text)
            red_jug_player.append(players[6].text)
            red_mid_player.append(players[7].text)
            red_adc_player.append(players[8].text)
            red_sup_player.append(players[9].text)
            #########################################################################################


    # game info columns        
    LPL_games_table['Match_up'] = match_up_1
    LPL_games_table['Game_round'] = game_no

    LPL_games_table['blue_side'] = blue_side
    LPL_games_table['red_side'] = red_side
    LPL_games_table['win_side'] = win_side


    # genral game stats columns
    LPL_games_table['blue_kill'] = blue_kill
    LPL_games_table['blue_tower'] = blue_tower
    LPL_games_table['blue_dragon'] = blue_dragon
    LPL_games_table['blue_baron'] = blue_baron
    LPL_games_table['blue_gold'] = blue_gold

    LPL_games_table['red_kill'] = red_kill
    LPL_games_table['red_tower'] = red_tower
    LPL_games_table['red_dragon'] = red_dragon
    LPL_games_table['red_baron'] = red_baron
    LPL_games_table['red_gold'] = red_gold


    # player name columns
    LPL_games_table['blue_top_player'] = blue_top_player
    LPL_games_table['blue_jug_player'] = blue_jug_player
    LPL_games_table['blue_mid_player'] = blue_mid_player
    LPL_games_table['blue_adc_player'] = blue_adc_player
    LPL_games_table['blue_sup_player'] = blue_sup_player


    LPL_games_table['red_top_player'] = red_top_player
    LPL_games_table['red_jug_player'] = red_jug_player
    LPL_games_table['red_mid_player'] = red_mid_player
    LPL_games_table['red_adc_player'] = red_adc_player
    LPL_games_table['red_sup_player'] = red_sup_player


    # champion name columns
    LPL_games_table['blue_top_champion'] = blue_top_champion
    LPL_games_table['blue_jug_champion'] = blue_jug_champion
    LPL_games_table['blue_mid_champion'] = blue_mid_champion
    LPL_games_table['blue_adc_champion'] = blue_adc_champion
    LPL_games_table['blue_sup_champion'] = blue_sup_champion

    LPL_games_table['red_top_champion'] = red_top_champion
    LPL_games_table['red_jug_champion'] = red_jug_champion
    LPL_games_table['red_mid_champion'] = red_mid_champion
    LPL_games_table['red_adc_champion'] = red_adc_champion
    LPL_games_table['red_sup_champion'] = red_sup_champion

    # week and patch
    LPL_games_table['Week'] = week_1
    LPL_games_table['patch'] = patch_1

    return LPL_games_table



# web-scrape data
# change type to int/float
desired_date = input('Enter the date of match: ')
lpl_table = retrieve_lpl_game(desired_date)

# stats are int
int_columns = ['blue_kill', 'blue_tower', 'blue_dragon', 'blue_baron',
       'red_kill', 'red_tower', 'red_dragon', 'red_baron']

for col in int_columns:
    lpl_table[col] = lpl_table[col].astype('int32')

# gold are float
lpl_table['blue_gold'] = lpl_table['blue_gold'].astype('float')
lpl_table['red_gold'] = lpl_table['red_gold'].astype('float')



#####################
# create connection #
#####################
def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

pw = '1qaz2wsx'
connection = create_server_connection("localhost", "root", pw)

# create database
def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

create_database_query = 'CREATE DATABASE IF NOT EXISTS LPL_spring_games'
create_database(connection, create_database_query)


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

###################
# create database #
###################      
        
def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection


create_LPL_spring = """
CREATE TABLE IF NOT EXISTS lpl_spring_games (
  Match_up VARCHAR(64) NOT NULL,
  Game_round VARCHAR(64) NOT NULL,
  
  blue_side VARCHAR(64) NOT NULL,
  red_side VARCHAR(64) NOT NULL,
  win_side VARCHAR(64) NOT NULL,
  
  blue_kill INT NOT NULL,
  blue_tower INT NOT NULL,
  blue_dragon INT NOT NULL,
  blue_baron INT NOT NULL,
  blue_gold FLOAT NOT NULL,
  
  red_kill INT NOT NULL,
  red_tower INT NOT NULL,
  red_dragon INT NOT NULL,
  red_baron INT NOT NULL,
  red_gold FLOAT NOT NULL,
  
  blue_top_player VARCHAR(64) NOT NULL,
  blue_jug_player VARCHAR(64) NOT NULL,
  blue_mid_player VARCHAR(64) NOT NULL,
  blue_adc_player VARCHAR(64) NOT NULL,
  blue_sup_player VARCHAR(64) NOT NULL,
  
  red_top_player VARCHAR(64) NOT NULL,
  red_jug_player VARCHAR(64) NOT NULL,
  red_mid_player VARCHAR(64) NOT NULL,
  red_adc_player VARCHAR(64) NOT NULL,
  red_sup_player VARCHAR(64) NOT NULL,
  
  blue_top_champion VARCHAR(64) NOT NULL,
  blue_jug_champion VARCHAR(64) NOT NULL,
  blue_mid_champion VARCHAR(64) NOT NULL,
  blue_adc_champion VARCHAR(64) NOT NULL,
  blue_sup_champion VARCHAR(64) NOT NULL,
  
  red_top_champion VARCHAR(64) NOT NULL,
  red_jug_champion VARCHAR(64) NOT NULL,
  red_mid_champion VARCHAR(64) NOT NULL,
  red_adc_champion VARCHAR(64) NOT NULL,
  red_sup_champion VARCHAR(64) NOT NULL,  
  
  Week VARCHAR(64) NOT NULL,
  patch VARCHAR(64) NOT NULL
  );
 """

db = 'LPL_spring_games'

connection = create_db_connection("localhost", "root", pw, db) # Connect to the Database
execute_query(connection, create_LPL_spring) # Execute our defined query      



# insert data into SQL
# make all value into list, then generate query str

for idx, row in lpl_table.iterrows():

    list_values = []

    for val in row:
        list_values.append('\"' + str(val) + '\"')

    insert_lpl_spring_games = 'INSERT INTO lpl_spring_games VALUES ' + '(' +  ','.join(list_values) + ');'
    
    # execute query str
    execute_query(connection, insert_lpl_spring_games) 
