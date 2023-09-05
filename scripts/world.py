import pygame
from scripts.object import *

class World(Object):
    
    def __init__(self, name, position: tuple, size: tuple) -> None:

        super().__init__(position, size)

        #-# Creating Surface #-#
        self.AddSurface("Unselected", pygame.Surface((466, 100), pygame.SRCALPHA))
        self.AddSurface("Selected", pygame.Surface((466, 100), pygame.SRCALPHA))

        #-# Drawing Borders #-#
        self.surfaces["Unselected"].blit(Image(ImagePath("world", "others")), (0, 0))
        self.surfaces["Selected"].blit(Image(ImagePath("selected_world", "others")), (0, 0))
    
        #-# Drawing world Names #-#
        self.surfaces["Unselected"].blit(pygame.font.Font(None, 32).render(name[:-4], True, (255, 255, 255)), (100, 10))
        self.surfaces["Selected"].blit(pygame.font.Font(None, 32).render(name[:-4], True, (255, 255, 255)), (100, 10))

        worldData = open("worlds/"+name, "r")
        Data = worldData.readlines()
        worldData.close()

        if len(Data) == 102: self.worldSize = "Small World"
        elif len(Data) == 202: self.worldSize = "Medium World"
        elif len(Data) == 302: self.worldSize = "Large World"
        if Data[1].strip("[]\n") == "1": self.difficult = "Easy"
        elif Data[1].strip("[]\n") == "2": self.difficult = "Normal"
        elif Data[1].strip("[]\n") == "3": self.difficult = "Hard"

        #-# Drawing world difficults #-#
        self.surfaces["Unselected"].blit(pygame.font.Font(None, 32).render(self.difficult, True, (255, 255, 255)), (100, 40))
        self.surfaces["Selected"].blit(pygame.font.Font(None, 32).render(self.difficult, True, (255, 255, 255)), (100, 40))
        
        #-# Drawing world sizes #-#
        self.surfaces["Unselected"].blit(pygame.font.Font(None, 32).render(self.worldSize, True, (255, 255, 255)), (100, 70))
        self.surfaces["Selected"].blit(pygame.font.Font(None, 32).render(self.worldSize, True, (255, 255, 255)), (100, 70))

        self.status = "Unselected"
        self.Hide()
