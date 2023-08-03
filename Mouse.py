"""
FILENAME: Mouse.py
AUTHOR: wonyong Lee
DATE: 12.08.22
DESCRIPTION: file stands for Mouse class
"""
import DataDecl


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.IsClicked = False
        self.IsPressed = False

    def AABB(self, Object: DataDecl.Object):
        # min = TopLeft
        min = (Object.x, Object.y)
        # max = BottomRight
        max = (Object.x + Object.width, Object.y + Object.height)

        if (self.x >= min[0] and self.x <= max[0]
                and self.y >= min[1] and self.y <= max[1]):
            return True

        return False

    
    