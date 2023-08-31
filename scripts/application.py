#-# Import Packages #-#
import pygame, sys, os
from button import *

#-# Application Class #-#
class Application():
    
    def __init__(self, title: str, size: tuple, backgroundColor: tuple = None, FPS: int = 60) -> None:
        
        self.InitPygame()
        self.InitClock()
        self.SetTitle(title)
        self.SetSize(size)
        self.OpenWindow()
        self.SetFPS(FPS)
        self.SetBackgorundColor(backgroundColor)
        self.objects = {}
        self.tab = ""

    def Run(self, eventHandlings, exitEventsHandling=None) -> None:
        
        #-# Starting App #-#
        self.isRunning = True

        #-# Main Loop #-#
        while self.isRunning:
            
            #-# FPS #-#
            self.clock.tick(self.FPS)

            #-# Getting Mouse Position #-#
            self.mousePosition = pygame.mouse.get_pos()

            #-# Getting Pressed Keys #-#
            self.keys = pygame.key.get_pressed()

            #-# Handling Events #-#
            for event in pygame.event.get():
                
                

                if self.tab in self.objects:
                    
                    if "Buttons" in self.objects[self.tab]:

                        for button in self.objects[self.tab]["Buttons"].values(): button.HandleEvent(event, self.mousePosition)

                    if "Objects" in self.objects[self.tab]:

                        for object in self.objects[self.tab]["Objects"]: object.HandleEvents(event, self.mousePosition)

                if exitEventsHandling:
                    
                    exitEventsHandling(event, self.mousePosition)
                
                else:

                    if event.type == pygame.QUIT:

                        self.Exit()
                    
                    elif event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_ESCAPE:

                            self.Exit()

                eventHandlings(event)

            self.Draw()

    def InitPygame(self) -> None:
        
        pygame.init()

    def InitMixer(self) -> None:

        pygame.mixer.init()

    def InitClock(self) -> None:

        self.clock = pygame.time.Clock()
                
    def OpenWindow(self) -> None:

        self.window = pygame.display.set_mode(self.size)

    def CenterWindow(self) -> None:

        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def SetFPS(self, FPS: int) -> None:
        
        self.FPS = FPS

    def SetTitle(self, title: str) -> None:
        
        self.title = title
        pygame.display.set_caption(self.title)

    def SetSize(self, size: tuple) -> None:

        self.size = self.width, self.height = size

    def SetBackgorundColor(self, color: tuple) -> None:

        self.backgroundColor = color

    def AddObject(self, tab: str, **kwargs):
        
        #-# Creat Tab If not exist #-#
        self.AddTab(tab)
        
        #-# Create object list into tab if not exist #-#
        if "Objects" not in self.objects[tab]:

            self.objects[tab]["Objects"] = []

        newObject = Object(**kwargs)
        self.objects[tab]["Objects"].append(newObject)

    def AddButton(self, name: str, tab: str, position: tuple) -> None:
        
        #-# Creat Tab If not exist #-#
        self.AddTab(tab)

        #-# Create button dict into tab if not exist #-#
        if "Buttons" not in self.objects[tab]:

            self.objects[tab]["Buttons"] = {}
        
        #-# Adding button to tab #-#
        self.objects[tab]["Buttons"][name] = Button(position, self.ButtonSize[tab], name, **self.ButtonProperties)

    def AddTab(self, name: str) -> None:

        #-# Creat Tab If not exist #-#
        if not name in self.objects:

            self.objects[name] = {}

    def Exit(self) -> None:

        self.isRunning = False
        pygame.quit()
        sys.exit()

    def Draw(self) -> None:

        #-# Fill Background #-#
        if self.backgroundColor:

            self.window.fill(self.backgroundColor)

        if self.objects.__contains__(self.tab) and self.objects[self.tab].__contains__("Buttons"):
            for button in self.objects[self.tab]["Buttons"].values(): button.Draw(self.window)

        pygame.display.update()
