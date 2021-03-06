# Analysis

Questions to answer:
Considering an undirected Graph G:

1. Which region is the most interconnected?
2. Which region is the most intraconnected?
3. Which players are the most connected between regions?
4. Which players are the most connected within regions?
5. Who is the 'Kevin Bacon' of the League of Legends community?
6. Which coach is the most connected?


## Descriptive statistics
Descriptive statistics of the graph

Region | Nodes | Edges | Density | Triangles | Average Clustering Coefficient | Days Active
------------ | ------------- | ------------- | ------------- | ------------- | ------------- | -------------
LJL/Japan | 208 | 1128 | 0.0524 | 2067 | 0.68 | 2259
LL/Latin America | 138 | 643 | 0.068 | 1126 | 0.74 | 803
LPL/China | 1069 | 8098 | 0.0142 | 20885 | 0.59 | 2984
OPL/Oceania | 376 | 2207 | 0.0313 | 3592 | 0.59 | 2032
LCS/North America | 567 | 4639 | 0.0289 | 12187 | 0.62 | 2975
LEC/Europe | 805 | 4614 | 0.0143 | 9309 | 0.69 | 2973
LMS/Taiwan + Hong Kong + Macao | 388 | 2581 | 0.0344 | 8043 | 0.7 | 1718
LST/Southeast Asia | 77 | 205 | 0.0701 | 249 | 0.88 | 399
LCK/South Korea | 648 | 4396 | 0.021 | 9403 | 0.62 | 2829
TCL/Turkey | 584 | 4148 | 0.0244 | 8546 | 0.62 | 2259
PCL/PCS | 125 | 472 | 0.0609 | 837 | 0.83 | 397
CBLOL/Brazil | 406 | 3670 | 0.0446 | 16853 | 0.66 | 2532
VCS/Vietnam | 181 | 1410 | 0.0866 | 3416 | 0.59 | 1706
LCL/Russia | 198 | 1010 | 0.0518 | 1620 | 0.67 | 1902
WORLDS | 608 | 2146 | 0.0116 | 3245 | 0.84 | NA
MSI | 251 | 757 | 0.0241 | 1095 | 0.91 | NA
All | 4940 | 42124 | 0.0035 | 100219 | 0.59 | NA

\* The number of triangles in the row 'All' are not equivalent to the sum of the triangles of the other rows. In the visualizations and other analyses, the full Graph (All) is a MultiGraph, where more than one edge can occur between two nodes. However, counting triangles for MultiGraphs is not particularly easy, therefore the triangle calculation was done on a Graph instance of the 'All' network. This may be updated later as there is a [method](https://www.researchgate.net/publication/258114016_When_a_Graph_is_not_so_Simple_Counting_Triangles_in_Multigraph_Streams) for triangle calculation for MultiGraphs 
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
Not factoring in weights, applied to the largest connected component.

Region | Average Distance | Diameter (Longest Distance) | Shortest Average Distance & Node | Longest Average Distance & Node
------------ | ------------- | ------------- | ------------ | ------------- | 
LJL/Japan | 2.68 | 5 | 1.93 (Paz (Shirou Sasaki (????????? ??????))) | 3.45 (Dicey (Daisuke Ashida))
LL/Latin America | 2.78 | 5 | 2.01 (Baula (Alejandro Serrano)) | 3.5 (Jirall (Daniel del Castillo))
LPL/China | 3.27 | 8 | 2.47 (Amazing (Liu Shi-Yu) (Liu Shi-Yu (?????????))) | 5.29 (QRen (Ren Qiang (??????)))
OPL/Oceania | 3.03 | 7 | 2.27 (Pabu (Jackson Pavone)) | 4.72 (Imperius (Benny Nguyen))
LCS/North America | 2.75 | 6 | 2.01 (KEITHMCBRIEF (Yuri Jew)) | 4.09 (Anxietylol (Kevin Duque))
LEC/Europe | 3.77 | 10 | 2.69 (Kikis (Mateusz Szkudlarek)) | 6.57 (Cohle (Matteo Faoro))
LMS/Taiwan + Hong Kong + Macao | 3.12 | 7 | 2.32 (SkuLL (Ng Kwok Man (?????????))) | 5.67 (GaryKi (Ng Ka Ki (?????????)))
LST/Southeast Asia | 3.88 | 10 | 2.76 (Coldenfeet (Pongsatorn Kornrat)) | 5.46 (GGamza (Lee Joo-young (?????????)))
LCK/South Korea | 3.16 | 6 | 2.42 (SoHwan (Kim Jun-yeong (?????????))) | 4.52 (Clear (Song Hyeon-min) (Song Hyeon-min (?????????)))
TCL/Turkey | 2.89 | 6 | 2.14 (HolyPhoenix (An??l I????k)) | 4.65 (Lvsyan (Sergi Madrigal G??mez))
PCL/PCS | 3.58 | 8 | 2.68 (Rock (Tsai Chung-Ting) (Tsai Chung-Ting (?????????))) | 4.93 (Lauva (Yuang Hsin-Yu (?????????)))
CBLOL/Brazil | 2.71 | 6 | 1.98 (ziriguidun (Pedro Vilarinho)) | 4.79 (Mayakuza (Andr?? Maia))
VCS/Vietnam | 2.36 | 4 | 1.85 (CombatLao (Nguy???n V?? Th??nh Lu??n)) | 3.19 (Rby (T??? ????nh Huy))
LCL/Russia | 2.89 | 6 | 2.08 (NoNHoly (Aleksandr Ovchinikov)) | 4.57 (PewPewSolari (Olga Arsenyeva))
WORLDS | 5.54 | 14 | 3.69 (Faker (Lee Sang-hyeok (?????????))) | 8.34 (Carzzy (Maty???? Ors??g))
MSI | 3.33 | 7 | 2.3 (Mata (Cho Se-hyeong (?????????))) | 4.22 (ShiauC (Liu Chia-Hao (?????????)))
ALL | 4.39 | 11 | 3.15 (GBM (Lee Chang-seok (?????????))) | 7.27 (Azure (Noel Christopher Cuadra) (Noel Christopher Cuadra))



<img src="https://github.com/simonvw95/LeagueOfLegendsCompetitiveNetwork/blob/main/images/distance_distribution.png" alt="Test" width="512" height="512">


### Node Centrality Measures

Region | Closeness Centrality & Node | Betweenness Centrality & Node |
------------ | ------------- | -------------
LJL/Japan | 0.5 (Paz (Shirou Sasaki (????????? ??????))) | 0.1 (Cogcog (Ryohei Matsuda)) | 
LL/Latin America | 0.47 (Baula (Alejandro Serrano)) | 0.12 (Unforgiven (Maximiliano Utrero) (Maximiliano Utrero)) | 
LPL/China | 0.4 (Amazing (Liu Shi-Yu) (Liu Shi-Yu (?????????))) | 0.03 (y4 (Wang Nong-Mo (?????????))) | 
OPL/Oceania | 0.44 (Pabu (Jackson Pavone)) | 0.05 (Sybol (Lachlan Civil)) | 
LCS/North America | 0.48 (KEITHMCBRIEF (Yuri Jew)) | 0.04 (Cris (Cristian Rosales)) | 
LEC/Europe | 0.35 (Kikis (Mateusz Szkudlarek)) | 0.05 (Werlyb (Jorge Casanovas)) | 
LMS/Taiwan + Hong Kong + Macao | 0.42 (SkuLL (Ng Kwok Man (?????????))) | 0.05 (Lauva (Yuang Hsin-Yu (?????????))) | 
LST/Southeast Asia | 0.19 (Coldenfeet (Pongsatorn Kornrat)) | 0.14 (Coldenfeet (Pongsatorn Kornrat)) | 
LCK/South Korea | 0.4 (SoHwan (Kim Jun-yeong (?????????))) | 0.04 (Smeb (Song Kyung-ho (?????????))) | 
TCL/Turkey | 0.47 (HolyPhoenix (An??l I????k)) | 0.06 (HolyPhoenix (An??l I????k)) | 
PCL/PCS | 0.26 (Rock (Tsai Chung-Ting) (Tsai Chung-Ting (?????????))) | 0.13 (Maoan (Chien Mao-An (?????????))) | 
CBLOL/Brazil | 0.5 (ziriguidun (Pedro Vilarinho)) | 0.05 (Zuao (Jo??o Vitor Morais)) | 
VCS/Vietnam | 0.52 (CombatLao (Nguy???n V?? Th??nh Lu??n)) | 0.05 (CombatLao (Nguy???n V?? Th??nh Lu??n)) | 
LCL/Russia | 0.48 (NoNHoly (Aleksandr Ovchinikov)) | 0.12 (dayruin (Boris Sherbakov)) | 
WORLDS | 0.19 (Faker (Lee Sang-hyeok (?????????))) | 0.09 (Uzi (Jian Zi-Hao) (Jian Zi-Hao (?????????))) | 
MSI | 0.08 (Mata (Cho Se-hyeong (?????????))) | 0.02 (Mata (Cho Se-hyeong (?????????))) | 
All | TBD | TBD |
