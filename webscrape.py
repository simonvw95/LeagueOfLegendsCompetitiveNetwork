# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 11:22:03 2021

@author: Simon
"""

# import necessary packages
import pandas as pd
import time
import networkx as nx
import re
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


# the leagues and tournaments that were scraped

# LCS
URL = 'https://lol.gamepedia.com/League_Championship_Series'
# LEC
URL = 'https://lol.gamepedia.com/LoL_European_Championship'
# LCK
URL = 'https://lol.gamepedia.com/League_of_Legends_Champions_Korea'
# LPL
URL = 'https://lol.gamepedia.com/LoL_Pro_League'
# CBLOL
URL = 'https://lol.gamepedia.com/Circuit_Brazilian_League_of_Legends'
# OPL (Oceanic Pro League)
URL = 'https://lol.gamepedia.com/Oceanic_Pro_League'
# PCL (Pacific Championship Series)
URL = 'https://lol.gamepedia.com/Pacific_Championship_Series'
# TCL (Turkish Champion League)
URL = 'https://lol.gamepedia.com/Turkish_Championship_League'
# VCS (Vietnam League)
URL = 'https://lol.gamepedia.com/VCS_A/2017_Season'
# LCL (LoL Continental League) # special case
URL = 'https://lol.gamepedia.com/League_of_Legends_Continental_League'
# LJL (LoL Japan League) # special case
URL = 'https://lol.gamepedia.com/League_of_Legends_Japan_League'
# LL (Liga Latinoamerica) # special case
URL = 'https://lol.gamepedia.com/Liga_Latinoam%C3%A9rica'
# MSI (Mid Season Invitationals)
URL = 'https://lol.fandom.com/wiki/Mid-Season_Invitational'
# Worlds (World Championships)
URL = 'https://lol.fandom.com/wiki/World_Championship'
# IEM (Intel Extreme Masters) + ISL
URL = 'https://lol.gamepedia.com/Intel_Extreme_Masters'


# a similarity metric for strings, used for names here
def similarity(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

def getSeasonData(URL, special_case = False, MSI_WORLDS = False, IEM = False):
    
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
    edge_list = []
    gamer_tags = []
    player_names = []
    
    # initialize an empty meta dataframe
    meta_data = pd.DataFrame(columns = list(['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team']))
    

    # go over every hyperlink (every tournament)
    for link in links:
        
        # start the timer
        start_time = time.time()
        
        # find the name of the tournament
        last_fwd_slash = link.rfind('/')
        tourn_title = link[last_fwd_slash + 1:]
        print(tourn_title)
        
        # go over every possible team, number from 1 to 30, (max is 17 I believe but just incase)
        for team_no in range(1, 30):
            team_links = link + "/" + "Team_Rosters?action=edit&section=" + str(team_no)
            
            # try except block incase something goes wrong, sometimes data entry is faulty
            try:

                # get the page of the team in that specific tournament
                driver.get(team_links)
                
                # check if the page exists, if it doesn't then it asks you to login to create the page
                # or says that you don't have permission
                # if this is the case then ignore this 'tournament' as it is not a tournament
                
                login_req_page = driver.find_elements_by_class_name('firstHeading')
                break_main = False
                
                for header in login_req_page:
                    if header.text == 'Login required' or header.text == 'Permission error':
                        print('Skipping: ' + tourn_title + " " + str(team_no))
                        break_main = True
                        break
                    
                if break_main:
                    break
                
                # get the box of text with the desired content
                textboxs = driver.find_elements_by_class_name('mw-editfont-default')
                
                # turn it into clean text
                if textboxs:
                    clean_text = textboxs[-1].text
                    
                    # extract the team name
                    team_name = clean_text.partition("{{team|")[2].partition("}}")[0]

                    # get the lines that contain player info
                    players = []
                    # add a counter incase data entry is irregular and the code doesn't know it should be done
                    cnt = 0
                    while 'name=' in clean_text:
                        if 'ExtendedRosterLine' in clean_text:
                            players.append(clean_text.partition("{{ExtendedRosterLine")[2].partition("}}")[0])
                            clean_text = clean_text.replace("{{ExtendedRosterLine" + players[-1] + "}}", "")
                        if 'RosterLineOld' in clean_text:
                            players.append(clean_text.partition("{{RosterLineOld")[2].partition("}}")[0])
                            clean_text = clean_text.replace("{{RosterLineOld" + players[-1] + "}}", "")
                        cnt += 1
                        if cnt > 100:
                            break
                        
                    # get their gamer tag and actual name
                    player_tags = []
                    for i in range(len(players)):
                        gamer_tag = players[i].partition("|player=")[2].partition("|")[0] 
                        
                        name = players[i].partition("|name=")[2].partition("|")[0]
                        
                        # remove unnecessary spaces
                        gamer_tag = " ".join(gamer_tag.split())
                        name = " ".join(name.split())
                        
                        # go over all the exctracted player names
                        for n in range(len(player_names)):
                            # if we have a full match then use the name we have
                            if (similarity(name, player_names[n]) > 0.95):
                                name = player_names[n]
                                gamer_tag = gamer_tags[n]
                                break
                            
                            # sometimes a full match doesn't work if certain letters are capitalized
                            if re.search(name, player_names[n], re.IGNORECASE):
                                name = player_names[n]
                                gamer_tag = gamer_tags[n]
                                break
                            else:
                            # if we don't have a full match then check if the gamer tag and name matches to a certain degree
                                if (similarity(gamer_tag, gamer_tags[n]) > 0.9):
                                    # check for similarity in names
                                    if (similarity(name, player_names[n]) > 0.85):
                                        name = player_names[n]
                                        gamer_tag = gamer_tags[n]
                                        break
                                        

                        # only add gamer tag and player name to the big list if the name isn't already in there
                        if name not in player_names:
                            
                            gamer_tags.append(gamer_tag)
                            player_names.append(name)

                        player_tags.append(gamer_tag + " (" + name + ")")
                        
                        # meta data df order: list(['gamer_tag', 'full_name', 'role', 'residency', 'country'])
                        role = " ".join(players[i].partition("|role=")[2].partition("|")[0].split())
                        residency = " ".join(players[i].partition("|res=")[2].partition("|")[0].split())
                        country = " ".join(players[i].partition("|flag=")[2].partition("|")[0].split())
                        temp_df = {'gamer_tag' : gamer_tag, 'full_name' : name, 'role' : role, 'residency' : residency, 'country' : country, 'team' : team_name}
                        
                        meta_data = meta_data.append(temp_df, ignore_index = True)
                        
                    # add new data to an existing team name column if the column already exists
                    if team_name in teams_df.columns:
                        temp_df = pd.DataFrame()
                        temp_df[team_name] = pd.Series(player_tags)
                        teams_df = teams_df.merge(temp_df, left_on = team_name, right_on = team_name, how = 'outer')
                    # add the team to the dataframe if it isn't in there
                    else:
                        teams_df[team_name] = pd.Series(player_tags)                       
                    
                    # extract the info about players having played a match together
                    matching_play_matrix = []
                    for i in range(len(players)):
                        matching_play_matrix.append(players[i].partition("|r=")[2].partition("|")[0])
                        players[i] = players[i].replace("|r=" + matching_play_matrix[-1] + "}}", "")
        
                    # create a dict that gives each player their own list of played matches
                    id_match_matrix = {}
                    for i in range(len(player_tags)):
                        id_match_matrix[player_tags[i]] = matching_play_matrix[i]
                        
                    # go over every person twice (for each person match that person with an other person on the same team)
                    for i in id_match_matrix:
                        for j in id_match_matrix:
                            # skip if the person is matching with him/herself
                            if i != j:
                                # go over every match in the match list
                                for k in range(len(id_match_matrix[j])):
                                    try:
                                        # if they both have a 'y' then it means they played together
                                        if id_match_matrix[i][k] == 'y' and id_match_matrix[j][k] == 'y':
                                            # create a tuple and reverse that tuple
                                            tup = [i, j]
                                            reverse_tup = tup[::-1]
                                            # if the tuple or the reverse of that tuple is not in the edge list, then add it
                                            if [tup[0], tup[1]] not in edge_list and [reverse_tup[0], reverse_tup[1]] not in edge_list:
                                                edge_list.append([tup[0], tup[1]])
                                    except IndexError:
                                        continue
                        
                            
                            
        
            except Exception as e:
                print(e)
    
        end_time = time.time()
        
        print("Extracting tournament info took: ", round(end_time - start_time, 4), " seconds.")
        print("")
    # remove unnecessary nan values that make the df longer
    teams_df = teams_df.apply(lambda x: pd.Series(x.dropna().values))
    # remove duplicate rows in meta data
    meta_data = meta_data.drop_duplicates()
    
    return edge_list, teams_df, meta_data
     
edge_list, teams_df, meta_data = getSeasonData(URL, IEM = True)
            

seen_list = []

def evaluateDuplicates(edge_list, check_last_names = False, check_gamer_tag = False):
    
    # turn the edge list into a graph so we can get a list of nodes
    G = nx.Graph()
    for i in edge_list:
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
                if check_last_names:
                    name_1 = node_list[i].partition('(')[2]
                    name_2 = node_list[j].partition('(')[2]
                    empty_dict[(node_list[i], node_list[j])] = similarity(name_1, name_2)
                elif check_gamer_tag:
                    name_1 = node_list[i].split('(')[0]
                    name_2 = node_list[j].split('(')[0]
                    empty_dict[(node_list[i], node_list[j])] = similarity(name_1, name_2)
                else:
                    empty_dict[(node_list[i], node_list[j])] = similarity(node_list[i], node_list[j])
                
    # copy the original edge list and start two counters
    edge_list_copy = edge_list.copy()
    cnt = 0
    new_cnt = 0
    
    # sort the list based on the names their similarity
    sorted_list = list(sorted(empty_dict.items(), key = lambda item: item[1], reverse = True))
    
    while True:
        i = sorted_list[cnt]
        
        try:
            if [i[0][0], i[0][1]] not in seen_list:
                print(i)
                print("Same person?, Yes or no")
                answer = input()
                
                # if it is the same person then we change every occurrence of the 2nd name to the 1st name
                # e.g. (('mcscrag (Brendan McGee)', 'mcscrag (Brandon McGee)'), 0.9130434782608695)
                # clearly the same person, high similarity metric
                # change every instance of 'mcscrag (Brandon McGee)' (2nd) to (('mcscrag (Brendan McGee)'
                if answer.lower() == 'yes':
                    for j in edge_list_copy:
                        if j[0] == i[0][1]:
                            j[0] = i[0][0]
                        if j[1] == i[0][1]:
                            j[1] = i[0][0]
                if answer.lower() == 'no':
                    seen_list.append([i[0][0], i[0][1]])
                new_cnt += 1
                
            cnt += 1
            
            if new_cnt >= 10:
                break
        except:
            continue
        

    edge_list_newest = []
    for i in edge_list_copy:
        if i not in edge_list_newest:
            edge_list_newest.append(i)
            
            
    return edge_list_newest

edge_list_final = evaluateDuplicates(edge_list)
edge_list = edge_list_final



# save the edge_list LCS
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LCS.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close


# save the edge_list LEC
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LEC.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close


# save the edge_list LCK
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LCK.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close


# save the edge_list LPL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LPL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list brazilian leagues
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\BRL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list OPL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\OPL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list PCL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\PCL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list TCL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\TCL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list VCS
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\VCS.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list LCL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LCL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list LJL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LJL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list LL
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\LL.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list Worlds
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\worlds.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list MSI
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\MSI.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close

# save the edge_list IEM
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\IEM.pckl', 'wb')
#pickle.dump([edge_list, teams_df, meta_data], filehandler)
#filehandler.close


file = pd.read_csv('C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/final_edge_list.csv')
long_edge_list = file.values.tolist()


# concatenating all edge lists
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
all_pickles = os.listdir(path)
long_edge_list = []
long_teams_df = pd.DataFrame()
long_meta_data = pd.DataFrame(columns = list(['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team']))
for i in all_pickles:
    if i[-5:] == '.pckl':
        file = open(path + i, 'rb')
        file_content = pickle.load(file)
        file.close
        long_edge_list += file_content[0]
        long_teams_df = pd.concat([long_teams_df, file_content[1]], axis = 1)
        long_meta_data = long_meta_data.append(file_content[2], ignore_index = True)
        

# clean up the long edge list by finding similar names
edge_list_final = evaluateDuplicates(long_edge_list)
long_edge_list = edge_list_final

edge_list_df = pd.DataFrame(edge_list_final, columns = list(['From', 'To']))
edge_list_df.to_csv(path_or_buf = path + 'final_edge_list.csv', index = False)

############################## Worlds MSI and IEM were added later, separate code for that
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
long_edge_list = []
long_teams_df = pd.DataFrame()
long_meta_data = pd.DataFrame(columns = list(['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team']))
for i in ['MSI.pckl', 'worlds.pckl', 'IEM.pckl']:
    file = open(path + i, 'rb')
    file_content = pickle.load(file)
    file.close
    long_edge_list += file_content[0]
    long_teams_df = pd.concat([long_teams_df, file_content[1]], axis = 1)
    long_meta_data = long_meta_data.append(file_content[2], ignore_index = True)

edge_list_final = evaluateDuplicates(long_edge_list)
long_edge_list = edge_list_final

# save the edge_list international tournaments
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\IEM_WORLDS_MSI.pckl', 'wb')
#pickle.dump([long_edge_list, long_teams_df, long_meta_data], filehandler)
#filehandler.close


# add the final edge list to the internation tournaments edge list
long_teams_df = pd.DataFrame()
long_meta_data = pd.DataFrame(columns = list(['gamer_tag', 'full_name', 'role', 'residency', 'country', 'team']))

file = open(path + '/IEM_WORLDS_MSI.pckl', 'rb')
file_content = pickle.load(file)
file.close
long_edge_list = file_content[0]
long_teams_df = pd.concat([long_teams_df, file_content[1]], axis = 1)
long_meta_data = long_meta_data.append(file_content[2], ignore_index = True)

# join the teams data
large_teams_df = pd.read_csv(path + '/teams_data.csv')
long_teams_df = long_teams_df.drop([''], axis = 1)
long_teams_df = long_teams_df.apply(lambda x: pd.Series(x.dropna().values))

long_teams_df = pd.concat([large_teams_df, long_teams_df], axis = 1)
long_teams_df.to_csv(path_or_buf = path + 'teams_data.csv', index = False)

# join the meta data
large_meta_data = pd.read_csv(path + '/meta_data.csv')
large_meta_data = large_meta_data.append(long_meta_data, ignore_index = True)
long_meta_data = large_meta_data
# remove redundancies again, see below


# join the edge lists
large_edge_list = pd.read_csv(path + 'final_edge_list.csv')
large_edge_list = large_edge_list.values.tolist()
long_edge_list = large_edge_list + long_edge_list
# clean them up again
edge_list = evaluateDuplicates(long_edge_list, check_gamer_tag = True)
# 44k, 42833, 42534, 42371, 42324, 42267, 42225, 42200, 42191, 42190, 42185, 42180
long_edge_list = edge_list

# save for use later
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\final_edge_list.pckl', 'wb')
#pickle.dump([edge_list], filehandler)
#filehandler.close
#
#filehandler = open(r'C:\Users\Simon\OneDrive\Documents\GitHub\LeagueTeamsNetwork\names_seen_list.pckl', 'wb')
#pickle.dump([seen_list], filehandler)
#filehandler.close

edge_list_df = pd.DataFrame(long_edge_list, columns = list(['From', 'To']))
edge_list_df.to_csv(path_or_buf = path + 'league_2012_2021_edge_list.csv', index = False)

##############################

# clean up the meta data information, can check for redundancies in the role residency and country
def removeRedundancies(df, column, collection, lower = False):
    print(set(df[column]))
    for i in range(len(df[column])):
        for j in collection:
            if df[column][i] in collection[j]:
                df[column][i] = j
                
        if lower:
            df[column][i] = df[column][i].lower()
    print()
    print(set(df[column]))
    
    
role_coll = {}
role_coll['Top'] = ['Top <!--Played as "Yoyo" for the first three rounds-->', 'Top', 't', 'toplane', 'Top <!--李东秀-->', 'top', 'Top <!--Played as "noko" in Round 2-->', 'Toplane', 'Sub/Top', 'T', 'Top Laner']
role_coll['Jungle'] = ['Sub/Jungle', 'Jungle', 'j', 'Jungle <!--申岷升-->', 'J', 'jungle', 'Jungler']
role_coll['Mid'] = ['Mid', 'm', 'Sub/Mid', 'Mid Laner', 'M', 'mid', 'Midlane', 'AP']
role_coll['Ad Carry'] = ['Sub/AD', 'Bot Laner', 'b', 'A', 'bot', 'a', 'Bot', 'AD', 'AD Carry', 'Ad', 'ad']
role_coll['Support'] = ['Support', 'Sub/Support', 'support', 'sup', 'S', 's']
role_coll['Coach'] = ['c', 'C', 'c--> {{ExtendedRosterEnd', 'Coach', 'Assistant Coach', 'Head Coach', 'Strategic Coach', 'coach']
role_coll['Substitute'] = ['Sub', 'sub', 'Substitute']
role_coll['Unknown'] = ['']

removeRedundancies(long_meta_data, 'role', role_coll)

            
resid_coll = {}
resid_coll['Unknown/None'] = ['', 'Unrecognized Region', 'none', '??', 'None', 'Unknown', 'unknown', 'nan', numpy.nan]
resid_coll['North America'] = ['na', 'North America', 'Oceania', 'oce', 'OCE', 'oceania', 'NA']
resid_coll['Europe'] = ['Europe', 'eu', 'europe', 'EU']
resid_coll['South Korea'] = ['South Korea', 'kr', 'KR', 'Korea']
resid_coll['China'] = ['cn', 'CN', 'China', 'china']
resid_coll['PCS (Pacific Championship Series)'] = ['PCS', 'lms', 'Taiwan', 'Taiwan, Hong Kong, and Macao', 'LMS', 'pcs', 'sea', 'tw', 'SEA', 'TW', 'Southeast Asia']
resid_coll['Brazil'] = ['BR', 'br', 'Brazil']
resid_coll['CIS (Commonwealth of Independent States)'] = ['cis', 'CIS', 'ru', 'Commonwealth of Independent States']
resid_coll['Japan'] = ['Japan', 'jp', 'JP']
resid_coll['Latin America'] = ['LAT', 'Latin America', 'LAS', 'lat', 'las', 'LAN', 'lan']
resid_coll['Turkey'] = ['tr', 'TR', 'Turkey']
resid_coll['Vietnam'] = ['vn', 'vyn', 'Vietnam', 'VN']

removeRedundancies(long_meta_data, 'residency', resid_coll)


country_coll = {}
country_coll['China'] = ['China', 'cn', 'CN', 'china', 'cn<!--assumed-->', 'Cm']
country_coll['South Korea'] = ['South Korea', 'Korea', 'kr', 'south korea', 'KR']
country_coll['Germany'] = ['Germany', 'DE', 'de', 'germany']
country_coll['United Kingdom'] = ['UK', 'uk', 'United Kingdom']
country_coll['Belgium'] = ['BE', 'Belgium', 'Be', 'be', 'belgium']
country_coll['Netherlands'] = ['Netherlands', 'netherlands', 'nl', 'NL']
country_coll['Vietnam'] = ['Vietnam', 'VN', 'vietnam']
country_coll['United States'] = ['United States', 'us', 'usa', 'USA', 'US']
country_coll['Denmark'] = ['Denmark', 'dk', 'DK', 'Dk']
country_coll['Brazil'] = ['Brazil', 'BR', 'Br', 'br']
country_coll['France'] = ['France', 'FR', 'fr', 'Fr']
country_coll['Italy'] = ['Italy', 'it', 'IT']
country_coll['New Zealand'] = ['NZ', 'nz', 'Nz']
country_coll['Canada'] = ['CA', 'Canada', 'Ca', 'ca']
country_coll['Sweden'] = ['Sweden', 'sweden']
country_coll['Unknown'] = ['Unknown', 'none', numpy.nan]

removeRedundancies(long_meta_data, 'country', country_coll, lower = True)

# drop the duplicates
long_meta_data = long_meta_data.drop_duplicates()

# save as csv
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
long_meta_data.to_csv(path_or_buf = path + 'meta_data.csv', index = False)
long_teams_df.to_csv(path_or_buf = path + 'teams_data.csv', index = False)
edge_list_df = pd.DataFrame(edge_list_final, columns = list(['From', 'To']))
edge_list_df.to_csv(path_or_buf = path + 'final_edge_list.csv', index = False)


# create sub_edge_lists from the pckl files
path = 'C:/Users/Simon/OneDrive/Documents/GitHub/LeagueTeamsNetwork/'
all_pickles = os.listdir(path)
for i in ['final_edge_list.csv', 'final_edge_list.pckl', 'league_2012_2021_edge_list.csv', 'meta_data.csv', 'names_seen_list.pckl', 'sub_edge_lists', 'teams_data.csv', 'webscrape.py']:
    all_pickles.remove(i)

for i in all_pickles:
    file = open(path + i, 'rb')
    file_content = pickle.load(file)
    file.close
    edge_list = file_content[0]
    edge_list_df = pd.DataFrame(edge_list, columns = list(['From', 'To']))
    edge_list_df.to_csv(path_or_buf = path +  '/sub_edge_lists/' + i.split('.')[0] + '.csv', index = False)


teams_df = pd.read_csv(path + 'teams_data.csv')
