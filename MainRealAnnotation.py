import pygame
import pygame.gfxdraw
import DataDecl
import GIS_Calc
import Mouse
import Color
import sys
import FileIO
from tkinter import filedialog
from tkinter import messagebox
import json
import os
import DrawScreen
import Data
from GIS import GIS
import socket
from NMEA0183parser import NMEA0183parser
from _thread import *

global_lon = 0
global_lat = 0
# # 서버 소켓 생성
HOST = '192.168.45.227'
PORT = 5001
# 이미지 확대
img_width_scale = 1
img_height_scale = 1

# isOnNetwork = True
isOnNetwork = False


def drawScreen(img_path: str, startPointX: int, startPointY: int, scaleWidth: int, scaleHeight: int):
    img = pygame.image.load(img_path)
    scaledImg = pygame.transform.scale(img, (scaleWidth, scaleHeight))
    screen.blit(scaledImg, (startPointX, startPointY))


def threaded(client_socket, addr):
    print('>> Connected by :', addr[0], ':', addr[1])

    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    while True:
        try:
            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data:
                print('>> Disconnected by ' + addr[0], ':', addr[1])
                break

            received = str(data, encoding='utf-8')
            # print('수신 : {0}'.format(received))
            # print("파싱:")

            global global_lon
            global global_lat

            tempData = NMEA0183parser(received)
            global_lon = tempData.getValidLongitude()
            global_lat = tempData.getValidLatitude()

        except ConnectionResetError as e:
            print('>> Disconnected by ' + addr[0], ':', addr[1])
            break

    if client_socket in client_sockets:
        client_sockets.remove(client_socket)
        print('remove client list : ', len(client_sockets))

    client_socket.close()


if __name__ == '__main__':

    pygame.init()
    clock = pygame.time.Clock()

    mapName = ""
    gridRow = 0
    gridColumn = 0
    mapBeginX = 0
    mapBeginY = 0
    mapEndX = 0
    mapEndY = 0
    longitude = 0.0
    latitude = 0.0

    screenStartX = 0
    screenStartY = 0
    imageWidth = 0
    imageHeight = 0
    iconCount = 10
    iconWidth = 100
    iconHeigh = 0
    imgStartPointX = screenStartX + iconWidth
    imgStartPointY = screenStartY

    UI_Dict = {'start': -4.0, 'plus_ten': 10.0, 'minus_one': -1.0, 'minus_ten': -10.0, 'END': -5.0, 'INF': 987654321.0,
               'ROAD': 0.01, 'GRASS': 100.0, 'ALREADY_INV_PATH': -1, 'NOT_INVED_PATH': -2, 'SOLUTION_PATH': -3,
               'Intersection_Begin': 0.001, 'Intersection_End': 0.002}
    UI_Dict_key = 'ROAD'

    # 그리드 자료형 명시
    # gridList: list[Data.GridInfo] = []
    gridList = []

    filename = filedialog.askopenfilenames(initialdir=os.path.abspath(__file__), \
                                           title="Choose JSON solution File", \
                                           filetypes=(("Json", '*.json'), ("All files", "*.*")))

    if filename == '':
        messagebox.showwarning("Warning", "Select File")  # 파일 선택 안했을 때 메세지 출력

    fileDir = os.path.dirname(filename[0]) + '/'

    f = open(filename[0], "r")
    jsondata = json.load(f)

    gridRow = jsondata.get("map_row")
    gridColumn = jsondata.get("map_col")
    mapBeginX = jsondata.get("beg_x")
    mapBeginY = jsondata.get("beg_y")
    mapEndX = jsondata.get("dest_x")
    mapEndY = jsondata.get("dest_y")
    longitude = jsondata.get("gps_long")
    latitude = jsondata.get("gps_lat")
    map_grid = jsondata.get("map")

    # mapName = "dgist_2.png"
    mapName = jsondata.get("map_name")
    mapDir = fileDir + mapName
    image = pygame.image.load(mapDir)
    imageWidth = image.get_width() * img_width_scale
    imageHeight = image.get_height() * img_height_scale

    gridIntervalWidth = imageWidth / gridColumn
    gridIntervalHeight = imageHeight / gridRow

    for y in range(gridRow):
        for x in range(gridColumn):
            gridList.append(Data.GridInfo(
                imgStartPointX + (gridIntervalWidth * x),
                imgStartPointY + (gridIntervalHeight * y),
                gridIntervalWidth,
                gridIntervalHeight,
                map_grid[y * gridColumn + x]))

    iconCount = 10
    iconWidth = 100
    iconHeigh = int(imageHeight / iconCount)
    imgStartPointX = screenStartX + iconWidth
    imgStartPointY = screenStartY

    screenWidth = iconWidth + imageWidth
    screenHeight = imageHeight
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    screen.fill(Color.WHITE)


    UI_map_data = Data.UI(mapDir, imgStartPointX, imgStartPointY, imageWidth, imageHeight)
    UI_start_data = Data.UI("assets/start.png", screenStartX, screenStartY + (iconHeigh * 0), iconWidth, iconHeigh)
    UI_end_data = Data.UI("assets/END.png", screenStartX, screenStartY + (iconHeigh * 1), iconWidth, iconHeigh)
    UI_Road_data = Data.UI("assets/ROAD.png", screenStartX, screenStartY + (iconHeigh * 2), iconWidth, iconHeigh)
    UI_Grass_data = Data.UI("assets/GRASS.png", screenStartX, screenStartY + (iconHeigh * 3), iconWidth, iconHeigh)
    UI_cross_begin = Data.UI("assets/int_beg.png", screenStartX, screenStartY + (iconHeigh * 4), iconWidth,
                             iconHeigh)
    UI_cross_end = Data.UI("assets/int_end.png", screenStartX, screenStartY + (iconHeigh * 5), iconWidth,
                           iconHeigh)
    UI_INF_data = Data.UI("assets/infinity.png", screenStartX, screenStartY + (iconHeigh * 6), iconWidth, iconHeigh)
    UI_resetall_data = Data.UI("assets/resetall.png", screenStartX, screenStartY + (iconHeigh * 7), iconWidth,
                               iconHeigh)
    UI_save_data = Data.UI("assets/save.png", screenStartX, screenStartY + (iconHeigh * 8), iconWidth, iconHeigh)
    UI_pause_data = Data.UI("assets/pause.png", screenStartX, screenStartY + (iconHeigh * 9), iconWidth, iconHeigh)

    # 화면 셋팅
    drawScreen(UI_map_data.path, UI_map_data.x, UI_map_data.y, UI_map_data.width, UI_map_data.height)
    drawScreen(UI_Road_data.path, UI_Road_data.x, UI_Road_data.y, UI_Road_data.width, UI_Road_data.height)
    drawScreen(UI_Grass_data.path, UI_Grass_data.x, UI_Grass_data.y, UI_Grass_data.width, UI_Grass_data.height)
    drawScreen(UI_cross_begin.path, UI_cross_begin.x, UI_cross_begin.y, UI_cross_begin.width, UI_cross_begin.height)
    drawScreen(UI_cross_end.path, UI_cross_end.x, UI_cross_end.y, UI_cross_end.width, UI_cross_end.height)
    drawScreen(UI_start_data.path, UI_start_data.x, UI_start_data.y, UI_start_data.width, UI_start_data.height)
    drawScreen(UI_INF_data.path, UI_INF_data.x, UI_INF_data.y, UI_INF_data.width, UI_INF_data.height)
    drawScreen(UI_resetall_data.path, UI_resetall_data.x, UI_resetall_data.y, UI_resetall_data.width,
               UI_resetall_data.height)
    drawScreen(UI_end_data.path, UI_end_data.x, UI_end_data.y, UI_end_data.width, UI_end_data.height)
    drawScreen(UI_save_data.path, UI_save_data.x, UI_save_data.y, UI_save_data.width, UI_save_data.height)
    drawScreen(UI_pause_data.path, UI_pause_data.x, UI_pause_data.y, UI_pause_data.width, UI_pause_data.height)

    Isrunning = True
    IsMousePressed = False

    startGird = 0
    endGird = 0

    gis = GIS(longitude, latitude)
    # gis.getLonMeter(latitude)

    pygame.display.set_caption(mapName)

    for y in range(gridRow):
        for x in range(gridColumn):
            gridList.append(Data.GridInfo(
                imgStartPointX + (gridIntervalWidth * x),
                imgStartPointY + (gridIntervalHeight * y),
                gridIntervalWidth,
                gridIntervalHeight,
                UI_Dict["GRASS"]))

    ## RTK서버 구동
    if(isOnNetwork):
        print('>> Server Start')
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print('>> Wait')
        client_socket, addr = server_socket.accept()
        client_sockets = []
        client_sockets.append(client_socket)
        start_new_thread(threaded, (client_socket, addr))

    ##while
    while Isrunning:
        drawScreen(UI_map_data.path, UI_map_data.x, UI_map_data.y, UI_map_data.width, UI_map_data.height)

        # 맵에 속성별(길, 무한, 시작점...등등) 색상 입히기
        for y in range(gridRow):
            for x in range(gridColumn):
                cur = y * gridColumn + x
                currentX = gridList[cur].x
                currentY = gridList[cur].y
                currentWidth = gridIntervalWidth
                currentHeight = gridIntervalHeight
                currentCost = gridList[cur].girdCost

                if currentCost == UI_Dict["ROAD"]:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.WHITE)
                elif currentCost == UI_Dict['Intersection_Begin']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.PURPLE)
                elif currentCost == UI_Dict['Intersection_End']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.SKYBLUE)
                elif currentCost == UI_Dict["INF"]:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.BLACK)
                elif currentCost == UI_Dict['ALREADY_INV_PATH']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.GREY)
                elif currentCost == UI_Dict['NOT_INVED_PATH']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.WHITE)
                elif currentCost == UI_Dict['start']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.RED)
                elif currentCost == UI_Dict['END']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.BLACK)
                else:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.GREEN)

        for x in range(gridColumn):
            pygame.gfxdraw.line(screen, int(gridList[x].x), 0, int(gridList[x].x), screenHeight, Color.RED)
        for y in range(gridRow):
            cur = y * gridColumn
            pygame.gfxdraw.line(screen, imgStartPointX, int(gridList[cur].y), screenWidth, int(gridList[cur].y),
                                Color.RED)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Isrunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                IsMousePressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                IsMousePressed = False

        clock.tick(600)

        if IsMousePressed:
            # 마우스 클릭 좌표
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            mouseGrid_X = int((mouseX - imgStartPointX) / gridIntervalWidth)
            mouseGrid_Y = int((mouseY - imgStartPointY) / gridIntervalHeight)
            mouseCur_Gird = int(mouseGrid_Y * gridColumn + mouseGrid_X)

            print(mouseGrid_X, mouseGrid_Y)

            # 아이콘 영역
            if mouseX < imgStartPointX:
                # 마우스 여러번 클릭 방지
                IsMousePressed = False

                if UI_start_data.checkMousePostion(mouseX, mouseY):
                    print("start button")
                    UI_Dict_key = 'start'
                elif UI_end_data.checkMousePostion(mouseX, mouseY):
                    UI_Dict_key = 'END'
                    print("end button")
                elif UI_Road_data.checkMousePostion(mouseX, mouseY):
                    UI_Dict_key = 'ROAD'
                    print("Road button")
                elif UI_Grass_data.checkMousePostion(mouseX, mouseY):
                    UI_Dict_key = 'GRASS'
                    print("Grass button")
                elif UI_cross_begin.checkMousePostion(mouseX, mouseY):
                    print("Intersection_Begin button")
                    UI_Dict_key = 'Intersection_Begin'
                elif UI_cross_end.checkMousePostion(mouseX, mouseY):
                    print("Intersection_end button")
                    UI_Dict_key = 'Intersection_End'
                elif UI_INF_data.checkMousePostion(mouseX, mouseY):
                    UI_Dict_key = 'INF'
                    print("INF button")
                elif UI_resetall_data.checkMousePostion(mouseX, mouseY):
                    print("Reset button")
                    for i in range(gridRow * gridColumn):
                        gridList[i].girdCost = UI_Dict['GRASS']
                    print("grid reset complete")
                elif UI_save_data.checkMousePostion(mouseX, mouseY):
                    # new
                    FileIO.SaveMap2(gridList, gridRow, gridColumn, mapEndX, mapEndY, mapBeginX, mapBeginY, gis.startLon,
                               gis.startLat, gis.Lat_meter, gis.Lon_meter, mapName, fileDir)
                elif UI_pause_data.checkMousePostion(mouseX, mouseY):
                    UI_Dict_key = 'PAUSE'

            else:  # 맵 영역
                gridList[mouseCur_Gird].girdCost = UI_Dict[UI_Dict_key]

        if (isOnNetwork):
            coordX, coordY = gis.gps2grid(global_lon, global_lat)

            if(UI_Dict_key == 'PAUSE'):
                print("일시정지")
            elif coordX < gridColumn and coordY < gridRow and coordX >0 and coordY >0:
                img_Gird = int(coordY * gridColumn + coordX)
                print(UI_Dict[UI_Dict_key])
                gridList[img_Gird].girdCost = UI_Dict[UI_Dict_key]
                # print("X: " + str(coordX) + " ,Y: " + str(coordY))
            else:
                print("현재 좌표가 지도 범위 안에 없습니다.")

        pygame.display.update()

print(gis.startLat, gis.startLon)

pygame.quit()
sys.exit()
