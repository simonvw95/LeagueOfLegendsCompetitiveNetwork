# LeagueOfLegendsCompetitiveNetwork

# Under construction, webscraping process is being repeated in order to weed out mistakes and add additional data to the edge list.

## This repository contains multiple CSV files where each contains information about competitive League of Legends players.

The overarching goal of this project was to acquire data regarding professional LoL, short for League of Legends, players and see how they are connected to one another. The method of acquiring said data will be explained and shared via a python file (see List of contents).



## List of contents
1. Background information
2. league_2012_2021_edge_list.csv
3. final_meta_data.csv
4. final_teams_data.csv
5. webscrape.py / Data Gathering
6. sub_edge_lists
   1. CBLOL_Brazil.csv
   2. LCK_South Korea.csv
   3. LCL_Russia.csv
   4. LCS_North America.csv
   5. LEC_Europe.csv
   6. LJL_Japan.csv
   7. LL_Latin America.csv
   8. LMS_Taiwan + Hong Kong + Macao.csv
   9. LPL_China.csv
   10. LST_Southeast Asia.csv
   11. MSI.csv
   12. OPL_OCeania.csv
   13. PCL_PCS.csv
   14. TCL_Turkey.csv
   15. VCS_Vietnam.csv
   16. WORLDS.csv

## Background information
[League of Legends](https://en.wikipedia.org/wiki/League_of_Legends) is a 2009 multiplayer online battle arena video game developed and published by Riot Games. Two teams battle and attempt to destroy each other's Nexus, the team that succeeds in doing so, wins. Teams are made up of five players though one or more coaches can be present for some phases of the beginning of the game (draft phase). 

## league_2012_2021_edge_list.csv
This csv file contains roughly 42,000 lines (and four columns) and thus 42,000 edges. The edge list is a culmination of several separate edge lists where each separate edge list originated from a different national league (e.g. LCS, LEC or LCK) or large international tournament (e.g. MSI or Worlds) from 2012 to 2021. Due to inconsistent data entry, legal name changes, gamer tag changes and many other issues, this edge list was refined over multiple iterations of cleaning. Additional information regarding the cleaning process can be found in the 'webscrape.py' section. In this edge list, players and coaches are mingled. A link between players and/or coaches is created **if and only if** the two have **actively** played a match together. A coach having coached a match counts as if he or she played with the players from that match. Whereas a substitute player will not be linked to another player if he or she did not play a competitive match together. The csv file looks like the following table:

From | To | n_played | Region | 
------------ | ------------- | ------------- | -------------
Alocs (Leonardo Belo) | Leko (Whesley Holler) | 17 | CBLOL/Brazil
Alocs (Leonardo Belo) | Revolta (Gabriel Henud) | 21 | CBLOL/Brazil
Alocs (Leonardo Belo) | manajj (André Rocha) | 17 | CBLOL/Brazil
Alocs (Leonardo Belo) | takeshi (Murilo Alves) | 39 | CBLOL/Brazil
Leko (Whesley Holler) | Revolta (Gabriel Henud) | 37 | CBLOL/Brazil
Leko (Whesley Holler) | manajj (André Rocha) | 17 | CBLOL/Brazil
Leko (Whesley Holler) | takeshi (Murilo Alves) | 37 | CBLOL/Brazil

The edge list was meant for undirected networks, the existence of a connection such as (Alocs (Leonardo Belo), Leko (Whesley Holler)) implies the existence of the reverse connection (Leko (Whesley Holler), Alocs (Leonardo Belo)). The 'n_played' column denotes the number of matches a pair of players played together. The 'Region' column indicates in which region these two players played together. A duplicate edge **is possible** if the two players played together in a different region or at MSI/Worlds. Furthermore, the region entries indicate the main league plus the region as there are amateur leagues a grade lower than the main league: e.g. LCS/North America would also include the NA Challenger Series and LCS Academy League.

## final_meta_data.csv
The final_meta_data csv file contains roughly 18,000 lines and six columns. The meta data of every league and tournament was gathered and joined in to a single csv file. The entries in some columns were standardized in order to remove duplicate entries (e.g. adc/ADC/carry/bot were rewritten to Ad Carry). Duplicate entries may still appear due to missing data, inconsistent team naming or multiple roles/teams per player. The format of the meta_data.csv file is as follows, including a few example rows:

gamer_tag | full_name | role | residency | country | team |
------------ | ------------- | ------------- | ------------- | ------------- | -------------
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN
brTT | Felipe Gonçalves | Ad Carry | Unknown/None | brazil | kStars
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN Gaming
LEP | Pedro Luiz Marcari | Top | Brazil | brazil |  KaBuM! Orange

## final_teams_data.csv
The final_teams_data csv file is in a wide format, it contains all of the named teams as columns. The rows are the members of that team that **actively** played together, as mentioned in the 2nd paragraph. As a result of the wide variety of teams, including teams that have simply renamed, the number of teams is very large. The resulting dataframe/table that can be created from this file contains 1529 teams with a maximum of 51 players per team.

CNB | KaBuM | kStars | .....
------------ | ------------- | ------------- | .....
Alocs (Leonardo Belo) | Espeon (Martin Gonçalves) | SuNo (An Sun-ho (안순호)) | .....
Leko (Whesley Holler) | LEP (Pedro Luiz Marcari) | Winged (Park Tae Jin (박태진)) | .....
manajj (André Rocha) | Danagorn (Daniel Drummond) | Mylon (Matheus Borges) | .....
Revolta (Gabriel Henud) | TinOwns (Thiago Sartori) | brTT (Felipe Gonçalves) | .....
takeshi (Murilo Alves) | bit1 (Bruno Lima) | Loop (Caio Almeida) | .....
Aoshi (Franklin Coutinho) | nan | Winged (Park Tae-jin (박태진)) | .....


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

The webscraping process was performed for every major league and tournament, they are denoted in the 'sub_edge_lists' paragraph. Within every major league, the separate sub tournaments (e.g. play-ins, play-offs etc.) was then found, and subsequently every participating team and their match data was then found. After the extraction of all the edges, team data, and meta data, the three types of data were joined into three massive datasets.

Due to inconsistent data entries (missing middle names/last names/nicknames/foreign translation), legal name changes, and gamer tag changes the players had to be compared to each other. Every single player was compared to every other player and their name similarity was sorted. This was done semi-manually, if the last names were the same and the gamer tag was the same except for capitalization, then the first occurrence of the name would overwrite the other occurrences. In the manual process, a script automatically opened two web pages each with a gamer tag, the two pages were then visually inspected to see if they were the same player. The players' full names (minus the gamer tags), their gamer tags, and their gamer tags plus the full names were compared in order to weed out duplicate mentions of the same player. Some examples of inconsistent entries:

Comparison of gamer tags exposed this:
**Nyjacky (Chenglong "Jacky" Wang) - Nyjacky (Chenglong Wang) - 1.0**
Comparison of full names exposed this:
**Jensen (Nicolaj Jensen) - Incarnati0n (Nicolaj Jensen) - 1.0**
Comparison of gamer tags and full names exposed this:
**catjug (Chen Yi-Jie (陈艺杰)) - catjungle (Chen Yi-Jie) - 0.82**

A value of 1.0 meant that the string comparison was a 1 to 1 result, a perfect match. This cleaning process was repeated until no duplicates could be found. However, there may still be duplicates that could not be spotted. In most cases the most recent and accurate name was chosen to replace the older names.

Again, due to inconsistent data entries, some columns in the meta data csv file had to be standardized. In the 'role' column, entries that were meant to be 'Top Lane' for example, could be denoted by 'T', 't', 'top' and others. This standardization process was repeated for every role. The 'country' column went through a similar process. Lastly, cleaning the 'residency' column proved to be a bit more tricky as some regions were later abandoned and residents from one no longer existing region were then assigned to a larger existing region. For example, the 'residency' column contained data entries such as 'OCE' and 'Oceania' which in October 2020 was dissolved and all players with residency in Oceania would acquire North American residency. This [page](https://lol.fandom.com/wiki/Residency_Requirements) was consulted in order to find such outliers.


## sub_edge_lists

This folder contains all the separate edge lists from each major league and major internation tournament. These files are particularly handy if one wishes to view one specific tournament or league. These sub edge lists were extracted from the main edge list via sorting by 'Region' and saving the individual csv files.

The table below depicts the ranges of each league/tournament. Ongoing indicates that the particular league is currently still active. Mix indicates that the csv file contains a mix of multiple tournaments. The % Collected column indicates the amount of data that could be collected using a reliable method. In most cases all of the data could be collected **except** for the Qualifiers tournaments which were apart of nearly all leagues. In very few cases, data was simply not available in the table format as presented in the beginning of the previous paragraph. For example, the OPL has listed 24 Main Events and 8 Qualifiers of which 24 and and 7 could be webscraped, respectively, giving us a % Collected of 31/32 * 100 = 96.9%. 

League/Tournament | Start | End | Start Data Collection | End Data Collection | % Collected
------------ | ------------- | ------------- | ------------- | ------------- | -------------
CBLOL | 26-04-2014 | Ongoing | 26-4-2014 | 31-3-2021 | 100%
IEM_WORLDS_MSI | Mix | Mix | Mix | 31-3-2021 | 
LCK | 21-03-2012 | Ongoing | 03-07-2013 | 31-3-2021 | 78.8%
LCL | 16-01-2016 | Ongoing | 16-01-2016 | 31-3-2021 | 100%
LCS | 13-01-2013 | Ongoing | 07-02-2013 | 31-3-2021 | 98.0% 
LEC | 12-12-2012 | Ongoing | 07-02-2013 | 31-3-2021 | 81.8% 
LJL | 09-02-2014 | Ongoing | 24-01-2015 | 31-3-2021 | 86.1%
LL | 19-01-2019 | Ongoing | 19-01-2019 | 31-3-2021 | 100% 
LPL | 29-01-2013 | Ongoing | 16-03-2013 | 31-3-2021 | 93.0%
MSI | 07-05-2015 | Ongoing | 07-05-2015 | 31-3-2021 | 100%
OPL | 10-01-2015 | 28-08-2020 | 05-02-2015 | 28-08-2020 | 96.9%
PCS | 29-02-2020 | Ongoing | 29-02-2020 | 31-3-2021 | 100% 
TCL | 01-12-2013 | Ongoing | 24-01-2015 | 31-3-2021 | 80.5%
VCS | 02-11-2013 | Ongoing | 30-07-2016 | 31-3-2021 | 65.1%
WORLDS | 18-06-2011 | Ongoing | 04-10-2012 | 31-3-2021 | 90%
