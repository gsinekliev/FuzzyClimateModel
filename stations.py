from collections import namedtuple

StationInformation = namedtuple( 'StationInformation', [ 'country', 'city', 'wmoind' ] ) 

# using 6 o'clock time contains all needed data. -> otherwise some miss precipitation and other data

# YYGGi IIiii iihVV Nddff 00fff 1sTTT 2sTTT 3PPPP 4PPPP 5appp 6RRRt 7wwWW 8NCCC 9GGgg
# 222Dv 0sTTT 1PPHH 2PPHH 3dddd 4PPHH 5PPHH 6IEER 70HHH 8aTTT
# 333 0.... 1sTTT 2sTTT 3Ejjj 4Esss 5jjjj jjjjj 6RRRt 7RRRR 8Nchh 9SSss 

# add length of day, classes in which climate they belong and may be bonus data in comments
# verify
#       h   -> Cloud base of lowest cloud seen in meters
#       VV  -> visibility in km
#       N   -> cloud cover in percantage
#       1   -> Tempreture in C
#       2   -> Dew Point in C ( except if sign is 9, TTT is relative humidity )
#       3   -> Station Presure in mb
#       6   -> Liquid Precipitation in mm

STATIONS_INFORMATION = [
    # EUROPE
    StationInformation( "Albania", "Korca", 13629 ),                   # | 40-36N | 020-46E | 889 m
    StationInformation( "Armenia", "Yerevan", 37788 ),                 # | 40-09N | 044-23E | 854 m
    StationInformation( "Austria", "Tulln", 11030 ),                   # | 48-19N | 016-07E | 175 m
    StationInformation( "Belarus", "Kostjvkovici", 26887 ),            # | 53-21N | 032-04E | 164 m
    StationInformation( "Belgium", "Charleroi/Gosselies", 06449 ),     # | 50-28N | 004-27E | 187 m
    StationInformation( "Bosnia and Herzegovina", "Sarajevo", 14654 ), # | 43-52N | 018-26E | 630 m
    StationInformation( "Bulgaria", "Sofia", 15614 ),                  # | 42-39N | 023-23E | 586 m
    StationInformation( "Croatia", "Zagreb", 14240 ),                  # | 45-49N | 016-02E | 123 m
    StationInformation( "Cyprus", "Nicosia", 17521 ),                  # | 35-08N | 033-31E | 110 m
    StationInformation( "Czech Republic", "Praha-Kbely", 11567 ),      # | 50-07N | 014-32E | 286 m
    StationInformation( "Denmark", "Aarslev", 06126 ),                 # | 55-19N | 010-26E | 49 m
    StationInformation( "Estonia", "Tallinn", 26038 ),                 # | 59-23N | 024-35E | 34 m
    StationInformation( "Finland", "Kilpisjarvi", 02801 ),             # | 69-03N | 020-47E | 478 m
    StationInformation( "France", "Paris", 07150 ),                    # | 48-58N | 002-27E | 66 m
    StationInformation( "Georgia", "Tbilisi", 37545 ),                 # | 41-42N | 044-45E | 403 m
    StationInformation( "Germany", "Berlin-Tegel", 10382 ),            # | 52-34N | 013-19E | 37 m
    StationInformation( "Greece", "Athens ", 16741 ),                  # | 37-56N | 023-56E | 72 m
    StationInformation( "Hungary", "Szombathely", 12812 ),             # | 47-16N | 016-38E | 220 m
    StationInformation( "Ireland", "Mullingar", 03971 ),               # | 53-32N | 007-22W | 101 m
    StationInformation( "Italy", "Milano/Malpensa", 16066 ),           # | 45-37N | 008-44E | 234 m
    StationInformation( "Kazakhstan", "Balkasino", 28978 ),            # | 52-32N | 068-45E | 399 m
    StationInformation( "Latvia", "Dobele", 26424 ),                   # | 56-37N | 023-19E | 44 m
    StationInformation( "Liechtenstein", "Vaduz", 06990 ),             # | 47-08N | 009-31E | 460 m
    StationInformation( "Lithuania", "Vilnius", 26730 ),               # | 54-38N | 025-06E | 162 m
    StationInformation( "Malta", "Luqa", 16597 ),                      # | 35-51N | 014-29E | 91 m
    StationInformation( "Montenegro", "Plevlja", 13363 ),              # | 43-21N | 019-21E | 784 m
    StationInformation( "Netherlands", "Amsterdam", 06240 ),           # | 52-18N | 004-46E | -4 m
    StationInformation( "Norway", "Hornsund", 01003 ),                 # | 77-00N | 015-30E | 10 m
    StationInformation( "Poland", "Warszawa-Okecie", 12375 ),          # | 52-10N | 020-58E | 106 m
    StationInformation( "Portugal", "Porto", 08545 ),                  # | 41-14N | 008-41W | 69 m
    StationInformation( "Romania", "Bucharest", 15422 ),               # | 44-25N | 026-05E | 82 m
    StationInformation( "Russia", "Moskva", 27612 ),                   # | 55-50N | 037-37E | 156 m
    StationInformation( "Serbia", "Beograd", 13272 ),                  # | 44-49-28N | 020-17-28E | 96 m
    StationInformation( "Slovakia", "Bratislava", 11813 ),             # | 48-10-00N | 017-07-00E | 288 m
    StationInformation( "Slovenia", "Ljubljana", 14015 ),              # | 46-04N | 014-31E | 299 m
    StationInformation( "Spain", "Madrid", 08221 ),                    # | 40-27N | 003-33W | 609 m
    StationInformation( "Sweden", "Kerstinbo", 02482 ),                # | 60-16N | 016-59E | 56 m
    StationInformation( "Switzerland", "Zurich-Kloten", 06670 ),       # | 47-29N | 008-32E | 436 m
    StationInformation( "Turkey", "Ankara", 17128 ),                   # | 40-07N | 032-59E | 953 m
    StationInformation( "Ukraine", "Mukachevo", 33634 ),               # | 48-26-00N | 022-45-00E | 119 m
    StationInformation( "United Kingdom", "Lerwick", 03005 ),          # | 60-08N | 001-11W | 82 m

    # Skipping, because of not having full info from stations.
    # StationInformation( "Azerbaijan", "Baku", 37851 ),
    # StationInformation( "Iceland", "Reykjavík" ),
    # StationInformation( "Kosovo", "Pristina" ),
    # StationInformation( "Luxembourg", "Luxembourg" ),
    # StationInformation( "Moldova", "Chişinău" ),
    # StationInformation( "Monaco", "Monaco" ),
    # StationInformation( "Republic of Macedonia", "Skopje" ),
    # StationInformation( "San Marino", "San Marino" ),

    # ASIA
    # TODO: add station IDs and set additional Information
    #       from this endpoint http://www.ogimet.com/synopsc.phtml.en
    # StationInformation( "Abkhazia", "Sukhumi" )
    # StationInformation( "Afghanistan", "Kabul" )
    # StationInformation( "Armenia", "Yerevan" )
    # StationInformation( "Azerbaijan", "Baku" )
    # StationInformation( "Bahrain", "Manama" )
    # StationInformation( "Bangladesh", "Dhaka" )
    # StationInformation( "Bhutan", "Thimphu" )
    # StationInformation( "Brunei", "Bandar Seri Begawan" )
    # StationInformation( "Cambodia", "Phnom Penh" )
    # StationInformation( "China", "Beijing" )
    # StationInformation( "Cyprus", "Nicosia" )
    # StationInformation( "East Timor", "Dili" )
    # StationInformation( "Egypt", "Cairo" )
    # StationInformation( "Georgia", "Tbilisi" )
    # StationInformation( "Hong Kong", "Hong Kong" )
    # StationInformation( "India", "New Delhi" )
    # StationInformation( "Indonesia", "Jakarta" )
    # StationInformation( "Iran", "Tehran" )
    # StationInformation( "Iraq", "Baghdad" )
    # StationInformation( "Israel", "Jerusalem" )
    # StationInformation( "Japan", "Tokyo" )
    # StationInformation( "Jordan", "Amman" )
    # StationInformation( "Kazakhstan", "Astana" )
    # StationInformation( "Kuwait", "Kuwait City" )
    # StationInformation( "Kyrgyzstan", "Bishkek" )
    # StationInformation( "Laos", "Vientiane" )
    # StationInformation( "Lebanon", "Beirut" )
    # StationInformation( "Macau", "Macau" )
    # StationInformation( "Malaysia", "Kuala Lumpur" )
    # StationInformation( "Maldives", "Malé" )
    # StationInformation( "Mongolia", "Ulan Bator" )
    # StationInformation( "Myanmar", "Naypyidaw" )
    # StationInformation( "Nagorno-Karabakh", "Stepanakert" )
    # StationInformation( "Nepal", "Kathmandu" )
    # StationInformation( "North Korea", "Pyongyang" )
    # StationInformation( "Northern Cyprus", "North Nicosia" )
    # StationInformation( "Oman", "Muscat" )
    # StationInformation( "Pakistan", "Islamabad" )
    # StationInformation( "Palestine", "E. Jerusalem" )
    # StationInformation( "Papua New Guinea", "Port Moresby" )
    # StationInformation( "Philippines", "Manila" )
    # StationInformation( "Qatar", "Doha" )
    # StationInformation( "Russia", "Moscow" )
    # StationInformation( "Saudi Arabia", "Riyadh" )
    # StationInformation( "Singapore", "Singapore" )
    # StationInformation( "South Korea", "Seoul" )
    # StationInformation( "South Ossetia", "Tskhinvali" )
    # StationInformation( "Sri Lanka", "Sri Jayawardenepura Kotte" )
    # StationInformation( "Syria", "Damascus" )
    # StationInformation( "Taiwan", "Taipei" )
    # StationInformation( "Tajikistan", "Dushanbe" )
    # StationInformation( "Thailand", "Bangkok" )
    # StationInformation( "Turkey", "Ankara" )
    # StationInformation( "Turkmenistan", "Ashgabat" )
    # StationInformation( "United Arab Emirates", "Abu Dhabi" )
    # StationInformation( "Uzbekistan", "Tashkent" )
    # StationInformation( "Vietnam", "Hanoi" )
    # StationInformation( "Yemen", "Sana'a", 41404 )

    # TODO: add stations for north america to have atleast 100 stations
]