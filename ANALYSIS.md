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

Region | Nodes | Edges | Density | Days Active
------------ | ------------- | ------------- | ------------- | -------------
LJL/Japan |211 | 1155 | 0.0521 | 2259
LL/Latin America |138 | 643 | 0.0680 | 803
LPL/China |1073 | 8109 | 0.0141 | 2984
OPL/Oceania |382 | 2223 | 0.0305 | 2032
LCS/North America |568 | 4642 | 0.0288 | 2975
LEC/Europe |805 | 4614 | 0.0143 | 2973
LMS/Taiwan + Hong Kong + Macao |394 | 2628 | 0.0339 | 1718
LST/Southeast Asia |78 | 209 | 0.0696 | 399
LCK/South Korea |649 | 4397 | 0.0209 | 2829
TCL/Turkey |586 | 4160 | 0.0243 | 2259
PCL/PCS |126 | 474 | 0.0602 | 397
CBLOL/Brazil |406 | 3670 | 0.0446 | 2532
VCS/Vietnam |182 | 1441 | 0.0875 | 1706
LCL/Russia |198 | 1010 | 0.0518 | 1902
WORLDS |608 | 2146 | 0.0116 | NA
MSI |251 | 757 | 0.0241 | NA
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
Not factoring in weights, applied to the largest connected component.

Region | Average Distance | Diameter (Longest Distance) | Shortest Average Distance & Node | Longest Average Distance & Node
------------ | ------------- | ------------- | ------------- | -------------
LJL_Japan | 2.67 | 5 | 1.93 (Paz (Shirou Sasaki (佐々木 志郎))) | 3.45 (Dicey (Daisuke Ashida))
LL_Latin America | 2.78 | 5 | 2.01 (Baula (Alejandro Serrano)) | 3.5 (Jirall (Daniel del Castillo))
LPL_China | 3.27 | 8 | 2.47 (Amazing (Liu Shi-Yu) (Liu Shi-Yu (刘时雨))) | 5.29 (QRen (Ren Qiang (任强)))
OPL_Oceania | 3.03 | 7 | 2.27 (Pabu (Jackson Pavone)) | 4.72 (Imperius (Benny Nguyen))
LCS_North America | 2.75 | 6 | 2.01 (KEITHMCBRIEF (Yuri Jew)) | 4.09 (Anxietylol (Kevin Duque))
LEC_Europe | 3.77 | 10 | 2.69 (Kikis (Mateusz Szkudlarek)) | 6.57 (Cohle (Matteo Faoro))
LMS_Taiwan + Hong Kong + Macao | 3.09 | 7 | 2.32 (SkuLL (Ng Kwok Man (吳國玟))) | 5.62 (GaryKi (Ng Ka Ki (吳嘉奇)))
LST_Southeast Asia | 3.88 | 10 | 2.76 (Coldenfeet (Pongsatorn Kornrat)) | 5.46 (GGamza (Lee Joo-young (이주영)))
LCK_South Korea | 3.16 | 6 | 2.42 (SoHwan (Kim Jun-yeong (김준영))) | 4.52 (Clear (Song Hyeon-min) (Song Hyeon-min (송현민)))
TCL_Turkey | 2.89 | 6 | 2.14 (HolyPhoenix (Anıl Işık)) | 4.65 (Lvsyan (Sergi Madrigal Gómez))
PCL_PCS | 3.58 | 8 | 2.68 (Rock (Tsai Chung-Ting) (Tsai Chung-Ting (蔡忠廷))) | 4.93 (Lauva (Yuang Hsin-Yu (黃新宇)))
CBLOL_Brazil | 2.71 | 6 | 1.98 (ziriguidun (Pedro Vilarinho)) | 4.79 (Mayakuza (André Maia))
VCS_Vietnam | 2.38 | 5 | 1.85 (Zin (Nguyễn Tuấn Thọ)) | 3.24 (Rby (Tạ Đình Huy))
LCL_Russia | 2.89 | 6 | 2.08 (NoNHoly (Aleksandr Ovchinikov)) | 4.57 (PewPewSolari (Olga Arsenyeva))
WORLDS | 5.54 | 14 | 3.69 (Faker (Lee Sang-hyeok (이상혁))) | 8.34 (Carzzy (Matyáš Orság))
MSI | 3.33 | 7 | 2.3 (Mata (Cho Se-hyeong (조세형))) | 4.22 (ShiauC (Liu Chia-Hao (劉家豪)))
ALL | 4.39 | 11 | 3.15 (GBM (Lee Chang-seok (이창석))) | 7.27 (Azure (Noel Christopher Cuadra) (Noel Christopher Cuadra))


### Clustering coefficient

### Triangles
