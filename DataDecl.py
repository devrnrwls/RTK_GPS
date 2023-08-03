"""
FILENAME: DataDecl.py
AUTHOR: wonyong Lee
DATE: 12.06.22
DESCRIPTION: file stands for class declaration
"""



class Object():
    def __init__(self,path:str,pos_x:int,pos_y:int,size_x,size_y):
        self.path = path
        self.x = pos_x
        self.y = pos_y
        self.width = size_x
        self.height = size_y
        self.isClicked = False
        self.isCollided = False

class Grid(Object):
    def __init__(self,pos_x,pos_y,size_x,size_y,cost):
        super().__init__("",pos_x,pos_y,size_x,size_y)
        self.cost = cost

class UI(Object):
    def __init__(self,path:str,pos_x,pos_y,size_x,size_y):
        super().__init__(path,pos_x,pos_y,size_x,size_y)


class GridInfo(Object):
    def __init__(self, gridStartPointX, gridStartPointY, gridIntervalWidth, gridIntervalHeight, cost):
        super().__init__("", gridStartPointX, gridStartPointY, gridIntervalWidth, gridIntervalHeight)
        # self.gridStartPointX = pos_x
        # self.gridStartPointY = pos_y
        # self.gridIntervalWidth = size_x
        # self.gridIntervalHeight = size_y
        self.girdCost = cost

