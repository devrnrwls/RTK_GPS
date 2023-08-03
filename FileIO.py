"""
FILENAME: FileIO.py
AUTHOR: wonyong Lee
DATE: 12.09.22
DESCRIPTION: file stands for File IO
"""
import Data
import DataDecl

def SaveMap2(grid:Data.GridInfo,Grid_row,Grid_Col,End_pos_x,End_pos_y,Beg_pos_x,Beg_pos_y,long,lat,latmeter, longmeter, map_name, fileDir):
    tmp_name = map_name.split(".")
    file_name = tmp_name[0] + ".json"
    # f = open("gj_test.json",'w')
    f = open(fileDir + file_name, 'w')
    print(f.name)
    data = "{\n\"map_name\": "
    data += "\"%s\",\n" % map_name
    data +="\"map_row\": "
    data += "%d,\n" %Grid_row
    data += "\"map_col\": "
    data += "%d,\n" %Grid_Col
    data += "\"beg_x\": %d,\n"%Beg_pos_x
    data += "\"beg_y\": %d,\n" %Beg_pos_y
    data += "\"dest_x\": %d,\n" %End_pos_x
    data += "\"dest_y\": %d,\n" %End_pos_y
    data += "\"gps_long\": %.11f,\n" %long
    data += "\"gps_lat\": %.11f,\n" %lat
    data += "\"lat_meter\": %.11f,\n" % latmeter
    data += "\"long_meter\": %.11f,\n" %longmeter
    data += "\"map\":\n["
    for i in range(Grid_row*Grid_Col):
        if i != Grid_row*Grid_Col-1:
            data += "%.3f," %grid[i].girdCost
        else:
            data += "%.3f" %grid[i].girdCost
        
    
    data += "]\n }"

    f.write(data)
    f.close()


def SaveMap(grid: Data.GridInfo, Grid_row, Grid_Col, End_pos_x, End_pos_y, Beg_pos_x, Beg_pos_y, long, lat, latmeter,
            longmeter, map_name):
    tmp_name = map_name.split(".")
    file_name = tmp_name[0] + ".json"
    # f = open("gj_test.json",'w')
    f = open(file_name, 'w')
    print(f.name)
    data = "{\n\"map_name\": "
    data += "\"%s\",\n" % map_name
    data += "\"map_row\": "
    data += "%d,\n" % Grid_row
    data += "\"map_col\": "
    data += "%d,\n" % Grid_Col
    data += "\"beg_x\": %d,\n" % Beg_pos_x
    data += "\"beg_y\": %d,\n" % Beg_pos_y
    data += "\"dest_x\": %d,\n" % End_pos_x
    data += "\"dest_y\": %d,\n" % End_pos_y
    data += "\"gps_long\": %.11f,\n" % long
    data += "\"gps_lat\": %.11f,\n" % lat
    data += "\"lat_meter\": %.11f,\n" % latmeter
    data += "\"long_meter\": %.11f,\n" % longmeter
    data += "\"map\":\n["
    for i in range(Grid_row * Grid_Col):
        if i != Grid_row * Grid_Col - 1:
            data += "%.3f," % grid[i].girdCost
        else:
            data += "%.3f" % grid[i].girdCost

    data += "]\n }"

    f.write(data)
    f.close()
