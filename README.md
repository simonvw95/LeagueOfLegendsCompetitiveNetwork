# LeagueOfLegendsCompetitiveNetwork
## This repository contains multiple CSV files where each contains information about competitive League of Legends players.

The overarching goal of this project was to acquire data regarding professional LoL, short for League of Legends, players and see how they are connected to one another. The method of acquiring said data will be explained and shared through a python file (see List of contents).



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
This csv file contains roughly 42,000 lines (and two columsn) and thus 42,000 edges. The edge list is a culmination of several separate edge lists where each separate edge list originated from a different national league (e.g. LCS, LEC or LCK) or large international tournament (e.g. IEM or Worlds). Due to inconsistent data entry, legal name changes, gamer tag changes and many other issues, this edge list was refined over multiple iterations of cleaning. Additional information regarding the cleaning process can be found in the 'webscrape.py' section. In this edge list, players and coaches are mingled. A link between players and/or coaches is created **if and only if** the two have played a match together. A coach having coached a match counts as if her or she played with the players from that match. Whereas a substitute player would not be linked to a player if he or she did not play a competitive match together.

## meta_data.csv
The meta_data csv file contains roughly 18,000 lines and six columns. The meta data of every league and tournament was gathered and joined in to a single csv file. The entries in some columns were standardized in order to remove duplicate entries. In this file, however, **ALL** player names and gamer tags are included and all the players' teams and residencies. This means that some players may appear multiple times with different gamer tags though they may be the same person, and vice versa with different last names and the same gamer tag. The format of the meta_data.csv file is as follows, including a few example rows:

gamer_tag | full_name | role | residency | country | team
------------ | -------------
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN
brTT | Felipe Gonçalves | Ad Carry | Unknown/None | brazil | kStars
brTT | Felipe Gonçalves | Ad Carry | Brazil | brazil | paiN Gaming
LEP | Pedro Luiz Marcari | Top | Brazil | brazil |  KaBuM! Orange

## teams_data.csv
The teams_data csv file is in a wide format, it contains all of the named teams as columns. The rows are the members of that team that __ACTIVELY__ played together, being on a team 

Gamer tags, last names and gamer tags + last names were compared in the edge list in order to detect if there were duplicate names for the same 
