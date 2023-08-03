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


class GIS():
    def __init__(self, lon, lat):
        self.startLon = lon
        self.startLat = lat
        self.Earth_round = 40075.000000  # km
        self.Lat_meter = 0.00000900900901  # per 1 meter
        self.Lon_meter = 0.00001118072 # 계산기로 계산 0.000011236
        self.one_sec = 0.000278  # 1/3600

    # def getLonMeter(self, Lat):
    #     LongMeter = self.Earth_round * math.cos(Lat * math.pi / 180.000000) / 360.000000
    #     LongMeter /= 60.000000
    #     LongMeter /= 60.000000
    #     LongMeter *= 1000  # round it to meter
    #     self.Lon_meter = round(self.one_sec / LongMeter, 6)
    #     return self.Lon_meter

    def gps2grid(self, cur_lon, cur_lat):
        lon = cur_lon - self.startLon
        lat = self.startLat - cur_lat

        x = int(lon/self.Lon_meter)
        y = int(lat/self.Lat_meter)

        return x, y
