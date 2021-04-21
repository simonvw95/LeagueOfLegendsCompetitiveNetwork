# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:22:03 2021

@author: Simon
"""

# import necessary packages
import pandas as pd
import time
import networkx as nx
import pickle
import os
import numpy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from difflib import SequenceMatcher


options = Options()
options.add_argument("--window-size=1920,1200")

driver_p = r'C:\Users\Simon\Downloads\chromedriver'
driver = webdriver.Chrome(executable_path = driver_p)

driver2 = webdriver.Chrome(executable_path = driver_p)

# the leagues and tournaments that were scraped
# all the MAIN tournaments and their challenger/academy leagues
# LCS + NA Academy League
URL_LCS = 'https://lol.gamepedia.com/League_Championship_Series'
# LEC + European Masters
URL_LEC = 'https://lol.gamepedia.com/LoL_European_Championship'
# LCK 
URL_LCK = 'https://lol.gamepedia.com/League_of_Legends_Champions_Korea'
# LPL
URL_LPL = 'https://lol.gamepedia.com/LoL_Pro_League'
# CBLOL
URL_CBLOL = 'https://lol.gamepedia.com/Circuit_Brazilian_League_of_Legends'
# OPL (Oceanic Pro League)
URL_OPL = 'https://lol.gamepedia.com/Oceanic_Pro_League'
# PCL (Pacific Championship Series)
URL_PCS = 'https://lol.gamepedia.com/Pacific_Championship_Series'
# TCL (Turkish Champion League)
URL_TCL = 'https://lol.gamepedia.com/Turkish_Championship_League'
# VCS (Vietnam League)
URL_VCS = 'https://lol.gamepedia.com/VCS_A/2017_Season'
# LMS (League of Legends Master Series) Disbanded (Taiwan, Hong Kong, and Macao)
URL_LMS = 'https://lol.fandom.com/wiki/League_of_Legends_Master_Series'


#national_leagues = {}
#national_leagues['LCS/North America'] = URL_LCS # done
#national_leagues['LEC/Europe'] = URL_LEC # done
#national_leagues['LCK/South Korea'] = URL_LCK
#national_leagues['LPL/China'] = URL_LPL
#national_leagues['CBLOL/Brazil'] = URL_CBLOL
#national_leagues['OPL/Oceania'] = URL_OPL
#national_leagues['PCS/PCS'] = URL_PCS
#national_leagues['TCL/Turkey'] = URL_TCL
#national_leagues['VCS/Vietnam'] = URL_VCS
#national_leagues['LMS/Taiwan + Hong Kong + Macao'] = URL_LMS


# LCL (LoL Continental League) # special case
URL_LCL = 'https://lol.gamepedia.com/League_of_Legends_Continental_League'
# LJL (LoL Japan League) # special case
URL_LJL = 'https://lol.gamepedia.com/League_of_Legends_Japan_League'
# LL (Liga Latinoamerica) # special case
URL_LL = 'https://lol.gamepedia.com/Liga_Latinoam%C3%A9rica'
# LST (League of Legends SEA Tour)
URL_LST = 'https://lol.fandom.com/wiki/League_of_Legends_SEA_Tour'

#minor_leagues = {}
#minor_leagues['LCL/Russia'] = URL_LCL
#minor_leagues['LJL/Japan'] = URL_LJL
#minor_leagues['LL/Latin America'] = URL_LL
#minor_leagues['LST/Southeast Asia'] = URL_LST

# MSI (Mid Season Invitationals)
URL_MSI = 'https://lol.fandom.com/wiki/Mid-Season_Invitational'
# Worlds (World Championships)
URL_WORLDS = 'https://lol.fandom.com/wiki/World_Championship'
# IEM (Intel Extreme Masters) + ISL
URL_IEM = 'https://lol.gamepedia.com/Intel_Extreme_Masters'

#national_tourn = {}
#national_tourn['MSI'] = URL_MSI
#national_tourn['WORLDS'] = URL_WORLDS
#national_tourn['IEM'] = URL_IEM

def getSeasonData(URL, name_region, special_case = False, MSI_WORLDS = False, IEM = False):
    
    if name_region == 'LCL/Russia' or name_region == 'LJL/Japan' or name_region == 'LL/Latin America' or name_region == 'LST/Southeast Asia':
        special_case = True
        
    if name_region == 'MSI' or name_region == 'WORLDS':
        MSI_WORLDS = True
        
    if name_region == 'IEM':
        IEM = True
    
    # get the webpage from the link
    driver.get(URL)

    # some pages could only be scraped by looking at the wikitable
    if special_case:
        competitions = driver.find_elements_by_class_name('wikitable')
    # other pages looking at the hlist would do
    else:
        competitions = driver.find_elements_by_class_name('hlist')
        
    # get all the hyperlinks to all competitions
    
    # MSI and the Worlds tournaments had a different page setup and required more execution
    if MSI_WORLDS:
        
        pre_links = []
        # the first two loops acquired all the years of that tournament (2012-2021)
        for i in [competitions[2]]:
            a_list = i.find_elements_by_tag_name('a')
            
            for j in a_list:
                pre_links.append(j.get_attribute('href'))
             
        # these two loops acquired the (sub)-tournaments within that tournament
        # e.g. play-ins and the main event
        links = []
        for link in pre_links:
            driver.get(link)
            rosters_present = driver.find_elements_by_class_name('tabheader-top')
            if rosters_present:
                rosters_present = rosters_present[0]
                if 'Team Rosters' in rosters_present.text:
                    links.append(link)
                else:
                    a_list = rosters_present.find_elements_by_tag_name('a')
                    
                    for m in a_list:
                        links.append(m.get_attribute('href'))    
            
    else:
        # IEM was another special case
        if IEM:
            links = []
            for i in competitions:
                a_list = i.find_elements_by_tag_name('a')
                
                for j in a_list:
                    links.append(j.get_attribute('href'))  
        # any other tournament could be scraped using this bottom code
        else:
            links = []
            for i in competitions[0:2]:
                a_list = i.find_elements_by_tag_name('a')
                
                for j in a_list:
                    links.append(j.get_attribute('href'))       

    # initialize an empty dataframe, empty edge list, empty collection of gamer tags and player names
    teams_df = pd.DataFrame()
    edge_list = pd.DataFrame(columns = ['From', 'To', 'n_played'])
    gamer_tags = []
    player_names = []
    
    # initialize an empty meta dataframe
    meta_data = pd.DataFrame(columns = ['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team'])
    
    # start the timer
    start_time = time.time()
    # go over every hyperlink (every tournament)
    for link in links:
        
        
        
        
        # go over every possible team, number from 1 to 30, (max is 17 I believe but just incase)
        for team_no in range(1, 30):
            team_links = link + "/" + "Team_Rosters?action=edit&section=" + str(team_no)
            
            # try except block incase something goes wrong, sometimes data entry is faulty
            try:

                # get the page of the team in that specific tournament
                driver.get(team_links)
                
                # get the box of text with the desired content
                textboxs = driver.find_elements_by_class_name('mw-editfont-default')
                
                # turn it into clean text
                if textboxs:
                    clean_text = textboxs[-1].text
                    skip_crawl_list = ['== League 1 ==', '== League 2 ==', '== League 3 ==', '== League 4 ==', '==Group A==', '==Group B==', '==Group C==', '==Group D==', '==Group E==', '==Group F==', '==Group Stage==']
                    skip_this_one = False
                    for i in skip_crawl_list:
                        if i in clean_text:
                            skip_this_one = True

                    if skip_this_one:
                        continue
                    
                    if '<!--' and '-->' in clean_text:
                        text_to_repl = str(clean_text.partition('<!--')[2].partition('-->')[0])
                        clean_text = clean_text.replace('<!--' + text_to_repl + '-->', '')
                
                
                # check if the page exists, if it doesn't then it asks you to login to create the page
                # or says that you don't have permission
                # if this is the case then ignore this 'tournament' as it is not a tournament
                
                login_req_page = driver.find_elements_by_class_name('firstHeading')
                break_main = False
                
                for header in login_req_page:
                    if header.text == 'Login required' or header.text == 'Permission error':
                        break_main = True
                        break
                    
                if break_main:
                    break
                

                if textboxs:
                    team_name = None
                    # extract the team name
                    team_name = str(clean_text.partition("{{team|")[2].partition("}}")[0])

                    # get the lines that contain player info
                    players = []
                    # add a counter incase data entry is irregular and the code doesn't know it should be done
                    cnt = 0
                    while 'name=' in clean_text or '{|class="sortable wikitable"' in clean_text:
                        if 'ExtendedRosterLine' in clean_text:
                            players.append(clean_text.partition("{{ExtendedRosterLine")[2].partition("}}")[0])
                            clean_text = clean_text.replace("{{ExtendedRosterLine" + players[-1] + "}}", "")
                        if 'RosterLineOld' in clean_text:
                            players.append(clean_text.partition("{{RosterLineOld")[2].partition("}}")[0])
                            clean_text = clean_text.replace("{{RosterLineOld" + players[-1] + "}}", "")
                        cnt += 1
                        if cnt > 100:
                            break
                        
                    players = list(set(players))
                        
                    # get their gamer tag and actual name
                    player_tags = []
                    for i in range(len(players)):
                        
                        gamer_tag = players[i].partition("|player=")[2].partition("|")[0]
                        name = players[i].partition("|name=")[2].partition("|")[0]
                        
                        # remove unnecessary spaces
                        gamer_tag = " ".join(gamer_tag.split())
                        name = " ".join(name.split())
                        
                        # go over all the extracted player names
                        for n in range(len(player_names)):
                            # if we have a full match then use the name we have
                            if name == player_names[n]:
                                name = player_names[n]
                                gamer_tag = gamer_tags[n]
                                break
                                                                

                        # only add gamer tag and player name to the big list if the name isn't already in there
                        if name not in player_names:
                            
                            gamer_tags.append(gamer_tag)
                            player_names.append(name)

                        player_tags.append(gamer_tag + " (" + name + ")")
                        
                        # meta data df order: list(['gamer_tag', 'full_name', 'role', 'residency', 'country'])
                        if players:
                            role = " ".join(players[i].partition("|role=")[2].partition("|")[0].split())
                            residency = " ".join(players[i].partition("|res=")[2].partition("|")[0].split())
                            country = " ".join(players[i].partition("|flag=")[2].partition("|")[0].split())
                            
                            
                            if 'role1' in players[i]:
                                role1 = " ".join(players[i].partition("|role1=")[2].partition("|")[0].split())
                                role2 = " ".join(players[i].partition("|role2=")[2].partition("|")[0].split())
                                role = role1 + '/' + role2
                                
                            temp_df = {'gamer_tag' : gamer_tag, 'full_name' : name, 'role' : role, 'residency' : residency, 'country' : country, 'team' : team_name}
                            meta_data = meta_data.append(temp_df, ignore_index = True)
                            
                    # add new data to an existing team name column if the column already exists
                    if team_name and player_tags:
                        if team_name in teams_df.columns:
                            temp_df = pd.DataFrame()
                            temp_df[team_name] = pd.Series(player_tags)
                            temp_df[team_name] = temp_df[team_name].astype(str)
                            teams_df = teams_df.merge(temp_df, left_on = team_name, right_on = team_name, how = 'outer')
                            # add the team to the dataframe if it isn't in there
                        else:
                            teams_df[team_name] = pd.Series(player_tags)                       
                    
                    # extract the info about players having played a match together
                    matching_play_matrix = pd.DataFrame(columns = list(player_tags))
                    for i in range(len(players)):
                        if 'r1=' in players[i]:
                            # sometimes there are two designated roles for a single player
                            role1_list = list(" ".join(players[i].partition("|r1=")[2].partition("|")[0].replace(',', '')).split())
                            role2_list = list(" ".join(players[i].partition("|r2=")[2].partition("|")[0].replace(',', '')).split())
                            role_full_list = []
                                
                            # if there are 2 roles then the role lists must be merged
                            if role2_list:
                                if len(role1_list) != len(role2_list):
                                    if len(role1_list) > len(role2_list):
                                        role1_list = role1_list[0:len(role2_list)]
                                    else:
                                        role2_list = role2_list[0:len(role1_list)]
                                for y_n in range(len(role1_list)):
                                    if role1_list[y_n] == 'y' or role2_list[y_n] == 'y':
                                        role_full_list.append('y')
                            # if only r1 exists then we use that
                            else:
                                role_full_list = role1_list
                                    
                            matching_play_matrix[player_tags[i]] = pd.Series(role_full_list)
                            players[i] = players[i].replace("|r1=" + player_tags[i] + "}}", "")
                            players[i] = players[i].replace("|r2=" + player_tags[i] + "}}", "")
                                
                        else:
                            matching_play_matrix[player_tags[i]] = pd.Series(list(" ".join(players[i].partition("|r=")[2].partition("|")[0].replace(',', '')).split()))
        
                    # remove duplicates
                    matching_play_matrix = matching_play_matrix.T.groupby(level=0).first().T
                        
                    # go over every person twice (for each person match that person with an other person on the same team)
                    columns_mat = list(matching_play_matrix.columns)
                    for i in range(len(columns_mat)):
                        for j in range(i, len(columns_mat)):
                            # skip if the person is matching with him/herself
                            if i != j:
                                # go over every match in the match list
                                for k in range(len(matching_play_matrix[columns_mat[j]])):
                                    try:
                                        # if they both have a 'y' then it means they played together
                                        if matching_play_matrix[columns_mat[i]][k] == 'y' and matching_play_matrix[columns_mat[j]][k] == 'y':
                                            
                                            # create a tuple
                                            tup = [columns_mat[i], columns_mat[j]]

                                            if (((edge_list['From'] == tup[0]) & (edge_list['To'] == tup[1])).any() == False) and (((edge_list['From'] == tup[1]) & (edge_list['To'] == tup[0])).any() == False):
                                                edge_list.loc[len(edge_list) + 1] = [tup[0], tup[1], 1]
                                            # if it does exist then we increase the count
                                            else:
                                                # check if the edge exists
                                                temp = edge_list.loc[(edge_list['From'] == tup[0]) & (edge_list['To'] == tup[1])]
                                                if len(temp) == 1:
                                                    edge_list.loc[temp.index[0]]['n_played'] += 1
                                                # if the edge doesnt exist then maybe the reverse edge exists
                                                elif len(temp) == 0:
                                                    temp = edge_list.loc[(edge_list['From'] == tup[1]) & (edge_list['To'] == tup[0])]
                                                    edge_list.loc[temp.index[0]]['n_played'] += 1
                                                    
                                                
                                    except IndexError:
                                        print(team_links)
                                        continue
                        
        
            except Exception as e:
                print(e)
                print(team_links)
    
        
    # remove unnecessary nan values that make the df longer
    teams_df = teams_df.apply(lambda x: pd.Series(x.dropna().values))
    # remove duplicate rows in meta data
    meta_data = meta_data.drop_duplicates()
    
    # add the name of the region as a column
    edge_list['Region'] = name_region
    
    filehandler = open('C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/' + name_region.split('/')[0] + '.pckl', 'wb') 
    pickle.dump([edge_list, teams_df, meta_data], filehandler)
    filehandler.close
    
    end_time = time.time()
    print("Extracting tournament info took: ", round(end_time - start_time, 4), " seconds.")
    print("")
    
    return edge_list, teams_df, meta_data


# testing line to see if everything works
edge_list, teams_df, meta_data = getSeasonData(national_leagues['LCK/South Korea'], 'LCK/South Korea')
         

# 3 loops for the different leagues and tournaments
for nat_league in national_leagues:
    edge_list, teams_df, meta_data = getSeasonData(national_leagues[nat_league], nat_league)
    
for min_league in minor_leagues:
    edge_list, teams_df, meta_data = getSeasonData(minor_leagues[min_league], min_league)
    
for nat_tourn in national_tourn:
    edge_list, teams_df, meta_data = getSeasonData(national_tourn[nat_tourn], nat_tourn)
            

# concatenating all edge lists, meta data and teams data
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
all_pickles = os.listdir(path)
long_edge_list = pd.DataFrame(columns = ['From', 'To', 'n_played', 'Region'])
long_teams_df = pd.DataFrame()
long_meta_data = pd.DataFrame(columns = ['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team'])

# go over all the pickles
for i in all_pickles:
    if i[-5:] == '.pckl':
        # drop IEM, too much missing data and incorrect data collection
        if (i != 'seen_names.pckl') and (i != 'IEM.pckl'):
            file = open(path + i, 'rb')
            file_content = pickle.load(file)
            file.close
            long_edge_list = long_edge_list.append(file_content[0], ignore_index = True)
            
            # add new data to an existing team name column if the column already exists
            for j in file_content[1].columns:
                if j in long_teams_df.columns:
                    temp_df = pd.DataFrame()
                    temp_df[j] = pd.Series(file_content[1][j])
                    temp_df = temp_df.append(pd.DataFrame(long_teams_df[j])).dropna().drop_duplicates()
                    long_teams_df[j] = pd.Series(list(temp_df[j]))
                else:
                    long_teams_df[j] = pd.Series(file_content[1][j])                   
                    

            long_meta_data = long_meta_data.append(file_content[2], ignore_index = True)
            # make sure there are no nan values
            long_meta_data.fillna('', inplace = True)
            


# clean up the meta data information, can check for redundancies in the role residency and country
def removeRedundancies(df, column, collection, lower = False):
    
    # print out the unique column entries
    print(set(df[column]))
    
    # loop over all the entries in the column
    for i in range(len(df[column])):
        # and all the keys in the collection
        for j in collection:
            # and all the values belonging to that key
            for k in collection[j]:
                # ensure that it is a string, sometimes nan still pops up
                if isinstance(df[column][i], str):
                    if isinstance(k, str):
                        if df[column][i].lower() == k.lower():
                            df[column][i] = j
                else:
                    if df[column][i] == k:
                        df[column][i] = j
                    
                
        # there may be a dual role, this will occur if there is a '/' present
        # only will happen in the role column which will have 'Top' in the collection
        if '/' in df[column][i] and 'Top' in collection:
            first_role = df[column][i].split('/')[0]
            second_role = df[column][i].split('/')[1]
            
            # only acquire a role if it is not empty
            if first_role != '':
                for j in collection:
                    for k in collection[j]:
                        if first_role.lower() == k.lower():
                            first_role = j
            if second_role != '':
                for j in collection:
                    for k in collection[j]:
                        if second_role.lower() == k.lower():
                            second_role = j
                
                full_dual_role = first_role + '/' + second_role                    
                df[column][i] = full_dual_role
            else:
                df[column][i] = first_role
                
                
        if lower:
            df[column][i] = df[column][i].lower()
            
    # we have to go over the column again in case there are duplicate entries as stated below
    if 'Top' in collection:
         # if the reverse role already exists e.g. full_dual_role = 'Support/Coach'
         # and 'Coach/Support' already exists then we also make this entry 'Coach/Support'
        for i in range(len(df[column])):
            if '/' in df[column][i]:
                # reverse the role
                reverse_role = (df[column][i].split('/')[1] + '/' + df[column][i].split('/')[0])
                if reverse_role in set(df[column][0:i]):
                    df[column][i] = reverse_role

            
    
    print()
    print(set(df[column]))
    
    
    
# collection of role entries that have to be standardized
role_coll = {}
role_coll['Top'] = ['Top <!--Played as "Yoyo" for the first three rounds-->', 'Top', 't', 'toplane', 'Top <!--李东秀-->', 'Top <!--Played as "noko" in Round 2-->', 'Sub/Top', 'Top Laner', 'top lane']
role_coll['Jungle'] = ['Sub/Jungle', 'Jungle', 'j', 'Jungle <!--申岷升-->', 'J', 'Jungler']
role_coll['Mid'] = ['Mid', 'm', 'Sub/Mid', 'Mid Laner', 'Midlane', 'AP']
role_coll['Ad Carry'] = ['Sub/AD', 'Bot Laner', 'b', 'A', 'Bot', 'AD', 'AD Carry', 'adc']
role_coll['Support'] = ['Support', 'Sub/Support', 'sup', 'S', 'Support <!--Played as "ADC" for the first two rounds-->']
role_coll['Coach'] = ['c', 'C', 'c--> {{ExtendedRosterEnd', 'Coach', 'Assistant Coach', 'Head Coach', 'Strategic Coach', 'coach']
role_coll['Substitute'] = ['Sub', 'sub', 'Substitute']
role_coll['Unknown'] = ['']
role_coll['Top/Ad Carry'] = ['Top, AD']
role_coll['Top/Mid'] = ['Top, AP']

removeRedundancies(long_meta_data, 'role', role_coll)


# collection of region entries that have to be standardized            
resid_coll = {}
resid_coll['Unknown/None'] = ['', 'Unrecognized Region', '??', 'None', 'Unknown', 'nan', numpy.nan]
resid_coll['North America'] = ['North America', 'Oceania', 'OCE', 'NA']
resid_coll['Europe'] = ['Europe', 'EU']
resid_coll['South Korea'] = ['South Korea','KR', 'Korea']
resid_coll['China'] = ['CN', 'China']
resid_coll['PCS (Pacific Championship Series)'] = ['PCS', 'Taiwan', 'Taiwan, Hong Kong, and Macao', 'LMS', 'tw', 'SEA', 'TW', 'Southeast Asia']
resid_coll['Brazil'] = ['BR', 'Brazil']
resid_coll['CIS (Commonwealth of Independent States)'] = ['CIS', 'ru', 'Commonwealth of Independent States']
resid_coll['Japan'] = ['Japan', 'JP']
resid_coll['Latin America'] = ['LAT', 'Latin America', 'LAS', 'LAN']
resid_coll['Turkey'] = ['TR', 'Turkey']
resid_coll['Vietnam'] = ['vyn', 'Vietnam', 'VN']

removeRedundancies(long_meta_data, 'residency', resid_coll)


# collection of country entries that have to be standardized
# not all countries were standardized
country_coll = {}
country_coll['China'] = ['China', 'CN', 'cn<!--assumed-->']
country_coll['South Korea'] = ['South Korea', 'Korea', 'KR']
country_coll['Germany'] = ['Germany', 'DE']
country_coll['United Kingdom'] = ['UK', 'United Kingdom']
country_coll['Belgium'] = ['BE', 'Belgium']
country_coll['Netherlands'] = ['Netherlands', 'NL']
country_coll['Vietnam'] = ['Vietnam', 'VN']
country_coll['United States'] = ['United States', 'us', 'usa']
country_coll['Denmark'] = ['Denmark', 'dk']
country_coll['Brazil'] = ['Brazil', 'BR']
country_coll['France'] = ['France', 'FR']
country_coll['Italy'] = ['Italy', 'IT']
country_coll['New Zealand'] = ['NZ', 'New Zealand']
country_coll['Canada'] = ['CA', 'Canada']
country_coll['Sweden'] = ['Sweden']
country_coll['Unknown'] = ['Unknown', 'none', numpy.nan, '']

removeRedundancies(long_meta_data, 'country', country_coll, lower = True)



# drop the duplicates
long_meta_data = long_meta_data.drop_duplicates()
long_meta_data = long_meta_data.reset_index(drop=True)
long_meta_data.fillna('', inplace = True)


# save as csv
#path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
#long_meta_data.to_csv(path_or_buf = path + 'meta_data.csv', index = False)
#long_teams_df.to_csv(path_or_buf = path + 'teams_data.csv', index = False)
#long_edge_list.to_csv(path_or_buf = path + 'final_edge_list.csv', index = False)



############################################################################################
# start the cleaning process of the edge list

path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'

# originals
#edge_list = pd.read_csv(path + 'final_edge_list.csv')
#edge_list = edge_list.reset_index(drop = True) 
#teams_df = pd.read_csv(path + 'teams_data.csv')
#teams_df = teams_df.reset_index(drop = True) 
#meta_data = pd.read_csv(path + 'meta_data.csv')
#meta_data.fillna('', inplace = True)
#meta_data = meta_data.reset_index(drop = True) 


# new ones that are semi-cleaned
edge_list = pd.read_csv(path + 'final_refined_edge_list.csv')
edge_list = edge_list.reset_index(drop = True) 
teams_df = pd.read_csv(path + 'final_teams_data.csv')
teams_df = teams_df.reset_index(drop = True) 
meta_data = pd.read_csv(path + 'final_meta_data.csv')
meta_data.fillna('', inplace = True)
meta_data = meta_data.reset_index(drop = True) 



# a similarity metric for strings, used for names here
def similarity(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

def evaluateDuplicates(edge_list, meta_deta, teams_df, save = True, check_full_name = False, check_gamer_tag = False):
    
    # load a pickle that contains information about which names we have already compared
    file = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\seen_names.pckl', 'rb')
    seen_list = pickle.load(file)
    file.close
    
    # get a regular list from the edge list dataframe
    edge_list_nondf = edge_list.values.tolist()
    
    # turn the edge list into a graph so we can get a list of nodes
    G = nx.Graph()
    for i in edge_list_nondf:
        nx.add_path(G, (i[0], i[1]))
    
    node_list = list(G.nodes())
    
    # start the timer
    start_time = time.time()
    
    # go over all the nodes and find new instances of dual players
    empty_dict = {}
    for i in range(len(node_list)):
        if i % 1000 == 0:
            print('I am at' + str(i))
            print('This took me this long', round(time.time() - start_time, 4))
        for j in range(i, len(node_list)):
            if i != j:
                
                # extract the full name of each person
                full_name1 = node_list[i].partition('(')[2]
                full_name2 = node_list[j].partition('(')[2]
                # extract the gamer tag of each person
                gamer_tag1 = node_list[i].split('(')[0]
                gamer_tag2 = node_list[j].split('(')[0]
                if check_full_name:
                    empty_dict[(node_list[i], node_list[j])] = similarity(full_name1, full_name2)
                elif check_gamer_tag:

                    empty_dict[(node_list[i], node_list[j])] = similarity(gamer_tag1, gamer_tag2)
                else:
                    empty_dict[(node_list[i], node_list[j])] = similarity(node_list[i], node_list[j])
                
    # copy the original edge list and start two counters
    edge_list_copy = edge_list.copy(deep = True)
    meta_data_copy = meta_data.copy(deep = True)
    teams_df_copy = teams_df.copy(deep = True)
    
    # cnt is used for indexing
    cnt = 0
    # new_cnt is used as to stop the main loop 
    new_cnt = 0
    
    # sort the list based on the names their similarity
    sorted_list = list(sorted(empty_dict.items(), key = lambda item: item[1], reverse = True))
      
    new_players = []
    new_full_names = []
    new_gamer_tags = []
    
    old_players = []
    old_full_names = []
    old_gamer_tags = []
    
    
    while True:
        i = sorted_list[cnt]
        
        try:
            # if we haven't evaluated the combination of names before then we will evaluate
            if [i[0][0], i[0][1]] not in seen_list:
                
                # this extracts the full name without the ( )
                full_name1 = i[0][0].partition('(')[2][:-1]
                # this removes leading and trailing white spaces
                full_name1 = " ".join(full_name1.split())
                full_name2 = i[0][1].partition('(')[2][:-1]
                full_name2 = " ".join(full_name2.split())
                
                gamer_tag1 = i[0][0].split('(')[0]
                gamer_tag1 = " ".join(gamer_tag1.split())
                gamer_tag2 = i[0][1].split('(')[0]
                gamer_tag2 = " ".join(gamer_tag2.split())
                
                # first if statement ignores any entries that have too much missing data
                if ((full_name1 != '') or (full_name2 != '')) and ((gamer_tag1 != '') or (gamer_tag2 != '')):
                    # if the gamer tags are the same (uncapitalized) and the names are the same
                    # then we automatically pick the left name
                    if (gamer_tag1.lower() == gamer_tag2.lower()) and (full_name1 == full_name2):
                        
                        new_players.append(i[0][0])
                        new_full_names.append(full_name1)
                        new_gamer_tags.append(gamer_tag1)
                        
                        old_players.append(i[0][1])
                        old_full_names.append(full_name2)
                        old_gamer_tags.append(gamer_tag2)
                    else:                   
                        
                        # open 2 webpages so we can more easily look at the information available
                        driver.get('https://lol.fandom.com/wiki/Special:Search?fulltext=1&query=' + gamer_tag1)
                        driver2.get('https://lol.fandom.com/wiki/Special:Search?fulltext=1&query=' + gamer_tag2)
                        
                        
                        # left if the left name should be adhered,
                        # right if the right name should be adhered
                        print(i)
                        print("Same person?, left/right or no")
                        answer = input()
                        
                        # if it is the same person then we change every occurrence of the left/right name to the right/left name
                        # e.g. (('mcscrag (Brendan McGee)', 'mcscrag (Brandon McGee)'), 0.9130434782608695)
                        # clearly the same person, high similarity metric
                        # change every instance of 'mcscrag (Brandon McGee)' to (('mcscrag (Brendan McGee)' if left was typed
                        
                        # if the answer is left, then change all the 2nd names of the comparison to the first names
                        if answer.lower() == 'left':
                            
                            new_players.append(i[0][0])
                            new_full_names.append(full_name1)
                            new_gamer_tags.append(gamer_tag1)
                            
                            old_players.append(i[0][1])
                            old_full_names.append(full_name2)
                            old_gamer_tags.append(gamer_tag2)
                                        
                        if answer.lower() == 'right':
                            
                            new_players.append(i[0][1])
                            new_full_names.append(full_name2)
                            new_gamer_tags.append(gamer_tag2)
                            
                            old_players.append(i[0][0])
                            old_full_names.append(full_name1)
                            old_gamer_tags.append(gamer_tag1)
    
                                    
                        if answer.lower() == 'no':
                            seen_list.append([i[0][0], i[0][1]])
                        new_cnt += 1
                    
            cnt += 1
            
            if new_cnt >= 10:
                break
        except:
            continue
                   
        
    # now we can do all the changes that we've saved
    for ans in range(len(new_players)):
        
        newest_player = new_players[ans]
        newest_full_name = new_full_names[ans]
        newest_gamer_tag = new_gamer_tags[ans]
        
        oldest_player = old_players[ans]
        oldest_full_name = old_full_names[ans]
        oldest_gamer_tag = old_gamer_tags[ans]
        
        # go over the edge list and make changes
        for j in range(len(edge_list_copy['From'])):
            if edge_list_copy['From'][j] == oldest_player:
                edge_list_copy.loc[j, 'From'] = newest_player
            if edge_list_copy['To'][j] == oldest_player:
                edge_list_copy.loc[j, 'To'] = newest_player    
        
        # go over the meta data and make changes
        for j in range(len(meta_data_copy['gamer_tag'])):
            if (" ".join(meta_data_copy['gamer_tag'][j].split()) == oldest_gamer_tag) and (" ".join(meta_data_copy['full_name'][j].split()) == oldest_full_name):
                meta_data_copy.loc[j, 'gamer_tag'] = newest_gamer_tag
                meta_data_copy.loc[j, 'full_name'] = newest_full_name
                
        # change all instances in the teams df too
        for j in range(len(teams_df_copy.columns)):
            for k in range(len(teams_df_copy.iloc[:, j])):
                if teams_df_copy.iloc[:, j][k] == oldest_player:
                    teams_df_copy.iloc[:, j][k] = newest_player  
                        
    # save the seen names list
    if save:
        filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\seen_names.pckl', 'wb')
        pickle.dump(seen_list, filehandler)
        filehandler.close

    # if there are duplicates in the dataframe as a result of the renaming process
    # then we have to group by first to tally up the number of played matches
    # then we can remove the duplicates
    edge_list_copy['n_played'] = edge_list_copy.groupby(['From', 'To', 'Region'])['n_played'].transform('sum')
    edge_list_copy = edge_list_copy.drop_duplicates(subset = ['From', 'To', 'Region'])
    edge_list_copy = edge_list_copy.reset_index(drop = True)    
    
    # drop duplicates in the meta data
    meta_data_copy = meta_data_copy.drop_duplicates()
    meta_data_copy = meta_data_copy.reset_index(drop = True)
    
    new_teams_df = pd.DataFrame(columns = list(teams_df_copy.columns))
    # drop duplicates in the teams dataframe
    for j in teams_df_copy.columns:
        new_column = pd.DataFrame(teams_df_copy.drop_duplicates(subset = [j])[j])
        new_teams_df[list(new_column.columns)[0]] = pd.Series(new_column[list(new_column.columns)[0]])
    
    new_teams_df = new_teams_df.reset_index(drop = True)  
    
    return edge_list_copy, meta_data_copy, new_teams_df



edge_list_cleaner, meta_data_cleaner, teams_df_cleaner = evaluateDuplicates(edge_list, meta_data, teams_df)


edge_list = edge_list_cleaner
meta_data = meta_data_cleaner
teams_df = teams_df_cleaner




# save as csv
#path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
#meta_data.to_csv(path_or_buf = path + 'final_meta_data.csv', index = False)
#teams_df.to_csv(path_or_buf = path + 'final_teams_data.csv', index = False)
#edge_list.to_csv(path_or_buf = path + 'final_refined_edge_list.csv', index = False)
#



# now that we've evaluated duplicate names we should evaluate the edge list
# e.g. A - B and B* - A where B* is now changed to B - A
# this means that A - B is the same edge as B - A, we need to remove one of those
def edgeListDuplicates(edge_list):
    
    # make a copy of the original edge list
    edge_list_copy = edge_list.copy(deep = True)
    edge_list_copy = edge_list_copy.reset_index(drop = True)  
    
    duplicate_entries_index = []
    
    # start the timer
    start = time.time()
    
    # go over the edge list, comparing every entry to every other entry
    for i in range(len(edge_list_copy)):
        if (i % 1000 == 0):
            print(i)
            print('Time taken: ', round(time.time() - start, 4))
            
        
        current_row = edge_list_copy.iloc[i]
        for j in range(i, len(edge_list_copy)):
            if i != j:
                # find out if we have the same edge but reversed
                if (current_row['From'] == edge_list_copy['To'][j]) and (current_row['To'] == edge_list_copy['From'][j]):
                    # find out if that edge is in the same league
                    if current_row['Region'] == edge_list_copy['Region'][j]:
                        # then we sum up the total matches played
                        edge_list_copy.loc[i, 'n_played'] += edge_list_copy['n_played'][j]
                        # and we remove the duplicate edge
                        duplicate_entries_index.append(j)
                        
    edge_list_copy = edge_list_copy.drop(duplicate_entries_index)
    
    return edge_list_copy
    
test = edgeListDuplicates(edge_list)



path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
#test = test.reset_index(drop = True)
#test.to_csv(path_or_buf = path + 'league_2012_2021_edge_list.csv', index = False)










# testing in between to check degrees
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
edge_list = pd.read_csv(path + 'league_2012_2021_edge_list.csv')
meta_data = pd.read_csv(path + 'final_meta_data.csv')
teams_data = pd.read_csv(path + 'final_teams_data.csv')
# check the degrees in case something went wrong

G = nx.Graph()
for i in edge_list.values.tolist():
    nx.add_path(G, (i[0], i[1]))
    
node_list = list(G.nodes())
names = []

sorted(G.degree, key = lambda x: x[1], reverse = True)[0:20]
# two players without a last name have a very high degree, after inspecting their webpages
# it seems like the webscraping progress made an error here, the best thing to do is to remove any mention
# of these two players
names.append('Badgamelol ()')
names.append('西西 ()')
# these players below don't have a last name and messed up the webscraping process
# creating connections where no connections were present
names.append('Eric (Vietnamese Player) ()')
names.append('Kenny (Macao Esports) ()')
names.append('La Ast ()')
names.append('Tenphet ()')
names.append('Ycc (YouthCrew Esports) ()')
names.append('yasupenber ()')

lowest_degree_list = sorted(G.degree, key = lambda x: x[1], reverse = False)[0:20]
# inspect nodes with the lowest degree, theoretically there should not be any nodes with
# a degree less than 4
# there are a few, not a lot of occurrences, mostly because of faulty webscraping after
# inspecting players' pages.
for i in lowest_degree_list:
    if i[1] < 4:
        names.append(i[0])


# clean the edge list
indices = []
for i in names:
    for j in range(len(edge_list)):
        if edge_list['From'][j] == i or edge_list['To'][j] == i:
            indices.append(j)

edge_list = edge_list.drop(indices)
edge_list = edge_list.reset_index(drop = True)
edge_list.to_csv(path_or_buf = path + '/final_main_files/' + 'league_2012_2021_edge_list.csv', index = False)
   
    
# clean the meta data
indices_meta = []
# string splitting and partitioning for names won't work for all names
# so we drop the rows where players have no full name
meta_data.fillna('', inplace = True)

for i in names:
    full_name = i.partition('(')[-1][:-1]
    full_name = " ".join(full_name.split())
    gamer_tag = i.split('(')[0]
    gamer_tag = " ".join(gamer_tag.split())
    
    for j in range(len(meta_data)):
        if meta_data['gamer_tag'][j] == gamer_tag and meta_data['full_name'][j] == full_name:
            indices_meta.append(j)
            
        if meta_data['full_name'][j] == '':
            indices_meta.append(j)
        


meta_data = meta_data.drop(list(set(indices_meta)))
meta_data = meta_data.reset_index(drop = True)
meta_data.to_csv(path_or_buf = path + '/final_main_files/' + 'final_meta_data.csv', index = False)
   

# clean the teams_data, add the columns to a new one so we can squash the data
new_teams_data = pd.DataFrame(columns = teams_data.columns)
for i in teams_data.columns:
    for j in range(len(teams_data[i])):
        for name in names:
            if teams_data[i][j] == name:
                teams_data.loc[j, i] = numpy.nan

            
    new_teams_data[i] = pd.Series(teams_data[i].dropna().reset_index(drop = True))
    
new_teams_data = new_teams_data.reset_index(drop = True)
# drop teams that have NO teammembers
new_teams_data = new_teams_data.dropna(axis = 1, how = 'all')

new_teams_data.to_csv(path_or_buf = path + '/final_main_files/' + 'final_teams_data.csv', index = False)















# create sub_edge_lists from the main edge list
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
edge_list = pd.read_csv(path + '/final_main_files/' + 'league_2012_2021_edge_list.csv')

# there are 16 unique regions/tournaments/leagues
unique_regions = set(edge_list['Region'])
print(len(unique_regions))

csv_collection = {}
for i in unique_regions:
    csv_collection[i] = pd.DataFrame(columns = edge_list.columns)
    

for i in range(len(edge_list)):
    for key in csv_collection:
        if key == edge_list['Region'][i]:
            csv_collection[key] = csv_collection[key].append(edge_list.loc[i], ignore_index = True)


# check if it worked by counting the lengths
len_cnt = 0
for key in csv_collection:
    len_cnt += len(csv_collection[key])
    
len_cnt == len(edge_list)

# now we can save the individual edge lists
for key in csv_collection:
    name_file = key.replace('/', '_')
    csv_collection[key].to_csv(path + 'sub_edge_lists/' + name_file, index = False)


# count the number of edges that have no gamer tag in the first string
cnt = 0
for i in range(len(edge_list)):
    if edge_list['From'][i].split('(')[0] == '' or edge_list['From'][i].split('(')[0] == ' ':
        cnt += 1
    if edge_list['To'][i].split('(')[0] == '' or edge_list['To'][i].split('(')[0] == ' ':
        cnt += 1
        

path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/final_main_files/'
# count the number of players that have no last name
edge_list = pd.read_csv(path + '/final_main_files/' + 'league_2012_2021_edge_list.csv')
meta_data = pd.read_csv(path + '/final_main_files/' + 'final_meta_data.csv')
teams_data = pd.read_csv(path + '/final_main_files/' + 'final_teams_data.csv')
cnt = 0
for i in range(len(meta_data)):
    if meta_data['full_name'][i] == numpy.nan:
        cnt += 1
        





        
        