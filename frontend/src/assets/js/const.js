const svg_lust = 'M353.6 304.6c-25.9 8.3-64.4 13.1-105.6 13.1s-79.6-4.8-105.6-13.1c-9.8-3.1-19.4 5.3-17.7 15.3 7.9 47.2 71.3 80 123.3 80s115.3-32.9 123.3-80c1.6-9.8-7.7-18.4-17.7-15.3zm-152.8-48.9c4.5 1.2 9.2-1.5 10.5-6l19.4-69.9c5.6-20.3-7.4-41.1-28.8-44.5-18.6-3-36.4 9.8-41.5 27.9l-2 7.1-7.1-1.9c-18.2-4.7-38.2 4.3-44.9 22-7.7 20.2 3.8 41.9 24.2 47.2l70.2 18.1zm188.8-65.3c-6.7-17.6-26.7-26.7-44.9-22l-7.1 1.9-2-7.1c-5-18.1-22.8-30.9-41.5-27.9-21.4 3.4-34.4 24.2-28.8 44.5l19.4 69.9c1.2 4.5 5.9 7.2 10.5 6l70.2-18.2c20.4-5.3 31.9-26.9 24.2-47.1zM248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200z'
const svg_gluttony = 'M464 256H48a48 48 0 0 0 0 96h416a48 48 0 0 0 0-96zm16 128H32a16 16 0 0 0-16 16v16a64 64 0 0 0 64 64h352a64 64 0 0 0 64-64v-16a16 16 0 0 0-16-16zM58.64 224h394.72c34.57 0 54.62-43.9 34.82-75.88C448 83.2 359.55 32.1 256 32c-103.54.1-192 51.2-232.18 116.11C4 180.09 24.07 224 58.64 224zM384 112a16 16 0 1 1-16 16 16 16 0 0 1 16-16zM256 80a16 16 0 1 1-16 16 16 16 0 0 1 16-16zm-128 32a16 16 0 1 1-16 16 16 16 0 0 1 16-16z'
const svg_warth = 'M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200zm0-144c-33.6 0-65.2 14.8-86.8 40.6-8.5 10.2-7.1 25.3 3.1 33.8s25.3 7.2 33.8-3c24.8-29.7 75-29.7 99.8 0 8.1 9.7 23.2 11.9 33.8 3 10.2-8.5 11.5-23.6 3.1-33.8-21.6-25.8-53.2-40.6-86.8-40.6zm-48-72c10.3 0 19.9-6.7 23-17.1 3.8-12.7-3.4-26.1-16.1-29.9l-80-24c-12.8-3.9-26.1 3.4-29.9 16.1-3.8 12.7 3.4 26.1 16.1 29.9l28.2 8.5c-3.1 4.9-5.3 10.4-5.3 16.6 0 17.7 14.3 32 32 32s32-14.4 32-32.1zm199-54.9c-3.8-12.7-17.1-19.9-29.9-16.1l-80 24c-12.7 3.8-19.9 17.2-16.1 29.9 3.1 10.4 12.7 17.1 23 17.1 0 17.7 14.3 32 32 32s32-14.3 32-32c0-6.2-2.2-11.7-5.3-16.6l28.2-8.5c12.7-3.7 19.9-17.1 16.1-29.8z'
const svg_positive = 'M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm141.4 389.4c-37.8 37.8-88 58.6-141.4 58.6s-103.6-20.8-141.4-58.6S48 309.4 48 256s20.8-103.6 58.6-141.4S194.6 56 248 56s103.6 20.8 141.4 58.6S448 202.6 448 256s-20.8 103.6-58.6 141.4zM343.6 196l33.6-40.3c8.6-10.3-3.8-24.8-15.4-18l-80 48c-7.8 4.7-7.8 15.9 0 20.6l80 48c11.5 6.8 24-7.6 15.4-18L343.6 196zm-209.4 58.3l80-48c7.8-4.7 7.8-15.9 0-20.6l-80-48c-11.6-6.9-24 7.7-15.4 18l33.6 40.3-33.6 40.3c-8.7 10.4 3.8 24.8 15.4 18zM362.4 288H133.6c-8.2 0-14.5 7-13.5 15 7.5 59.2 58.9 105 121.1 105h13.6c62.2 0 113.6-45.8 121.1-105 1-8-5.3-15-13.5-15z'
const svg_negative = 'M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200zm-80-216c17.7 0 32-14.3 32-32s-14.3-32-32-32-32 14.3-32 32 14.3 32 32 32zm160-64c-17.7 0-32 14.3-32 32s14.3 32 32 32 32-14.3 32-32-14.3-32-32-32zm-80 128c-40.2 0-78 17.7-103.8 48.6-8.5 10.2-7.1 25.3 3.1 33.8 10.2 8.4 25.3 7.1 33.8-3.1 16.6-19.9 41-31.4 66.9-31.4s50.3 11.4 66.9 31.4c8.1 9.7 23.1 11.9 33.8 3.1 10.2-8.5 11.5-23.6 3.1-33.8C326 321.7 288.2 304 248 304z'
const svg_neutral = 'M200.3 248c12.4-18.7 15.1-37.3 15.7-56-.5-18.7-3.3-37.3-15.7-56-8-12-25.1-11.4-32.7 0-12.4 18.7-15.1 37.3-15.7 56 .5 18.7 3.3 37.3 15.7 56 8.1 12 25.2 11.4 32.7 0zm128 0c12.4-18.7 15.1-37.3 15.7-56-.5-18.7-3.3-37.3-15.7-56-8-12-25.1-11.4-32.7 0-12.4 18.7-15.1 37.3-15.7 56 .5 18.7 3.3 37.3 15.7 56 8.1 12 25.2 11.4 32.7 0zM248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm0 448c-110.3 0-200-89.7-200-200S137.7 56 248 56s200 89.7 200 200-89.7 200-200 200zm105.6-151.4c-25.9 8.3-64.4 13.1-105.6 13.1s-79.6-4.8-105.6-13.1c-9.9-3.1-19.4 5.3-17.7 15.3 7.9 47.2 71.3 80 123.3 80s115.3-32.9 123.3-80c1.6-9.8-7.7-18.4-17.7-15.3z'
const aurin = {
    "ALPINE": {
      "econ": {
        "unemployment_num": 216,
        "total_people_hospital": 5241,
        "total_male_hospital": 2625,
        "total_female_hospital": 2614
      },
      "offence": {
        "weapons related": 178,
        "assaults": 210,
        "sexual offences": 127,
        "robbery": 0,
        "harassment and threatening": 51,
        "total": 2244
      }
    },
    "ARARAT": {
      "econ": {
        "unemployment_num": 257,
        "total_people_hospital": 6574,
        "total_male_hospital": 3106,
        "total_female_hospital": 3468
      },
      "offence": {
        "weapons related": 208,
        "assaults": 819,
        "sexual offences": 208,
        "robbery": 4,
        "harassment and threatening": 159,
        "total": 6082
      }
    },
    "BALLARAT": {
      "econ": {
        "unemployment_num": 3415,
        "total_people_hospital": 36640,
        "total_male_hospital": 16450,
        "total_female_hospital": 20189
      },
      "offence": {
        "weapons related": 1603,
        "assaults": 4442,
        "sexual offences": 2239,
        "robbery": 167,
        "harassment and threatening": 801,
        "total": 54948
      }
    },
    "BANYULE": {
      "econ": {
        "unemployment_num": 3429,
        "total_people_hospital": 50143,
        "total_male_hospital": 22452,
        "total_female_hospital": 27689
      },
      "offence": {
        "weapons related": 963,
        "assaults": 3234,
        "sexual offences": 1126,
        "robbery": 195,
        "harassment and threatening": 1184,
        "total": 46688
      }
    },
    "BASS COAST": {
      "econ": {
        "unemployment_num": 857,
        "total_people_hospital": 11011,
        "total_male_hospital": 5422,
        "total_female_hospital": 5589
      },
      "offence": {
        "weapons related": 396,
        "assaults": 1541,
        "sexual offences": 612,
        "robbery": 23,
        "harassment and threatening": 547,
        "total": 13372
      }
    },
    "BAW BAW": {
      "econ": {
        "unemployment_num": 1235,
        "total_people_hospital": 13343,
        "total_male_hospital": 6410,
        "total_female_hospital": 6933
      },
      "offence": {
        "weapons related": 773,
        "assaults": 1666,
        "sexual offences": 867,
        "robbery": 39,
        "harassment and threatening": 741,
        "total": 18412
      }
    },
    "BAYSIDE": {
      "econ": {
        "unemployment_num": 2215,
        "total_people_hospital": 43828,
        "total_male_hospital": 19936,
        "total_female_hospital": 23890
      },
      "offence": {
        "weapons related": 559,
        "assaults": 1380,
        "sexual offences": 765,
        "robbery": 127,
        "harassment and threatening": 470,
        "total": 22983
      }
    },
    "BENALLA": {
      "econ": {
        "unemployment_num": 319,
        "total_people_hospital": 5999,
        "total_male_hospital": 2910,
        "total_female_hospital": 3089
      },
      "offence": {
        "weapons related": 213,
        "assaults": 857,
        "sexual offences": 359,
        "robbery": 10,
        "harassment and threatening": 185,
        "total": 6167
      }
    },
    "BOROONDARA": {
      "econ": {
        "unemployment_num": 4837,
        "total_people_hospital": 61843,
        "total_male_hospital": 27879,
        "total_female_hospital": 33962
      },
      "offence": {
        "weapons related": 532,
        "assaults": 1853,
        "sexual offences": 793,
        "robbery": 183,
        "harassment and threatening": 688,
        "total": 37170
      }
    },
    "BRIMBANK": {
      "econ": {
        "unemployment_num": 9257,
        "total_people_hospital": 71961,
        "total_male_hospital": 32697,
        "total_female_hospital": 39264
      },
      "offence": {
        "weapons related": 3434,
        "assaults": 7165,
        "sexual offences": 1451,
        "robbery": 1146,
        "harassment and threatening": 1807,
        "total": 92393
      }
    },
    "BULOKE": {
      "econ": {
        "unemployment_num": 113,
        "total_people_hospital": 3636,
        "total_male_hospital": 1803,
        "total_female_hospital": 1832
      },
      "offence": {
        "weapons related": 40,
        "assaults": 121,
        "sexual offences": 90,
        "robbery": 0,
        "harassment and threatening": 35,
        "total": 1116
      }
    },
    "CAMPASPE": {
      "econ": {
        "unemployment_num": 824,
        "total_people_hospital": 22417,
        "total_male_hospital": 10780,
        "total_female_hospital": 11638
      },
      "offence": {
        "weapons related": 493,
        "assaults": 1447,
        "sexual offences": 698,
        "robbery": 32,
        "harassment and threatening": 358,
        "total": 15743
      }
    },
    "CARDINIA": {
      "econ": {
        "unemployment_num": 2601,
        "total_people_hospital": 32741,
        "total_male_hospital": 15194,
        "total_female_hospital": 17546
      },
      "offence": {
        "weapons related": 1120,
        "assaults": 2774,
        "sexual offences": 872,
        "robbery": 117,
        "harassment and threatening": 1086,
        "total": 32107
      }
    },
    "CASEY": {
      "econ": {
        "unemployment_num": 10663,
        "total_people_hospital": 113855,
        "total_male_hospital": 49237,
        "total_female_hospital": 64617
      },
      "offence": {
        "weapons related": 3037,
        "assaults": 9934,
        "sexual offences": 2801,
        "robbery": 646,
        "harassment and threatening": 3022,
        "total": 98799
      }
    },
    "CENTRAL GOLDFIELDS": {
      "econ": {
        "unemployment_num": 423,
        "total_people_hospital": 4902,
        "total_male_hospital": 2354,
        "total_female_hospital": 2549
      },
      "offence": {
        "weapons related": 291,
        "assaults": 682,
        "sexual offences": 286,
        "robbery": 12,
        "harassment and threatening": 207,
        "total": 6061
      }
    },
    "COLAC OTWAY": {
      "econ": {
        "unemployment_num": 398,
        "total_people_hospital": 9865,
        "total_male_hospital": 4411,
        "total_female_hospital": 5454
      },
      "offence": {
        "weapons related": 306,
        "assaults": 923,
        "sexual offences": 344,
        "robbery": 17,
        "harassment and threatening": 314,
        "total": 8262
      }
    },
    "CORANGAMITE": {
      "econ": {
        "unemployment_num": 296,
        "total_people_hospital": 8193,
        "total_male_hospital": 3835,
        "total_female_hospital": 4357
      },
      "offence": {
        "weapons related": 164,
        "assaults": 386,
        "sexual offences": 267,
        "robbery": 7,
        "harassment and threatening": 114,
        "total": 3828
      }
    },
    "DAREBIN": {
      "econ": {
        "unemployment_num": 5435,
        "total_people_hospital": 53081,
        "total_male_hospital": 23170,
        "total_female_hospital": 29911
      },
      "offence": {
        "weapons related": 1666,
        "assaults": 4337,
        "sexual offences": 1242,
        "robbery": 520,
        "harassment and threatening": 1420,
        "total": 72855
      }
    },
    "EAST GIPPSLAND": {
      "econ": {
        "unemployment_num": 1153,
        "total_people_hospital": 17234,
        "total_male_hospital": 8419,
        "total_female_hospital": 8815
      },
      "offence": {
        "weapons related": 796,
        "assaults": 2774,
        "sexual offences": 494,
        "robbery": 42,
        "harassment and threatening": 636,
        "total": 20032
      }
    },
    "FRANKSTON": {
      "econ": {
        "unemployment_num": 4365,
        "total_people_hospital": 75705,
        "total_male_hospital": 33583,
        "total_female_hospital": 42121
      },
      "offence": {
        "weapons related": 3523,
        "assaults": 5796,
        "sexual offences": 1745,
        "robbery": 425,
        "harassment and threatening": 1488,
        "total": 75380
      }
    },
    "GANNAWARRA": {
      "econ": {
        "unemployment_num": 220,
        "total_people_hospital": 6189,
        "total_male_hospital": 3069,
        "total_female_hospital": 3119
      },
      "offence": {
        "weapons related": 123,
        "assaults": 356,
        "sexual offences": 96,
        "robbery": 4,
        "harassment and threatening": 85,
        "total": 2860
      }
    },
    "GREATER SHEPPARTON": {
      "econ": {
        "unemployment_num": 1857,
        "total_people_hospital": 34431,
        "total_male_hospital": 15982,
        "total_female_hospital": 18449
      },
      "offence": {
        "weapons related": 1440,
        "assaults": 3568,
        "sexual offences": 1051,
        "robbery": 88,
        "harassment and threatening": 946,
        "total": 37085
      }
    },
    "HEPBURN": {
      "econ": {
        "unemployment_num": 345,
        "total_people_hospital": 5508,
        "total_male_hospital": 2641,
        "total_female_hospital": 2867
      },
      "offence": {
        "weapons related": 52,
        "assaults": 348,
        "sexual offences": 144,
        "robbery": 8,
        "harassment and threatening": 103,
        "total": 3750
      }
    },
    "HINDMARSH": {
      "econ": {
        "unemployment_num": 124,
        "total_people_hospital": 4006,
        "total_male_hospital": 2052,
        "total_female_hospital": 1954
      },
      "offence": {
        "weapons related": 52,
        "assaults": 189,
        "sexual offences": 80,
        "robbery": 1,
        "harassment and threatening": 75,
        "total": 1421
      }
    },
    "HOBSONS BAY": {
      "econ": {
        "unemployment_num": 2931,
        "total_people_hospital": 38206,
        "total_male_hospital": 17253,
        "total_female_hospital": 20953
      },
      "offence": {
        "weapons related": 1003,
        "assaults": 2670,
        "sexual offences": 589,
        "robbery": 214,
        "harassment and threatening": 798,
        "total": 33641
      }
    },
    "HORSHAM": {
      "econ": {
        "unemployment_num": 468,
        "total_people_hospital": 10018,
        "total_male_hospital": 4694,
        "total_female_hospital": 5324
      },
      "offence": {
        "weapons related": 328,
        "assaults": 1499,
        "sexual offences": 345,
        "robbery": 13,
        "harassment and threatening": 417,
        "total": 13054
      }
    },
    "HUME": {
      "econ": {
        "unemployment_num": 7756,
        "total_people_hospital": 84241,
        "total_male_hospital": 37378,
        "total_female_hospital": 46863
      },
      "offence": {
        "weapons related": 3491,
        "assaults": 7805,
        "sexual offences": 1976,
        "robbery": 476,
        "harassment and threatening": 2857,
        "total": 96188
      }
    },
    "INDIGO": {
      "econ": {
        "unemployment_num": 333,
        "total_people_hospital": 6531,
        "total_male_hospital": 3271,
        "total_female_hospital": 3260
      },
      "offence": {
        "weapons related": 127,
        "assaults": 222,
        "sexual offences": 156,
        "robbery": 8,
        "harassment and threatening": 77,
        "total": 2349
      }
    },
    "KINGSTON": {
      "econ": {
        "unemployment_num": 4247,
        "total_people_hospital": 65869,
        "total_male_hospital": 29221,
        "total_female_hospital": 36647
      },
      "offence": {}
    },
    "KNOX": {
      "econ": {
        "unemployment_num": 4584,
        "total_people_hospital": 61635,
        "total_male_hospital": 27974,
        "total_female_hospital": 33660
      },
      "offence": {
        "weapons related": 1639,
        "assaults": 3874,
        "sexual offences": 1484,
        "robbery": 279,
        "harassment and threatening": 941,
        "total": 52014
      }
    },
    "LATROBE": {
      "econ": {
        "unemployment_num": 3157,
        "total_people_hospital": 30198,
        "total_male_hospital": 13725,
        "total_female_hospital": 16472
      },
      "offence": {}
    },
    "LODDON": {
      "econ": {
        "unemployment_num": 158,
        "total_people_hospital": 3072,
        "total_male_hospital": 1522,
        "total_female_hospital": 1550
      },
      "offence": {
        "weapons related": 58,
        "assaults": 234,
        "sexual offences": 124,
        "robbery": 1,
        "harassment and threatening": 77,
        "total": 2147
      }
    },
    "MACEDON RANGES": {
      "econ": {
        "unemployment_num": 1002,
        "total_people_hospital": 15560,
        "total_male_hospital": 7938,
        "total_female_hospital": 7622
      },
      "offence": {
        "weapons related": 392,
        "assaults": 1370,
        "sexual offences": 339,
        "robbery": 17,
        "harassment and threatening": 411,
        "total": 11246
      }
    },
    "MANNINGHAM": {
      "econ": {
        "unemployment_num": 3452,
        "total_people_hospital": 48734,
        "total_male_hospital": 22416,
        "total_female_hospital": 26316
      },
      "offence": {
        "weapons related": 394,
        "assaults": 1602,
        "sexual offences": 496,
        "robbery": 101,
        "harassment and threatening": 797,
        "total": 22100
      }
    },
    "MANSFIELD": {
      "econ": {
        "unemployment_num": 132,
        "total_people_hospital": 2466,
        "total_male_hospital": 1353,
        "total_female_hospital": 1113
      },
      "offence": {
        "weapons related": 164,
        "assaults": 193,
        "sexual offences": 93,
        "robbery": 3,
        "harassment and threatening": 84,
        "total": 2591
      }
    },
    "MARIBYRNONG": {
      "econ": {
        "unemployment_num": 3760,
        "total_people_hospital": 36527,
        "total_male_hospital": 15915,
        "total_female_hospital": 20611
      },
      "offence": {
        "weapons related": 1249,
        "assaults": 2726,
        "sexual offences": 612,
        "robbery": 520,
        "harassment and threatening": 604,
        "total": 42601
      }
    },
    "MAROONDAH": {
      "econ": {
        "unemployment_num": 3025,
        "total_people_hospital": 48679,
        "total_male_hospital": 21499,
        "total_female_hospital": 27180
      },
      "offence": {
        "weapons related": 1137,
        "assaults": 3147,
        "sexual offences": 870,
        "robbery": 200,
        "harassment and threatening": 863,
        "total": 39404
      }
    },
    "MELBOURNE": {
      "econ": {
        "unemployment_num": 8006,
        "total_people_hospital": 25827,
        "total_male_hospital": 11245,
        "total_female_hospital": 14580
      },
      "offence": {
        "weapons related": 3814,
        "assaults": 12438,
        "sexual offences": 2594,
        "robbery": 1558,
        "harassment and threatening": 2879,
        "total": 175136
      }
    },
    "MELTON": {
      "econ": {
        "unemployment_num": 4943,
        "total_people_hospital": 52289,
        "total_male_hospital": 21807,
        "total_female_hospital": 30482
      },
      "offence": {}
    },
    "MILDURA": {
      "econ": {
        "unemployment_num": 1784,
        "total_people_hospital": 26186,
        "total_male_hospital": 12506,
        "total_female_hospital": 13679
      },
      "offence": {
        "weapons related": 1171,
        "assaults": 3202,
        "sexual offences": 604,
        "robbery": 80,
        "harassment and threatening": 719,
        "total": 30442
      }
    },
    "MITCHELL": {
      "econ": {
        "unemployment_num": 1112,
        "total_people_hospital": 14156,
        "total_male_hospital": 6756,
        "total_female_hospital": 7400
      },
      "offence": {
        "weapons related": 746,
        "assaults": 2139,
        "sexual offences": 605,
        "robbery": 28,
        "harassment and threatening": 892,
        "total": 18980
      }
    },
    "MOIRA": {
      "econ": {
        "unemployment_num": 629,
        "total_people_hospital": 16386,
        "total_male_hospital": 7655,
        "total_female_hospital": 8731
      },
      "offence": {
        "weapons related": 297,
        "assaults": 789,
        "sexual offences": 585,
        "robbery": 11,
        "harassment and threatening": 205,
        "total": 8138
      }
    },
    "MONASH": {
      "econ": {
        "unemployment_num": 6956,
        "total_people_hospital": 94946,
        "total_male_hospital": 41814,
        "total_female_hospital": 53128
      },
      "offence": {
        "weapons related": 1008,
        "assaults": 3175,
        "sexual offences": 1152,
        "robbery": 492,
        "harassment and threatening": 950,
        "total": 50972
      }
    },
    "MOONEE VALLEY": {
      "econ": {
        "unemployment_num": 3462,
        "total_people_hospital": 43199,
        "total_male_hospital": 20094,
        "total_female_hospital": 23104
      },
      "offence": {
        "weapons related": 1011,
        "assaults": 3042,
        "sexual offences": 701,
        "robbery": 359,
        "harassment and threatening": 1132,
        "total": 43912
      }
    },
    "MOORABOOL": {
      "econ": {
        "unemployment_num": 895,
        "total_people_hospital": 12288,
        "total_male_hospital": 5605,
        "total_female_hospital": 6683
      },
      "offence": {
        "weapons related": 372,
        "assaults": 895,
        "sexual offences": 391,
        "robbery": 17,
        "harassment and threatening": 257,
        "total": 10564
      }
    },
    "MORELAND": {
      "econ": {
        "unemployment_num": 5915,
        "total_people_hospital": 60310,
        "total_male_hospital": 26663,
        "total_female_hospital": 33641
      },
      "offence": {
        "weapons related": 1389,
        "assaults": 4712,
        "sexual offences": 1177,
        "robbery": 395,
        "harassment and threatening": 1344,
        "total": 66045
      }
    },
    "MORNINGTON PENINSULA": {
      "econ": {
        "unemployment_num": 3487,
        "total_people_hospital": 102806,
        "total_male_hospital": 47957,
        "total_female_hospital": 54820
      },
      "offence": {
        "weapons related": 1467,
        "assaults": 4294,
        "sexual offences": 1292,
        "robbery": 150,
        "harassment and threatening": 1349,
        "total": 53663
      }
    },
    "MOUNT ALEXANDER": {
      "econ": {
        "unemployment_num": 431,
        "total_people_hospital": 6708,
        "total_male_hospital": 3302,
        "total_female_hospital": 3406
      },
      "offence": {
        "weapons related": 205,
        "assaults": 428,
        "sexual offences": 157,
        "robbery": 22,
        "harassment and threatening": 155,
        "total": 5459
      }
    },
    "MOYNE": {
      "econ": {
        "unemployment_num": 299,
        "total_people_hospital": 7178,
        "total_male_hospital": 3406,
        "total_female_hospital": 3772
      },
      "offence": {
        "weapons related": 121,
        "assaults": 373,
        "sexual offences": 233,
        "robbery": 3,
        "harassment and threatening": 102,
        "total": 3026
      }
    },
    "MURRINDINDI": {
      "econ": {
        "unemployment_num": 318,
        "total_people_hospital": 4768,
        "total_male_hospital": 2417,
        "total_female_hospital": 2350
      },
      "offence": {
        "weapons related": 181,
        "assaults": 356,
        "sexual offences": 225,
        "robbery": 2,
        "harassment and threatening": 126,
        "total": 3425
      }
    },
    "NILLUMBIK": {
      "econ": {
        "unemployment_num": 1457,
        "total_people_hospital": 25151,
        "total_male_hospital": 11648,
        "total_female_hospital": 13502
      },
      "offence": {
        "weapons related": 222,
        "assaults": 899,
        "sexual offences": 361,
        "robbery": 35,
        "harassment and threatening": 312,
        "total": 12710
      }
    },
    "NORTHERN GRAMPIANS": {
      "econ": {
        "unemployment_num": 266,
        "total_people_hospital": 6578,
        "total_male_hospital": 3045,
        "total_female_hospital": 3533
      },
      "offence": {
        "weapons related": 227,
        "assaults": 683,
        "sexual offences": 246,
        "robbery": 5,
        "harassment and threatening": 316,
        "total": 6475
      }
    },
    "PORT PHILLIP": {
      "econ": {
        "unemployment_num": 3075,
        "total_people_hospital": 35073,
        "total_male_hospital": 15964,
        "total_female_hospital": 19108
      },
      "offence": {
        "weapons related": 1360,
        "assaults": 4292,
        "sexual offences": 1042,
        "robbery": 409,
        "harassment and threatening": 966,
        "total": 61471
      }
    },
    "PYRENEES": {
      "econ": {
        "unemployment_num": 176,
        "total_people_hospital": 2753,
        "total_male_hospital": 1371,
        "total_female_hospital": 1382
      },
      "offence": {
        "weapons related": 71,
        "assaults": 205,
        "sexual offences": 143,
        "robbery": 2,
        "harassment and threatening": 60,
        "total": 2426
      }
    },
    "QUEENSCLIFFE": {
      "econ": {
        "unemployment_num": 34,
        "total_people_hospital": 1144,
        "total_male_hospital": 513,
        "total_female_hospital": 631
      },
      "offence": {
        "weapons related": 8,
        "assaults": 23,
        "sexual offences": 16,
        "robbery": 0,
        "harassment and threatening": 4,
        "total": 663
      }
    },
    "SOUTH GIPPSLAND": {
      "econ": {
        "unemployment_num": 626,
        "total_people_hospital": 9080,
        "total_male_hospital": 4422,
        "total_female_hospital": 4658
      },
      "offence": {
        "weapons related": 198,
        "assaults": 671,
        "sexual offences": 384,
        "robbery": 6,
        "harassment and threatening": 290,
        "total": 6750
      }
    },
    "SOUTHERN GRAMPIANS": {
      "econ": {
        "unemployment_num": 335,
        "total_people_hospital": 7872,
        "total_male_hospital": 3566,
        "total_female_hospital": 4305
      },
      "offence": {
        "weapons related": 190,
        "assaults": 564,
        "sexual offences": 299,
        "robbery": 5,
        "harassment and threatening": 159,
        "total": 5755
      }
    },
    "STONNINGTON": {
      "econ": {
        "unemployment_num": 3112,
        "total_people_hospital": 43220,
        "total_male_hospital": 19048,
        "total_female_hospital": 24172
      },
      "offence": {
        "weapons related": 935,
        "assaults": 2775,
        "sexual offences": 831,
        "robbery": 274,
        "harassment and threatening": 615,
        "total": 50338
      }
    },
    "GOLDEN PLAINS": {
      "econ": {
        "unemployment_num": 501,
        "total_people_hospital": 6500,
        "total_male_hospital": 3177,
        "total_female_hospital": 3323
      },
      "offence": {
        "weapons related": 75,
        "assaults": 268,
        "sexual offences": 145,
        "robbery": 1,
        "harassment and threatening": 60,
        "total": 3257
      }
    },
    "GLEN EIRA": {
      "econ": {
        "unemployment_num": 4278,
        "total_people_hospital": 60499,
        "total_male_hospital": 26292,
        "total_female_hospital": 34207
      },
      "offence": {
        "weapons related": 689,
        "assaults": 2128,
        "sexual offences": 817,
        "robbery": 211,
        "harassment and threatening": 595,
        "total": 31873
      }
    },
    "GREATER BENDIGO": {
      "econ": {
        "unemployment_num": 3328,
        "total_people_hospital": 38339,
        "total_male_hospital": 17940,
        "total_female_hospital": 20399
      },
      "offence": {
        "weapons related": 1426,
        "assaults": 3924,
        "sexual offences": 1486,
        "robbery": 116,
        "harassment and threatening": 1248,
        "total": 45863
      }
    },
    "GREATER DANDENONG": {
      "econ": {
        "unemployment_num": 6897,
        "total_people_hospital": 74984,
        "total_male_hospital": 33077,
        "total_female_hospital": 41902
      },
      "offence": {
        "weapons related": 3456,
        "assaults": 8160,
        "sexual offences": 1868,
        "robbery": 808,
        "harassment and threatening": 2186,
        "total": 89968
      }
    },
    "GREATER GEELONG": {
      "econ": {
        "unemployment_num": 7057,
        "total_people_hospital": 87405,
        "total_male_hospital": 40561,
        "total_female_hospital": 46839
      },
      "offence": {
        "weapons related": 2855,
        "assaults": 7162,
        "sexual offences": 2363,
        "robbery": 385,
        "harassment and threatening": 1876,
        "total": 100487
      }
    },
    "GLENELG": {
      "econ": {
        "unemployment_num": 526,
        "total_people_hospital": 9093,
        "total_male_hospital": 4399,
        "total_female_hospital": 4695
      },
      "offence": {
        "weapons related": 284,
        "assaults": 798,
        "sexual offences": 363,
        "robbery": 11,
        "harassment and threatening": 140,
        "total": 8050
      }
    },
    "STRATHBOGIE": {
      "econ": {
        "unemployment_num": 210,
        "total_people_hospital": 4306,
        "total_male_hospital": 2202,
        "total_female_hospital": 2104
      },
      "offence": {
        "weapons related": 91,
        "assaults": 247,
        "sexual offences": 174,
        "robbery": 2,
        "harassment and threatening": 120,
        "total": 2764
      }
    },
    "SURF COAST": {
      "econ": {
        "unemployment_num": 558,
        "total_people_hospital": 9150,
        "total_male_hospital": 4478,
        "total_female_hospital": 4672
      },
      "offence": {
        "weapons related": 90,
        "assaults": 404,
        "sexual offences": 214,
        "robbery": 17,
        "harassment and threatening": 155,
        "total": 6655
      }
    },
    "SWAN HILL": {
      "econ": {
        "unemployment_num": 462,
        "total_people_hospital": 11012,
        "total_male_hospital": 5169,
        "total_female_hospital": 5842
      },
      "offence": {
        "weapons related": 540,
        "assaults": 1387,
        "sexual offences": 253,
        "robbery": 19,
        "harassment and threatening": 318,
        "total": 10642
      }
    },
    "TOWONG": {
      "econ": {
        "unemployment_num": 129,
        "total_people_hospital": 2479,
        "total_male_hospital": 1290,
        "total_female_hospital": 1189
      },
      "offence": {
        "weapons related": 69,
        "assaults": 139,
        "sexual offences": 73,
        "robbery": 1,
        "harassment and threatening": 50,
        "total": 1153
      }
    },
    "WANGARATTA": {
      "econ": {
        "unemployment_num": 615,
        "total_people_hospital": 11041,
        "total_male_hospital": 5332,
        "total_female_hospital": 5709
      },
      "offence": {
        "weapons related": 559,
        "assaults": 1199,
        "sexual offences": 363,
        "robbery": 11,
        "harassment and threatening": 371,
        "total": 12290
      }
    },
    "WARRNAMBOOL": {
      "econ": {
        "unemployment_num": 863,
        "total_people_hospital": 18416,
        "total_male_hospital": 8293,
        "total_female_hospital": 10123
      },
      "offence": {
        "weapons related": 472,
        "assaults": 1615,
        "sexual offences": 487,
        "robbery": 38,
        "harassment and threatening": 536,
        "total": 14801
      }
    },
    "WELLINGTON": {
      "econ": {
        "unemployment_num": 1196,
        "total_people_hospital": 17457,
        "total_male_hospital": 8163,
        "total_female_hospital": 9293
      },
      "offence": {
        "weapons related": 733,
        "assaults": 2429,
        "sexual offences": 995,
        "robbery": 26,
        "harassment and threatening": 823,
        "total": 21020
      }
    },
    "WEST WIMMERA": {
      "econ": {
        "unemployment_num": 72,
        "total_people_hospital": 2941,
        "total_male_hospital": 1507,
        "total_female_hospital": 1434
      },
      "offence": {
        "weapons related": 38,
        "assaults": 84,
        "sexual offences": 82,
        "robbery": 0,
        "harassment and threatening": 56,
        "total": 877
      }
    },
    "WHITEHORSE": {
      "econ": {
        "unemployment_num": 5603,
        "total_people_hospital": 72318,
        "total_male_hospital": 31079,
        "total_female_hospital": 41237
      },
      "offence": {
        "weapons related": 674,
        "assaults": 2633,
        "sexual offences": 1110,
        "robbery": 317,
        "harassment and threatening": 780,
        "total": 38949
      }
    },
    "WHITTLESEA": {
      "econ": {
        "unemployment_num": 6868,
        "total_people_hospital": 74934,
        "total_male_hospital": 33267,
        "total_female_hospital": 41667
      },
      "offence": {
        "weapons related": 1735,
        "assaults": 5784,
        "sexual offences": 1124,
        "robbery": 360,
        "harassment and threatening": 2219,
        "total": 71384
      }
    },
    "WODONGA": {
      "econ": {
        "unemployment_num": 1160,
        "total_people_hospital": 17807,
        "total_male_hospital": 8264,
        "total_female_hospital": 9543
      },
      "offence": {}
    },
    "WYNDHAM": {
      "econ": {
        "unemployment_num": 8831,
        "total_people_hospital": 79568,
        "total_male_hospital": 33171,
        "total_female_hospital": 46397
      },
      "offence": {
        "weapons related": 1862,
        "assaults": 5203,
        "sexual offences": 1079,
        "robbery": 573,
        "harassment and threatening": 1422,
        "total": 68777
      }
    },
    "YARRA": {
      "econ": {
        "unemployment_num": 2814,
        "total_people_hospital": 29850,
        "total_male_hospital": 13029,
        "total_female_hospital": 16821
      },
      "offence": {
        "weapons related": 1776,
        "assaults": 3772,
        "sexual offences": 764,
        "robbery": 582,
        "harassment and threatening": 776,
        "total": 63548
      }
    },
    "YARRA RANGES": {
      "econ": {
        "unemployment_num": 3572,
        "total_people_hospital": 73323,
        "total_male_hospital": 33802,
        "total_female_hospital": 39521
      },
      "offence": {
        "weapons related": 1383,
        "assaults": 3439,
        "sexual offences": 1574,
        "robbery": 148,
        "harassment and threatening": 1020,
        "total": 38283
      }
    },
    "YARRIAMBIACK": {
      "econ": {
        "unemployment_num": 136,
        "total_people_hospital": 4823,
        "total_male_hospital": 2471,
        "total_female_hospital": 2352
      },
      "offence": {
        "weapons related": 104,
        "assaults": 300,
        "sexual offences": 132,
        "robbery": 2,
        "harassment and threatening": 69,
        "total": 1974
      }
    }
  }
export const Const = {
    aurin,
    svg_lust,
    svg_gluttony,
    svg_warth,
    svg_positive,
    svg_negative,
    svg_neutral  
}