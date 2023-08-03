

class Object():
    def __init__(self,pos_x:int,pos_y:int,size_x,size_y):
        self.x = pos_x
        self.y = pos_y
        self.width = size_x
        self.height = size_y

    def checkMousePostion(self, mouseX, mouseY):
        # min = TopLeft
        min = (self.x, self.y)
        # max = BottomRight
        max = (self.x + self.width, self.y + self.height)

        if (mouseX >= min[0] and mouseX <= max[0]
                and mouseY >= min[1] and mouseY <= max[1]):
            return True

        return False

class GridInfo(Object):
    def __init__(self, gridStartPointX, gridStartPointY, gridIntervalWidth, gridIntervalHeight, cost):
        super().__init__(gridStartPointX, gridStartPointY, gridIntervalWidth, gridIntervalHeight)
        self.girdCost = cost

class UI(Object):
    def __init__(self,path:str,pos_x,pos_y,size_x,size_y):
        super().__init__(pos_x,pos_y,size_x,size_y)
        self.path = path