import pygame
from scripts.object import *

class Character(Object):
    
    def __init__(self, name, position: tuple, size: tuple) -> None:

        super().__init__(position, size)

        self.Heart = Image(ImagePath("heart", "objects"))
        self.Heart2 = Image(ImagePath("heart2", "objects"))
        self.Heart3 = Image(ImagePath("heart3", "objects"))

        #-# Creating Surface #-#
        self.AddSurface("Unselected", pygame.Surface((466, 100), pygame.SRCALPHA))
        self.AddSurface("Selected", pygame.Surface((466, 100), pygame.SRCALPHA))

        #-# Drawing Borders #-#
        self.surfaces["Unselected"].blit(Image(ImagePath("player", "others")), (0, 0))
        self.surfaces["Selected"].blit(Image(ImagePath("selected_player", "others")), (0, 0))
    
        #-# Drawing Player Names #-#
        self.surfaces["Unselected"].blit(pygame.font.Font(None, 32).render(name[:-4], True, (255, 255, 255)), (100, 10))
        self.surfaces["Selected"].blit(pygame.font.Font(None, 32).render(name[:-4], True, (255, 255, 255)), (100, 10))
        
        PlayerData = open("players/"+name, "r")

        for line in PlayerData.readlines():

            variable = line.split(" = ")[0]
            value = line.split(" = ")[1]

            if variable == "Character":

                #if self.SelectedPlayer == filenames.index(name):
                #	self.Character = value[:-1]

                self.surfaces["Unselected"].blit(Image(ImagePath("Head ("+ value[-4:-2] +")", "characters/heads"), [70, 70]), (15, 15))
                self.surfaces["Selected"].blit(Image(ImagePath("Head ("+ value[-4:-2] +")", "characters/heads"), [70, 70]), (15, 15))
            
            elif variable == "Health":
                
                #if self.SelectedPlayer == filenames.index(name):
                #	self.Health = int(value)
                
                Health = int(value)
            
            elif variable == "MaxHealth":
                
                #if self.SelectedPlayer == filenames.index(name):
                #	self.MaxHealth = int(value)
                
                MaxHealth = int(value)
            
            elif variable == "Items":
                
                #if self.SelectedPlayer == filenames.index(name):
                
                #	self.PlayerItems = [i for i in value.split(", ")]
                pass

        i = -1
        for i in range(Health//10):

            self.surfaces["Unselected"].blit(self.Heart, (85 + i*35, 15))
            self.surfaces["Selected"].blit(self.Heart, (85 + i*35, 15))

        if Health%10 == 5:

            i += 1
            self.surfaces["Unselected"].blit(self.Heart2, (85 + i*35, 15))
            self.surfaces["Selected"].blit(self.Heart2, (85 + i*35, 15))

        for j in range(9 - i):

            self.surfaces["Unselected"].blit(self.Heart3, (85 + (i+j+1)*35, 15))
            self.surfaces["Selected"].blit(self.Heart3, (85 + (i+j+1)*35, 15))

        PlayerData.close()	

        self.status = "Unselected"
        self.Hide()
