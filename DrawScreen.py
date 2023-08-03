import pygame



class DrawScreen():
    def __init__(self, mapName):

        image = pygame.image.load(mapName)
        self.imageWidth = image.get_width()
        self.imageHeight = image.get_height()

        self.menuWidth = 100
        self.screenWidth = self.menuWidth + self.imageWidth
        self.screenHeight = self.imageHeight
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
