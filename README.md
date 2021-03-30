# LeagueOfLegendsCompetitiveNetwork
## This repository contains multiple CSV files where each contains information about competitive League of Legends players.

The overarching goal of this project was to acquire data regarding professional LoL, short for League of Legends, players and see how they are connected to one another. The method of acquiring said data will be explained and shared via a python file (see List of contents).



## List of contents
1. Background information
2. league_2012_2021_edge_list.csv
3. meta_data.csv
4. teams_data.csv
5. webscrape.py
6. sub_edge_lists
   1. BRL.csv
   2. IEM.csv
   3. IEM_WORLDS_MSI.csv
   4. LCK.csv
   5. LCL.csv
   6. LCS.csv
   7. LEC.csv
   8. LJL.csv
   9. LL.csv
   10. LPL.csv
   11. MSI.csv
   12. OPL.csv
   13. PCL.csv
   14. TCL.csv
   15. VCS.csv
   16. worlds.csv

## Background information
[League of Legends](https://en.wikipedia.org/wiki/League_of_Legends) is a 2009 multiplayer online battle arena video game developed and published by Riot Games. Two teams battle and attempt to destroy each other's Nexus, the team that succeeds in doing so, wins. Teams are made up of five players though one or more coaches can be present for some phases of the beginning of the game (draft phase). 

## league_2012_2021_edge_list.csv
This csv file contains roughly 42,000 lines (and two columns) and thus 42,000 edges. The edge list is a culmination of several separate edge lists where each separate edge list originated from a different national league (e.g. LCS, LEC or LCK) or large international tournament (e.g. IEM or Worlds) from 2012 to 2021. Due to inconsistent data entry, legal name changes, gamer tag changes and many other issues, this edge list was refined over multiple iterations of cleaning. Additional information regarding the cleaning process can be found in the 'webscrape.py' section. In this edge list, players and coaches are mingled. A link between players and/or coaches is created **if and only if** the two have **actively** played a match together. A coach having coached a match counts as if he or she played with the players from that match. Whereas a substitute player will not be linked to another player if he or she did not play a competitive match together.

## meta_data.csv
The meta_data csv file contains roughly 18,000 lines and six columns. The meta data of every league and tournament was gathered and joined in to a single csv file. The entries in some columns were standardized in order to remove duplicate entries. In this file, however, **ALL** player names and gamer tags are included and all the players' teams and residencies. This means that some players may appear multiple times with different gamer tags though they may be the same person, and vice versa with different last names and the same gamer tag. The format of the meta_data.csv file is as follows, including a few example rows:

gamer_tag | full_name | role | residency | country | team |
------------ | ------------- | ------------- | ------------- | ------------- | -------------
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN
brTT | Felipe Gonçalves | Ad Carry | Unknown/None | brazil | kStars
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN Gaming
LEP | Pedro Luiz Marcari | Top | Brazil | brazil |  KaBuM! Orange

## teams_data.csv
The teams_data csv file is in a wide format, it contains all of the named teams as columns. The rows are the members of that team that **actively** played together, as mentioned in the 2nd paragraph. As a result of the wide variety of teams, including teams that have simply renamed, the number of teams is very large. The resulting dataframe/table that can be created from this file contains 1691 teams with a maximum of 62 players per team.

## webscrape.py
The [lolfandom](https://lol.fandom.com/wiki/League_of_Legends_Esports_Wiki) website was used in order to webscrape the information of every tournament and league. Whether a player actively played a competitive match with another teammate could easily be extracted from pages such as [this](https://lol.fandom.com/wiki/LEC/2019_Season/Spring_Season/Team_Rosters) or more accurately [this](https://lol.fandom.com/wiki/LEC/2019_Season/Spring_Season/Team_Rosters?action=edit&section=1).

The data on these pages was in the following table format where a mark would mean that these players participated in the same match and played together. 

player | team_1 | team_2 | team_3 | 
------------ | ------------- | ------------- | -------------
player_1 | - [x] | - [x] | - [x] |
player_2 | - [x] | - [x] | - [x] |
player_3 | - [x] | - [x] | - [x] |
player_4 | - [x] | - [x] | - [x] |
player_5 | - [x] | - [x] | - [ ] |
coach_1 | - [x] | - [x] | - [x] |
sub_1 | - [ ] | - [ ] | - [x] |

The webscraping process was performed for every major league and tournament. Within every major league, the separate sub tournaments (e.g. play-ins, play-offs etc.) was then found, and subsequently every participating team and their match data was then found. After the extraction of all the edges, team data, and meta data; the tags, last names and gamer tags + last names were compared in the edge list in order to detect if there were duplicate names for the same person. This process was performed for all the individual edge lists, the joined edge list named 'league_2012_2021_edge_list.csv' went through this cleaning process multiple times. In cases where players had multiple gamer tags (e.g. incarnati0n (Nicolaj Jensen) and Jensen (Nicolaj Jensen)) one of the two was overwritten. However, due to inconsistent data entries some players would then receive their old gamer tag rather than their newest gamer tag. 

Again, due to inconsistent data entries, some columns in the meta data csv file had to be standardized. In the 'role' column, entries that were meant to be 'Top Lane' for example, could be denoted by 'T', 't', 'top' and others. This standardization process was repeated for every role. The 'country' column went through a similar process. Lastly, cleaning the 'residency' column proved to be a bit more tricky as some regions were later abandoned and residents from one no longer existing region were then assigned to a larger existing region. For example, the 'residency' column contained data entries such as 'OCE' and 'Oceania' which in October 2020 was dissolved and all players with residency in Oceania would acquire North American residency. This [page](https://lol.fandom.com/wiki/Residency_Requirements) was consulted in order to find such outliers.

## sub_edge_lists

This folder contains all the separate edge lists from each major league and major internation tournament. These files are particularly handy if one wishes to view one specific tournament or league. If they are joined, however, the data will not be clean as players may appear under different names. For instance, Jo "CoreJJ" Yong-in (Hangul: 조용인) appears in the LCS and thus in the LCS.csv file, yet Jo "Core" Yong-in (Hangul: 조용인) will appear in the LCK.csv file as that player played in the LCK under a slightly different gamer tag. The large edge list 'league_2012_2021_edge_list.csv' has been cleaned so that these mistakes won't appear.
