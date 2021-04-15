# Analysis

Questions to answer:
Considering an undirected Graph G:

1. Which region is the most interconnected?
2. Which region is the most intraconnected?
3. Which players are the most interconnected?
4. Which players are the most intraconnected?
5. Who is the 'Kevin Bacon' of the League of Legends community?
6. Which coach is the most connected?


## Descriptive statistics
Descriptive statistics of the graph

Region | Nodes | Edges | Density | Days Active
------------ | ------------- | ------------- | ------------- | -------------
LJL/Japan |211 | 1155 | 0.0521 | 2259
LL/Latin America |138 | 643 | 0.0680 | 803
LPL/China |1073 | 8109 | 0.0141 | 2984
OPL/Oceania |382 | 2223 | 0.0305 | 2032
LCS/North America |568 | 4642 | 0.0288 | 2975
MSI |251 | 757 | 0.0241 | NA
LEC/Europe |805 | 4614 | 0.0143 | 2973
WORLDS |608 | 2146 | 0.0116 | NA
LMS/Taiwan + Hong Kong + Macao |394 | 2628 | 0.0339 | 1718
LST/Southeast Asia |78 | 209 | 0.0696 | 399
LCK/South Korea |649 | 4397 | 0.0209 | 2829
TCL/Turkey |586 | 4160 | 0.0243 | 2259
PCL/PCS |126 | 474 | 0.0602 | 397
CBLOL/Brazil |406 | 3670 | 0.0446 | 2532
VCS/Vietnam |182 | 1441 | 0.0875 | 1706
LCL/Russia |198 | 1010 | 0.0518 | 1902
All |4966 | 39620 | 0.0032 | NA

## Visual Inspection

### LCK & LPL & LEC & LCS
<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/LCK_LPL_LEC_LCS_legend.png" alt="Test" width="1024" height="1024">

### TCL & CBLOL & LMS & OPL
<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/TCL_CBLOL_LMS_OPL_legend.png" alt="Test" width="1024" height="1024">

### LL & PCL & LST
<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/LL_PCL_LST_legend.png" alt="Test" width="1024" height="1024">

### VCS & LJL & LCL
<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/VCS_LJL_LCL_legend.png" alt="Test" width="1024" height="1024">

## Network properties

### Degree

<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/degree_distribution.png" alt="Test" width="512" height="512">
### Components

### Distance
Not factoring in weights.

Measurement | Value | Node 1 | Node 2
------------ | ------------- | ------------- | ------------- 
Average Distance | 4.39  | NA | NA
Diameter (Longest Distance) | 11  | HellMa (Anastasiya Pleyko) \*| CYH (Chen Yi-Hui (陈艺辉)) \*
Shortest Average Distance |  GBM (Lee Chang-seok (이창석)) | 3.15 | NA
Longest Average Distance | Azure (Noel Christopher Cuadra) (Noel Christopher Cuadra)  | 7.27 | NA

\* There were 30 total paths with a length of 11, the edge chosen is one of them.
### Clustering coefficient

### Triangles
