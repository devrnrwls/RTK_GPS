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


def drawScreen(img_path:str, startPointX:int, startPointY:int, scaleWidth:int, scaleHeight:int):
    img = pygame.image.load(img_path)
    scaledImg=pygame.transform.scale(img, (scaleWidth, scaleHeight))
    screen.blit(scaledImg, (startPointX, startPointY))

if __name__ == '__main__':

    imgScale = 1

    pygame.init()

    clock = pygame.time.Clock()

    mapPath_Name = ""
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
               'ROAD': 0.01, 'GRASS': 100.0, 'ALREADY_INV_PATH': -1, 'NOT_INVED_PATH': -2, 'SOLUTION_PATH': -3, 'Intersection_Begin': 0.001, 'Intersection_End': 0.002}
    UI_Dict_key = 'ROAD'

    # 그리드 자료형 명시
    # gridList: list[Data.GridInfo] = []
    gridList= []

    print("Write load to load a map, or any character to create a map.")
    choiceLoad = input(str)

    #mapName = "dgist_entire.png"

    if choiceLoad == "load":

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
        file_name = jsondata.get("map_name")


        mapPath_Name = fileDir + file_name

        image = pygame.image.load(mapPath_Name)
        imageWidth = image.get_width() * imgScale
        imageHeight = image.get_height() * imgScale
        iconHeigh = int(imageHeight / iconCount)

        gridIntervalWidth = imageWidth / gridColumn
        gridIntervalHeight = imageHeight / gridRow
        UI_map_data = Data.UI(mapPath_Name, imgStartPointX, imgStartPointY, imageWidth, imageHeight)
        for y in range(gridRow):
            for x in range(gridColumn):
                gridList.append(Data.GridInfo(
                    imgStartPointX + (gridIntervalWidth * x),
                    imgStartPointY + (gridIntervalHeight * y),
                    gridIntervalWidth,
                    gridIntervalHeight,
                    map_grid[y * gridColumn + x]))

        gridList[mapBeginY * gridColumn + mapBeginX].girdCost = UI_Dict['start']
        gridList[mapEndY * gridColumn + mapEndX].girdCost = UI_Dict['END']

    else:
        mapPath = filedialog.askopenfilenames(initialdir=os.path.abspath(__file__), \
                                               title="Choose Image solution File", \
                                               filetypes=(("Png", '*.png'), ("All files", "*.*")))
        if mapPath == '':
            messagebox.showwarning("Warning", "Select File")  # 파일 선택 안했을 때 메세지 출력

        mapPath_Name = mapPath[0]

        for file_path in mapPath:
            file_name = os.path.basename(file_path)
            print(file_name)

        image = pygame.image.load(mapPath_Name)
        imageWidth = image.get_width() * imgScale
        imageHeight = image.get_height() * imgScale
        iconHeigh = int(imageHeight / iconCount)

        print("input grid row and column!")
        gridRow = int(input("row: ")) #실제 지도 높이 크기 (ex) 100m
        gridColumn = int(input("column: ")) #실제 지도 너비 크기 (ex) 100m
        longitude = float(input("gps longitude: ")) #지도 왼쪽 맨위 경도
        latitude = float(input("gps latitude: ")) ##지도 왼쪽 맨위 위도

        gridIntervalWidth= imageWidth / gridColumn
        gridIntervalHeight = imageHeight / gridRow
        UI_map_data = Data.UI(mapPath_Name, imgStartPointX, imgStartPointY, imageWidth, imageHeight)
        for y in range(gridRow):
            for x in range(gridColumn):
                gridList.append(Data.GridInfo(
                    imgStartPointX + (gridIntervalWidth * x),
                    imgStartPointY + (gridIntervalHeight * y),
                    gridIntervalWidth,
                    gridIntervalHeight,
                    UI_Dict["GRASS"]))

    iconCount = 10
    iconWidth = 100
    iconHeigh = int(imageHeight / iconCount)
    imgStartPointX = screenStartX + iconWidth
    imgStartPointY = screenStartY

    screenWidth = iconWidth + imageWidth
    screenHeight = imageHeight
    screen = pygame.display.set_mode((screenWidth, screenHeight))

    # 아이콘이 검정색 글씨에 배경이 없어서 흰색으로 채워줘야 함.
    screen.fill(Color.WHITE)


    UI_start_data = Data.UI("assets/start.png", screenStartX, screenStartY + (iconHeigh * 0), iconWidth, iconHeigh)
    UI_Int_beg_data = Data.UI("assets/int_beg.png", screenStartX, screenStartY + (iconHeigh * 1), iconWidth,
                              iconHeigh)
    UI_Int_end_data = Data.UI("assets/int_end.png", screenStartX, screenStartY + (iconHeigh * 2), iconWidth,
                              iconHeigh)
    UI_minus_ten_data = Data.UI("assets/minus_ten.png", screenStartX, screenStartY + (iconHeigh * 3), iconWidth,
                                iconHeigh)
    UI_end_data = Data.UI("assets/END.png", screenStartX, screenStartY + (iconHeigh * 4), iconWidth, iconHeigh)
    UI_save_data = Data.UI("assets/save.png", screenStartX, screenStartY + (iconHeigh * 5), iconWidth, iconHeigh)
    UI_INF_data = Data.UI("assets/infinity.png", screenStartX, screenStartY + (iconHeigh * 6), iconWidth, iconHeigh)
    UI_resetall_data = Data.UI("assets/resetall.png", screenStartX, screenStartY + (iconHeigh * 7), iconWidth,
                               iconHeigh)
    UI_Road_data = Data.UI("assets/ROAD.png", screenStartX, screenStartY + (iconHeigh * 8), iconWidth, iconHeigh)
    UI_Grass_data = Data.UI("assets/GRASS.png", screenStartX, screenStartY + (iconHeigh * 9), iconWidth, iconHeigh)

    # 화면 셋팅
    drawScreen(UI_map_data.path, UI_map_data.x, UI_map_data.y, UI_map_data.width, UI_map_data.height)
    drawScreen(UI_start_data.path, UI_start_data.x, UI_start_data.y, UI_start_data.width, UI_start_data.height)
    drawScreen(UI_Int_beg_data.path, UI_Int_beg_data.x, UI_Int_beg_data.y, UI_Int_beg_data.width,
               UI_Int_beg_data.height)
    drawScreen(UI_Int_end_data.path, UI_Int_end_data.x, UI_Int_end_data.y, UI_Int_end_data.width,
               UI_Int_end_data.height)
    drawScreen(UI_minus_ten_data.path, UI_minus_ten_data.x, UI_minus_ten_data.y, UI_minus_ten_data.width,
               UI_minus_ten_data.height)
    drawScreen(UI_end_data.path, UI_end_data.x, UI_end_data.y, UI_end_data.width, UI_end_data.height)
    drawScreen(UI_save_data.path, UI_save_data.x, UI_save_data.y, UI_save_data.width, UI_save_data.height)
    drawScreen(UI_INF_data.path, UI_INF_data.x, UI_INF_data.y, UI_INF_data.width, UI_INF_data.height)
    drawScreen(UI_resetall_data.path, UI_resetall_data.x, UI_resetall_data.y, UI_resetall_data.width,
               UI_resetall_data.height)
    drawScreen(UI_Road_data.path, UI_Road_data.x, UI_Road_data.y, UI_Road_data.width, UI_Road_data.height)
    drawScreen(UI_Grass_data.path, UI_Grass_data.x, UI_Grass_data.y, UI_Grass_data.width, UI_Grass_data.height)


    Isrunning = True

    # 마우스 클릭 확인
    IsMousePressed = False

    # lat_meter = GIS_Calc.Lat_meter
    # long_meter = GIS_Calc.Get_Long_Meter(latitude)
    lat_meter = 0.00000900900901 #미터당 위도 변화 값
    long_meter = 0.00001118072 #미터당 위도 변화 값

    startGird=0
    endGird=0

    pygame.display.set_caption(file_name)

    while Isrunning:
        drawScreen(UI_map_data.path, UI_map_data.x, UI_map_data.y, UI_map_data.width, UI_map_data.height)

        # 맵에 속성별(길, 무한, 시작점...등등) 색상 입히기
        for y in range(gridRow):
            for x in range(gridColumn):
                cur = y * gridColumn + x

                currentX =gridList[cur].x
                currentY = gridList[cur].y
                currentWidth = gridIntervalWidth
                currentHeight = gridIntervalHeight
                currentCost = gridList[cur].girdCost

                if currentCost == UI_Dict["ROAD"]:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.WHITE)
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
                elif currentCost == UI_Dict['Intersection_Begin']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.PURPLE)
                elif currentCost ==UI_Dict['Intersection_End']:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.SKYBLUE)
                else:
                    pygame.gfxdraw.box(screen, [currentX, currentY, currentWidth, currentHeight], Color.GREEN)

        for x in range(gridColumn):
            pygame.gfxdraw.line(screen, int(gridList[x].x), 0, int(gridList[x].x), screenHeight, Color.RED)
        for y in range(gridRow):
            cur = y * gridColumn
            pygame.gfxdraw.line(screen, imgStartPointX, int(gridList[cur].y), screenWidth, int(gridList[cur].y), Color.RED)

        #파이게임 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Isrunning = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                IsMousePressed = True
            elif event.type == pygame.MOUSEBUTTONUP:
                IsMousePressed = False

        clock.tick(600)

        # 마우스 클릭 이벤트 처리
        if IsMousePressed:
            # 마우스 클릭 좌표
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]

            mouseGrid_X = int((mouseX - imgStartPointX) / gridIntervalWidth)
            mouseGrid_Y = int((mouseY - imgStartPointY) / gridIntervalHeight)
            mouseCur_Gird = int(mouseGrid_Y * gridColumn + mouseGrid_X)
            print(f"{mouseGrid_X, mouseGrid_Y}")

            # print(mouseX, mouseY)

            #아이콘 영역
            if mouseX < imgStartPointX:
                #마우스 여러번 클릭 방지
                IsMousePressed = False
                if UI_start_data.checkMousePostion(mouseX, mouseY):
                    print("start button")
                    UI_Dict_key = 'start'
                elif UI_Int_beg_data.checkMousePostion(mouseX, mouseY):
                    print("Intersection_Begin button")
                    UI_Dict_key = 'Intersection_Begin'
                elif UI_Int_end_data.checkMousePostion(mouseX, mouseY):
                    print("Intersection_End button")
                    UI_Dict_key = 'Intersection_End'
                elif UI_minus_ten_data.checkMousePostion(mouseX, mouseY):
                    print("minus_ten button")
                    UI_Dict_key = 'minus_ten'
                elif UI_end_data.checkMousePostion(mouseX, mouseY):
                    print("end button")
                    UI_Dict_key = 'END'
                elif UI_INF_data.checkMousePostion(mouseX, mouseY):
                    print("INF button")
                    UI_Dict_key = 'INF'
                elif UI_Road_data.checkMousePostion(mouseX, mouseY):
                    print("Road button")
                    UI_Dict_key = 'ROAD'
                elif UI_Grass_data.checkMousePostion(mouseX, mouseY):
                    print("Grass button")
                    UI_Dict_key = 'GRASS'
                elif UI_resetall_data.checkMousePostion(mouseX, mouseY):
                    for i in range(gridRow * gridColumn):
                        gridList[i].girdCost = UI_Dict['GRASS']
                    print("grid reset complete")
                elif UI_save_data.checkMousePostion(mouseX, mouseY):
                    FileIO.SaveMap2(gridList, gridRow, gridColumn, mapEndX, mapEndY, mapBeginX, mapBeginY, longitude, latitude, lat_meter,
                                   long_meter, file_name, fileDir)
                    print("saved")
            else: #맵 영역
                if gridList[mouseCur_Gird].checkMousePostion(mouseX, mouseY):
                    if UI_Dict_key == 'start':

                        #이전 시작점 제거
                        gridList[mapBeginY * gridColumn + mapBeginX].girdCost = UI_Dict['GRASS']
                        gridList[mouseCur_Gird].girdCost = UI_Dict[UI_Dict_key]
                        startGird = mouseCur_Gird
                        mapBeginX = mouseGrid_X
                        mapBeginY = mouseGrid_Y
                        print(f"settings Beg pos to {mouseGrid_X, mouseGrid_Y}")
                    elif UI_Dict_key == 'END':

                        # 이전 종료지점 제거
                        gridList[mapEndY * gridColumn + mapEndX].girdCost = UI_Dict['GRASS']

                        gridList[mouseCur_Gird].girdCost = UI_Dict[UI_Dict_key]
                        endGird = mouseCur_Gird
                        mapEndX = mouseGrid_X
                        mapEndY = mouseGrid_Y
                        print(f"settings End pos to {mapEndX, mapEndY}")
                    else:
                        gridList[mouseCur_Gird].girdCost=UI_Dict[UI_Dict_key]
                        print("%s", UI_Dict_key)
                else:
                    print("문제 있음!!")
            # screen.fill(Color.WHITE)
        pygame.display.update()


pygame.quit()
sys.exit()

