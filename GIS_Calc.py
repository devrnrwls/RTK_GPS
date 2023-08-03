"""
FILENAME: GIS_Calc.py
AUTHOR: wonyong Lee
DATE: 12.15.22
DESCRIPTION: file stands for calculating gis through gps
"""

import math

"""
Long and Lat Calculation

1 degree on Lat = 111.32km (fixed)
1 min on Lat = 1.855333km (fixed)
1 sec on Lat = 0.030922km (fixed)
1 meter = 0.000011 sec (fixed)
whole Lat length are fixed 

but Long is not
1 degree on Long = 400075*cos(Lat DMS)/360
-> calculate it
"""



Earth_round = 40075.000000  # km
Lat_meter = 0.000009  # per 1 meter
one_sec = 0.000278  # 1/3600


def Get_Long_Meter(Lat):
    LongMeter = Earth_round*math.cos(Lat*math.pi/180.000000)/360.000000
    LongMeter /= 60.000000
    LongMeter /= 60.000000
    LongMeter *= 1000 #round it to meter

    return round(one_sec / LongMeter,6)
