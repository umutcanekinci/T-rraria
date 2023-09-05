#!/usr/bin/env python3

#-# Import Packages #-#
import os
os.environ['SDL_AUDIODRIVER'] = 'dsp'
import pygame
from tiles import *
from images import *
from items import *
from scripts.application import Application
from scripts.color import *
from button import *
from scripts.path import *
from scripts.object import *
from scripts.playerBox import *
from scripts.worldBox import *

class InputBox:

	def __init__(self, x, y, w, h, text=''):

		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('dodgerblue2') # ('lightskyblue3')
		self.text = text
		self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
		self.active = True # False

	def HandleEvents(self, event, mousePosition):

		if event.type == pygame.MOUSEBUTTONDOWN:

			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(mousePosition):

				# Toggle the active variable.
				self.active = True #not self.active

			else:

				self.active = False

			# Change the current color of the input box.
			self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue3')

		if event.type == pygame.KEYDOWN:

			if self.active:

				if event.key == pygame.K_BACKSPACE:

					self.text = self.text[:-1]

				else:

					self.text += event.unicode

				# Re-render the text.
				self.txt_surface = pygame.font.Font(None, 32).render(self.text, True, self.color)

	def update(self):
		# Resize the box if the text is too long.
		width = max(200, self.txt_surface.get_width()+10)
		if self.rect.w < width:        
			self.rect.w = width

	def Draw(self, screen):
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
		# Blit the rect.
		pygame.draw.rect(screen, self.color, self.rect, 2)

class Player(object):

	def __init__(self, Size, Character, Health, MaxHealth, Items, Game):

		self.Size = [self.W, self.H] = Size
		self.Rect = [self.X, self.Y] = [720 - self.W//2, 514]
		self.CharacterName = Character
		self.Sprites = {}

		for _, dirNames, fileNames in os.walk("images/characters/"+str(self.CharacterName)+"/"):

			for SpriteFolder in dirNames:

				self.Sprites[SpriteFolder] = [[Image(ImagePath(Photo[:-4], "characters/"+self.CharacterName+"/"+SpriteFolder), self.Size, Photo[-4:]) for Photo in images] for _, dirNames, images in os.walk("images/characters/"+self.CharacterName+"/"+SpriteFolder+"/")][0]
			
			break

		self.Images = [self.RightImages, self.LeftImages] = [self.Sprites.get("Idle"), self.Sprites.get("Walk"), self.Sprites.get("Run"), self.Sprites.get("Jump"), self.Sprites.get("Dead")], [[], [], [], [], []]
		

		for i in range(5):

			for i2 in range(15):

				self.LeftImages[i].append(pygame.transform.flip(self.RightImages[i][i2], True, False))

		self.Facing = self.WalkCount= 0
		self.Jumping, self.Falling, self.JumpSpeed, self.FallSpeed, self.MaxJumpPoint, self.MaxFallPoint = False, False, 20, 20, -796, -896
		self.Standing, self.isRunning = True, False

		self.Health, self.MaxHealth = Health, MaxHealth
		
		self.Heart = Image(ImagePath("heart", "objects"))
		self.Heart2 = Image(ImagePath("heart2", "objects"))
		self.Heart3 = Image(ImagePath("heart3", "objects"))

		self.Inventory = Inventory([Game.windowWidth//2, Game.windowHeight - 90],Show=True)
		self.Inventory.Items = Items
		self.Inventory.AddItem(1)
		self.Inventory.AddItem(2)
		self.Inventory.AddItem(3)
		self.Inventory.AddItem(15)
		self.Inventory.AddItem(16)
		self.Inventory.AddItem(17)

	def Draw(self, Window, mousePosition, Tab):

		self.Rect = [self.X, self.Y]

		if self.WalkCount == 14:
			self.WalkCount = 1
		else:
			self.WalkCount += 1

		if self.Jumping or self.Falling:

			Window.blit(self.Images[self.Facing][3][self.WalkCount], self.Rect)	
			
		elif self.isRunning:
			
			self.MovSpeed = 14
			Window.blit(self.Images[self.Facing][2][self.WalkCount], self.Rect)

		elif not self.Standing:

			self.MovSpeed = 7
			Window.blit(self.Images[self.Facing][1][self.WalkCount], self.Rect)

		else:

			self.MovSpeed = 7
			Window.blit(self.Images[self.Facing][0][self.WalkCount], self.Rect)
		

		i = -1

		for i in range(self.Health//10):

			Window.blit(self.Heart, (i*35, 0))

		if self.Health%10 == 5:

			i += 1
			Window.blit(self.Heart2, (i*35, 0))

		for j in range(9 - i):

			Window.blit(self.Heart3, ((i+j+1)*35, 0))

		self.Inventory.Draw(Window, mousePosition)

		if self.Facing == 0:

			self.Hitbox = (self.X, self.Y + 5, 75, 122)

		else:

			self.Hitbox = (self.X + 78, self.Y + 5, 75, 122)
			
		#pygame.draw.rect(Window, (255,0,0), self.Hitbox,2)

class Game(Application):

	def __init__(self):
		
		super().__init__("TIRRARIA", (1440, 900), None, 30)

		#-# Game Settings #-#
		#region

		self.tab = "Intro"
		self.selectedPlayerNumber, self.selectedWorldNumber = None, None
		self.playerCount, self.CountOfWorlds = 0, 0
		self.NewTiles, self.Items = [], []
		self.CursorImage = Image(ImagePath("default", "cursor"))
		#pygame.mouse.set_visible(False)
		self.tileSize = [64, 64]
		
		#endregion

		#-# Creating Objects #-#
		#region 

		self.objects = {}

		#-# Intro Tab Objects #-#
		self.CreateObject("Intro", "Intro", (0,0), self.size, {"Normal" : ImagePath("intro", "others", "jpg")})

		#-# Main Menu Tab Objects #-#
		self.CreateObject("Main Menu", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("Main Menu", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)

		#-# Contact Us Tab Objects #-#
		self.CreateObject("Contact Us", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("Contact Us", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)
		self.CreateObject("Contact Us", "Social Media", ("CENTER", 200), (600, 600), {"Normal" : ImagePath("social_media", "others")}, self.size)

		#-# Select Player Tab Objects #-#
		self.CreateObject("Select Player", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("Select Player", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)
		self.CreateObject("Select Player", "Players Panel", (480, 180), (0, 0), {"Normal" : ImagePath("selectPlayer", "others")})
		self.CreateObject("Select Player", "Next Page", (870, 740), (64, 64), {"Normal" : ImagePath("next", "button"), "Mouse Over" : ImagePath("next2", "button")})
		self.CreateObject("Select Player", "Previous Page", (510, 740), (64, 64), {"Normal" : ImagePath("next3", "button"), "Mouse Over" : ImagePath("next4", "button")})
		
		#-# Select World Tab Objects #-#
		self.CreateObject("Select World", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("Select World", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)
		self.CreateObject("Select World", "Worlds Panel", (480, 180), (0, 0), {"Normal" : ImagePath("selectWorld", "others")})
		self.CreateObject("Select World", "Next Page", (870, 740), (64, 64), {"Normal" : ImagePath("next", "button"), "Mouse Over" : ImagePath("next2", "button")})
		self.CreateObject("Select World", "Previous Page", (510, 740), (64, 64), {"Normal" : ImagePath("next3", "button"), "Mouse Over" : ImagePath("next4", "button")})

		#-# New Player Tab Objects #-#
		self.CreateObject("New Player", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("New Player", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)
		self.CreateObject("New Player", "New Player Panel", (480, 180), (0, 0), {"Normal" : ImagePath("NewPlayer", "others")}, self.size)
		self.CreateObject("New Player", "Next", (800, 550), (64, 64), {"Normal" : ImagePath("next", "button"), "Mouse Over" : ImagePath("next2", "button")})
		self.CreateObject("New Player", "Previous", (565, 550), (64, 64), {"Normal" : ImagePath("next3", "button"), "Mouse Over" : ImagePath("next4", "button")})
		self.AddObject("New Player", "Player Name Input", InputBox(550, 350, 345, 40))

		#-# New World Tab Objects #-#
		self.CreateObject("New World", "Window Background", (0, 0), self.size, {"Normal" : ImagePath("background", "others", "jpg")})
		self.CreateObject("New World", "Logo", ("CENTER", 20), (486, 142), {"Normal" : ImagePath("logo", "others")}, self.size)
		self.CreateObject("New World", "New World Panel", (480, 180), (0, 0), {"Normal" : ImagePath("NewWorld", "others")}, self.size)
		self.AddObject("New World", "World Name Input", InputBox(601, 350, 233, 40))
		
		#endregion

		#-# Creating Texts #-#
		#region
		
		self.CreateText("Select Player", "Page Number", (670, 750), "Page 1", 50)
		self.CreateText("Select World", "Page Number", (670, 750), "Page 1", 50)

		#endregion

		#-# Creating Player Boxes #-#
		# region

		self.players = {}

		for _, dirNames, fileNames in os.walk("players/"):

			fileNames.sort()
			self.playerCount = len(fileNames)
			self.playerPageCount = (self.playerCount // 4) + 1

			for playerNumber, playerName in enumerate(fileNames):

				self.AddPlayer(playerNumber, playerName, (490, 300 + (playerNumber%4)*110), (466, 100))
				
			break

		#endregion

		#-# Creating World Boxes #-#
		# region

		self.worlds = {}

		for _, dirNames, fileNames in os.walk("worlds/"):

			fileNames.sort()
			self.worldCount = len(fileNames)
			self.worldPageCount = (self.playerCount // 4) + 1

			for worldNumber, worldName in enumerate(fileNames):

				self.AddWorld(worldNumber, worldName, (490, 300 + (worldNumber%4)*110), (466, 100))
				
			break

		#endregion

		#-# Creating Buttons #-#
		#region

		#-# Button Properties #-#
		self.buttonProperties = dict( Color = (8, 7, 174), ActiveColor = (135, 135, 197), surfaceSize = self.size)
		self.CreateButtons({

							"Main Menu" : [["Play", ("CENTER", 200), (400, 40)],
					  					  ["Contact Us", ("CENTER", 250), (400, 40)],
										  ["Exit", ("CENTER", 300), (400, 40)]],

							"Contact Us" : [["Go Back", (70, 700), (233, 40)]],

							"Select Player" : [["Select Player", (723, 845), (233, 40)],
											  ["New Player", (601, 200 + (self.playerCount%4 + 1) * 110), (233, 40)],
											  ["Go Back", (480, 845), (233, 40)]],

							"Select World" : [["Select World", (723, 845), (233, 40)],
											 ["New World", (601, 200 + (self.worldCount%4 + 1) * 110), (233, 40)],
						 					 ["Go Back", (480, 845), (233, 40)]],
											  
						 	"New Player" : [["Create Player", (723, 845), (233, 40)],
										   ["Go Back", (480, 845), (233, 40)]],

						  	"New World" : [["Create World", (723, 845), (233, 40)],
										  ["Go Back", (480, 845), (233, 40)]]

							})
		
		#endregion

		self.playersIdle, self.characterNames, self.playersize, self.characterNo, self.characterWalkCount = [], [], [153, 141], 1, 0 #[153, 141]

		for _, dirNames, fileNames in os.walk("images/characters/"):

			for characterFolder in sorted(dirNames):

				Idle = []

				for _, dirNames, fileNames in os.walk("images/characters/"+characterFolder+"/Idle/"):

					for Photo in sorted(fileNames):

						Idle.append(Image(ImagePath(Photo[:-4], "characters/"+characterFolder+"/Idle"), self.playersize, Photo[-4:]))

					break	

				self.playersIdle.append(Idle)
				self.characterNames.append(characterFolder)

			break

	def AddPlayer(self, number, name, position: tuple, size: tuple):

		newPlayer = PlayerBox(name, position, size)
		self.players[number] = newPlayer
		self.AddObject("Select Player", name, newPlayer)

	def AddWorld(self, number, name, position: tuple, size: tuple):

		newWorld = WorldBox(name, position, size)
		self.worlds[number] = newWorld
		self.AddObject("Select World", name, newWorld)

	def ShowPlayerPage(self, pageNumber: int):

		#-# Showing player boxes #-#
		for i in range(4):

			playerNumber = (pageNumber-1)*4 + i

			if(playerNumber < self.playerCount):

				self.players[playerNumber].Show()

	def ShowWorldPage(self, pageNumber: int):

		#-# Showing world boxes #-#
		for i in range(4):

			worldNumber = (pageNumber-1)*4 + i

			if(worldNumber < self.worldCount):

				self.worlds[worldNumber].Show()

	def HidePlayerPage(self, pageNumber: int):

		#-# Hiding player boxes #-#
		for i in range(4):

			playerNumber = (pageNumber-1)*4 + i

			if(playerNumber < self.playerCount):

				self.players[playerNumber].Hide()

	def HideWorldPage(self, pageNumber: int):

		#-# Hiding world boxes #-#
		for i in range(4):

			worldNumber = (pageNumber-1)*4 + i

			if(worldNumber < self.worldCount):

				self.worlds[worldNumber].Hide()

	def OpenPreviousPlayerPage(self):
		
		if self.pageNumber != 1:

			self.HidePlayerPage(self.pageNumber)
			self.pageNumber -= 1
			self.ShowPlayerPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select Player")

	def OpenPreviousWorldPage(self):
		
		if self.pageNumber != 1:

			self.HideWorldPage(self.pageNumber)
			self.pageNumber -= 1
			self.ShowWorldPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select World")

	def OpenPlayerPage(self, pageNumber: int):

		if 0 < pageNumber <= self.playerPageCount :
			
			self.pageNumber = pageNumber
			self.ShowPlayerPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select Player")

	def OpenWorldPage(self, pageNumber: int):

		if 0 < pageNumber <= self.worldPageCount :
			
			self.pageNumber = pageNumber
			self.ShowWorldPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select World")
			
	def OpenNextPlayerPage(self):
		
		if self.pageNumber < self.playerPageCount:

			self.HidePlayerPage(self.pageNumber)
			self.pageNumber += 1
			self.ShowPlayerPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select Player")

	def OpenNextWorldPage(self):
		
		if self.pageNumber < self.worldPageCount:

			self.HideWorldPage(self.pageNumber)
			self.pageNumber += 1
			self.ShowWorldPage(self.pageNumber)
			self.UpdatePlayerPageNumber("Select World")

	def UpdatePlayerPageNumber(self, tab: str):

		self.objects[tab]["Texts"]["Page Number"].UpdateText("Page " + str(self.pageNumber))

		#-# Drawing next / previous page buttons #-#
		#region

		if self.pageNumber < self.playerPageCount:

			self.objects["Select Player"]["Objects"]["Next Page"].Show()

		else:

			self.objects["Select Player"]["Objects"]["Next Page"].Hide()
		
		if self.pageNumber == 1:

			self.objects["Select Player"]["Objects"]["Previous Page"].Hide()

		else:

			self.objects["Select Player"]["Objects"]["Previous Page"].Show()

		#endregion

		#-# Drawing new player button #-#
		#region 

		#-# Show / Hide New Player or New World Button #-#
		if self.pageNumber == self.playerPageCount:

			self.objects["Select Player"]["Buttons"]["New Player"].Show()

		else: 
			
			self.objects["Select Player"]["Buttons"]["New Player"].Hide()

		#endregion

	def UpdateWorldPageNumber(self, tab: str):

		self.objects[tab]["Texts"]["Page Number"].UpdateText("Page " + str(self.pageNumber))

		#-# Drawing next / previous page buttons #-#
		#region

		if self.pageNumber < self.worldPageCount:

			self.objects["Select World"]["Objects"]["Next Page"].Show()

		else:

			self.objects["Select World"]["Objects"]["Next Page"].Hide()
		
		if self.pageNumber == 1:

			self.objects["Select World"]["Objects"]["Previous Page"].Hide()

		else:

			self.objects["Select World"]["Objects"]["Previous Page"].Show()

		#endregion

		#-# Drawing new World button #-#
		#region 

		#-# Show / Hide New World or New World Button #-#
		if self.pageNumber == self.worldPageCount:

			self.objects["Select World"]["Buttons"]["New World"].Show()

		else: 
			
			self.objects["Select World"]["Buttons"]["New World"].Hide()

		#endregion

	def UnselectPlayer(self, playerNumber):

		self.players[playerNumber].SetStatus("Unselected")

	def UnselectWorld(self, worldNumber):

		self.worlds[worldNumber].SetStatus("Unselected")

	def SelectPlayer(self, playerNumber):

		if 0 <= playerNumber < self.playerCount:
			
			if self.selectedPlayerNumber != None:
			
				self.UnselectPlayer(self.selectedPlayerNumber)

			self.selectedPlayerNumber = playerNumber
			self.players[playerNumber].SetStatus("Selected")

	def SelectWorld(self, worldNumber):

		if 0 <= worldNumber < self.worldCount:
			
			if self.selectedWorldNumber != None:
			
				self.UnselectWorld(self.selectedWorldNumber)

			self.selectedWorldNumber = worldNumber
			self.worlds[worldNumber].SetStatus("Selected")

	def SelectNextPlayer(self):
		
		if self.selectedPlayerNumber//4 + 1 == self.pageNumber: # seçilen karakter bu sayfadaysa

			if (self.selectedPlayerNumber + 1)//4 + 1 == self.pageNumber: # seçilen karakterden sonraki karakter bu sayfadaysa

				self.SelectPlayer(self.selectedPlayerNumber + 1)

			elif (self.selectedPlayerNumber + 1)//4 + 1 == self.pageNumber + 1: # seçilen karakterden sonraki karakter sonraki sayfadaysa

				self.SelectPlayer(self.selectedPlayerNumber + 1)
				self.OpenNextPlayerPage()
		
		else:
			
			self.SelectPlayer((self.pageNumber-1)*4)

	def SelectNextWorld(self):
		
		if self.selectedWorldNumber//4 + 1 == self.pageNumber: # seçilen world bu sayfadaysa

			if (self.selectedWorldNumber + 1)//4 + 1 == self.pageNumber: # seçilen worldden sonraki world bu sayfadaysa

				self.SelectWorld(self.selectedWorldNumber + 1)

			elif (self.selectedWorldNumber + 1)//4 + 1 == self.pageNumber + 1: # seçilen worldden sonraki world sonraki sayfadaysa

				self.SelectWorld(self.selectedWorldNumber + 1)
				self.OpenNextWorldPage()
		
		else:
			
			self.SelectPlayer((self.pageNumber-1)*4)
			
	def SelectPreviousPlayer(self):
		
		if self.selectedPlayerNumber//4 + 1 == self.pageNumber: # seçilen karakter bu sayfadaysa
			
			if (self.selectedPlayerNumber - 1)//4 + 1 == self.pageNumber: # seçilen karakterden önceki karakter bu sayfadaysa

				self.SelectPlayer(self.selectedPlayerNumber - 1)

			elif (self.selectedPlayerNumber - 1)//4 + 1 == self.pageNumber - 1: # seçilen karakterden önceki karakter önceki sayfadaysa

				self.SelectPlayer(self.selectedPlayerNumber - 1)
				self.OpenPreviousPlayerPage()

		elif self.selectedPlayerNumber + 1 == self.playerCount:

			self.OpenPreviousPlayerPage()

		else:

			self.SelectPlayer((self.pageNumber-1)*4 + 3)

	def SelectPreviousWorld(self):
		
		if self.selectedWorldNumber//4 + 1 == self.pageNumber: # seçilen world bu sayfadaysa
			
			if (self.selectedWorldNumber - 1)//4 + 1 == self.pageNumber: # seçilen worldden önceki world bu sayfadaysa

				self.SelectWorld(self.selectedWorldNumber - 1)

			elif (self.selectedWorldNumber - 1)//4 + 1 == self.pageNumber - 1: # seçilen worldden önceki world önceki sayfadaysa

				self.SelectWorld(self.selectedWorldNumber - 1)
				self.OpenPreviousWorldPage()

		elif self.selectedWorldNumber + 1 == self.WorldCount:

			self.OpenPreviousWorldPage()

		else:

			self.SelectWorld((self.pageNumber-1)*4 + 3)

	def CreateButtons(self, TabButtons):

		for tab, buttons in TabButtons.items():

			for button in buttons:

				self.CreateButton(tab, *button, **self.buttonProperties)

	def Run(self):

		def EventHandling(event):
				
			if self.tab == "Game":

				self.CursorRow, self.CursorColumn = self.mousePosition[1]//64, self.mousePosition[0]//64
				self.CPos = [self.CRow, self.CColumn] = [(self.mousePosition[1] - self.BackgroundRect[1])//64, (self.mousePosition[0] - self.BackgroundRect[0])//64]
				
				if not (self.Player.Jumping or self.Player.Falling) and (self.keys[pygame.K_SPACE] or self.keys[pygame.K_w] or self.keys[pygame.K_UP]):
					
					self.Player.Jumping = True

				if self.Player.Jumping:

					if self.Player.MaxJumpPoint > self.BackgroundRect[1] >= self.Player.MaxFallPoint:	

						self.BackgroundRect[1] += self.Player.JumpSpeed

					else:

						self.Player.Jumping, self.Player.Falling = False, True

				elif self.Player.Falling == True:

					if self.Player.MaxJumpPoint >= self.BackgroundRect[1] > self.Player.MaxFallPoint:

						self.BackgroundRect[1] -= self.Player.FallSpeed
						
					else:
						self.Player.Jumping, self.Player.Falling = False, False

				if (self.keys[pygame.K_LEFT] or self.keys[pygame.K_a]):
					if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:
						self.Player.Running = True
					else:
						self.Player.Running = False
					self.Player.Standing = False
					if self.Player.Facing == 0:
						self.Player.Facing = 1							
						self.Player.X -= 78

					if self.Map.MapData[(self.Player.Hitbox[0] + self.Player.MovSpeed - self.BackgroundRect[0])//64 + 2][(self.Player.Hitbox[1] - self.BackgroundRect[1])//64] not in self.Map.BlockIDs and self.Map.MapData[(self.Player.Hitbox[0] - self.BackgroundRect[0])//64 + 2][(self.Player.Hitbox[1] - self.BackgroundRect[1])//64 + 1] not in self.Map.BlockIDs:
						if self.BackgroundRect[0] + self.Player.MovSpeed <= 0 and self.Player.X <= 720 - 37 - 78:
							self.BackgroundRect[0] += self.Player.MovSpeed
						elif self.Player.X - self.Player.MovSpeed > 0:
							self.Player.X -= self.Player.MovSpeed

				elif (self.keys[pygame.K_RIGHT] or self.keys[pygame.K_d]):
					if self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]:
						self.Player.Running = True
					else:
						self.Player.Running = False
					self.Player.Standing = False	

					if self.Player.Facing == 1:
						self.Player.Facing = 0
						self.Player.X += 78

					if self.Map.MapData[(self.Player.Hitbox[0] + self.Player.MovSpeed + self.Player.Hitbox[2] - self.BackgroundRect[0])//64 + 2][(self.Player.Hitbox[1] - self.BackgroundRect[1])//64] not in self.Map.BlockIDs and self.Map.MapData[(self.Player.Hitbox[0] + self.Player.Hitbox[2] - self.BackgroundRect[0])//64 + 2][(self.Player.Hitbox[1] - self.BackgroundRect[1])//64 + 1] not in self.Map.BlockIDs:
						if self.BackgroundRect[0] - self.Player.MovSpeed >= -self.Map.Size[0] + self.width and self.Player.X >= 720 - 37:
							self.BackgroundRect[0] -= self.Player.MovSpeed
						elif self.Player.X + self.Player.MovSpeed <= self.width - self.Player.W:
							self.Player.X += self.Player.MovSpeed
				else:
					self.Player.Standing = True
					self.Player.Running = False

			if self.tab != "Intro" and self.tab != "Main Menu" and self.tab != "Game":
				
				#-# Go Back Button #-#
				if self.objects[self.tab]["Buttons"]["Go Back"].isMouseClick(event, self.mousePosition):
					if self.tab == "Select Player" or self.tab == "Contact Us" or self.tab == "Settings": self.tab = "Main Menu"
					elif self.tab == "New Player": self.tab = "Select Player"
					elif self.tab == "Select World": self.tab = "Select Player"
					elif self.tab == "New World": self.tab = "Select World"

			if self.tab == "Intro":
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
					self.tab = "Main Menu"

			elif self.tab == "Main Menu":

				if self.objects[self.tab]["Buttons"]["Play"].isMouseClick(event, self.mousePosition):
					
					self.OpenPlayerPage(1)
					self.SelectPlayer(0)
					self.tab = "Select Player"

				elif self.objects[self.tab]["Buttons"]["Contact Us"].isMouseClick(event, self.mousePosition):	

					self.tab = "Contact Us"

			elif self.tab == "Select Player":

				if event.type == pygame.MOUSEBUTTONUP:

					if event.button == 5:

						self.SelectNextPlayer()

					elif event.button == 4:

						self.SelectPreviousPlayer()

					else:
						
						for i in range(len(self.players)):

							if self.players[i].isMouseClick(event, self.mousePosition):
						
								self.SelectPlayer(i)

				if self.objects[self.tab]["Buttons"]["New Player"].isMouseClick(event, self.mousePosition):
					
					self.tab = "New Player"

				elif (self.objects[self.tab]["Buttons"]["Select Player"].isMouseClick(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]) and self.selectedPlayerNumber != None:
					
					self.OpenWorldPage(1)
					self.SelectWorld(0)
					self.tab = "Select World"
				
				elif self.objects[self.tab]["Objects"]["Next Page"].isMouseClick(event, self.mousePosition):
					
					self.OpenNextPlayerPage()

				elif self.objects[self.tab]["Objects"]["Previous Page"].isMouseClick(event, self.mousePosition):
					
					self.OpenPreviousPlayerPage()

			elif self.tab == "Select World":
				
				if event.type == pygame.MOUSEBUTTONUP:

					if event.button == 5:

						self.SelectNextWorld()

					elif event.button == 4:

						self.SelectPreviousWorld()

					else:
						
						for i in range(len(self.worlds)):

							if self.worlds[i].isMouseClick(event, self.mousePosition):
						
								self.SelectWorld(i)

				if self.objects[self.tab]["Buttons"]["New World"].isMouseClick(event, self.mousePosition):
					
					self.tab = "New World"

				elif (self.objects[self.tab]["Buttons"]["Select World"].isMouseClick(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]) and self.selectedWorldNumber != None:
					
					world = self.worlds[self.selectedWorldNumber]
					player = self.players[self.selectedPlayerNumber]

					#-# Map Settings #-#
					self.Map = Map(world.name[:-4])
					self.Background = self.Map.Draw()

					self.BackgroundRect = [-((self.Map.Size[0] - self.width) // 2), -self.Map.Size[1] + 16*64]

					#-# World Settings #-#
					self.Player = Player(player.size, player.character, player.HP, player.maxHP, player.items, self)
					self.tab = "Game"
					self.pageNumber = 1
					self.UpdateWorldPageNumber(self.tab)

				elif self.objects[self.tab]["Objects"]["Next Page"].isMouseClick(event, self.mousePosition):
					
					self.OpenNextWorldPage()

				elif self.objects[self.tab]["Objects"]["Previous Page"].isMouseClick(event, self.mousePosition):
					
					self.OpenPreviousWorldPage()

			elif self.tab == "New Player":
				
				if self.objects[self.tab]["Objects"]["Next"].isMouseClick(event, self.mousePosition) and self.CharacterNo < len(self.playersIdle):
					
					self.CharacterNo += 1	
				
				elif self.objects[self.tab]["Objects"]["Previous"].isMouseClick(event, self.mousePosition) and self.CharacterNo > 1:
					
					self.CharacterNo -= 1
				
				elif self.objects[self.tab]["Buttons"]["Create Player"].isMouseClick(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]:
					
					try:

						playerData = open("players/"+self.objects[self.tab]["Objects"]["Player Name Input"].text+".txt", "r")
					
					except FileNotFoundError:
						
						playerData = open("players/"+self.objects[self.tab]["Objects"]["Player Name Input"].text+".txt", "w")
						playerData.write("Character = "+self.CharacterNames[self.CharacterNo - 1]+"\nMaxHealth = 100\nHealth = 100\nItems = []")
						self.tab = "Select Player"

					finally:

						playerData.close()

				self.objects[self.tab]["Objects"]["Player Name Input"].update()

			elif self.tab == "New World":

				if self.objects[self.tab]["Buttons"]["Create World"].isMouseClick(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]:
					
					CreateWorld(self.objects[self.tab]["Objects"]["World Name Input"].text, [30, 200], self.tileSize, "1")
					self.tab = "Select World"

				else:

					self.objects[self.tab]["Objects"]["World Name Input"].update()

			elif self.tab == "Game":
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 5:
						if self.Player.Inventory.SelectedBox < len(self.Player.Inventory.Boxs) - 1:
							self.Player.Inventory.SelectedBox += 1
						else:
							self.Player.Inventory.SelectedBox = 0

					elif event.button == 4:
						if self.Player.Inventory.SelectedBox > 0:
							self.Player.Inventory.SelectedBox -= 1
						else:
							self.Player.Inventory.SelectedBox = len(self.Player.Inventory.Boxs) - 1
					elif event.button == 1 or event.button == 2 or event.button == 3:
						if pygame.Rect(self.Player.Inventory.Boxs[0].Rect[0], self.Player.Inventory.Boxs[0].Rect[1], 64*len(self.Player.Inventory.Boxs), 64).collidepoint(self.mousePosition):
							for self.Player.Inventory.Box in self.Player.Inventory.Boxs:
								if self.Player.Inventory.OnBox == self.Player.Inventory.Box.ID:
									if pygame.Rect(self.Player.Inventory.Box.Rect[0], self.Player.Inventory.Box.Rect[1], self.Player.Inventory.Box.Size[0], self.Player.Inventory.Box.Size[1] + 20).collidepoint(self.mousePosition):
										self.Player.Inventory.SelectedBox = self.Player.Inventory.Box.ID	
								else:						
									if pygame.Rect(self.Player.Inventory.Box.Rect[0], self.Player.Inventory.Box.Rect[1], self.Player.Inventory.Box.Size[0], self.Player.Inventory.Box.Size[1]).collidepoint(self.mousePosition):
											self.Player.Inventory.SelectedBox = self.Player.Inventory.Box.ID				

						elif self.Map.MapData[self.CursorColumn + 2][self.CursorRow] in self.Map.ChestIDs:

							for Chest, Pos in self.Map.Chests:
								if Pos == [[self.CursorColumn + 2][self.CursorRow]]:
									Chest.Show = True
									
						elif self.CursorRow != self.Player.Rect[0] // 64 and self.CursorColumn != self.Player.Rect[1] // 64:
							for self.Player.Inventory.Box in self.Player.Inventory.Boxs:
								if self.Player.Inventory.Box.ID == self.Player.Inventory.SelectedBox and self.Player.Inventory.Box.Item != None:
									self.NewTiles = self.Map.AddTile(self.CPos, self.Player.Inventory.Box.Item.ID, self)

		super().Run(EventHandling, self.ExitEventsHandling)

	def Draw(self):

		if self.tab == "Game":

			self.window.blit(self.Background, self.BackgroundRect)

			for self.NewTile in self.NewTiles:
				self.window.blit(self.NewTile, self.BackgroundRect)

			if self.Player.Inventory.DrawCursor:
				for self.Player.Inventory.Box in self.Player.Inventory.Boxs:
					if self.Player.Inventory.Box.ID == self.Player.Inventory.SelectedBox and self.Player.Inventory.Box.Item != None:
						self.CursorTileImage = Image(ImagePath(str(self.Player.Inventory.Box.Item.ID), "tiles"))
						self.window.blit(self.CursorTileImage, (((self.mousePosition[0]-self.BackgroundRect[0])//64)*64 + self.BackgroundRect[0], ((self.mousePosition[1]-self.BackgroundRect[1])//64)*64 + self.BackgroundRect[1]))
				self.window.blit(self.CursorImage, (((self.mousePosition[0]-self.BackgroundRect[0])//64)*64 + self.BackgroundRect[0], ((self.mousePosition[1]-self.BackgroundRect[1])//64)*64 + self.BackgroundRect[1]))
			self.Player.Draw(self.window, self.mousePosition, self.tab)

			for self.Chest, Pos in self.Map.Chests:
				self.Chest.Draw(self.window, self.mousePosition)

			for self.Item in self.Items:
				self.Item.Draw(self.window, self)

		elif self.tab == "Intro":
			
			#-# Intro Move Animation #-#
			if self.objects[self.tab]["Objects"]["Intro"].y > -self.height:

				self.objects[self.tab]["Objects"]["Intro"].SetY(self.objects[self.tab]["Objects"]["Intro"].y-5)

			else:

				self.tab = "Main Menu"

		elif self.tab == "New Player":

			self.Character = self.playersIdle[self.characterNo - 1]

			if self.characterWalkCount < len(self.Character) - 1:
				
				self.characterWalkCount += 1

			else:

				self.characterWalkCount = 1

			self.window.blit(self.Character[self.characterWalkCount][0], [683, 514])

		super().Draw()

	def ExitEventsHandling(self, Event, mousePosition):

		if Event.type == pygame.QUIT or (self.objects["Main Menu"]["Buttons"]["Exit"].isMouseClick(Event, mousePosition) and self.tab == "Main Menu"):
			if self.tab == "Game" and len(self.NewTiles) > 0:
				self.Map.Save()
			self.Exit()
		elif Event.type == pygame.KEYUP:
			if Event.key == pygame.K_ESCAPE:
				if self.tab == "Game" or self.tab == "Contact Us" or self.tab == "Select Player":
					if self.tab == "Game" and len(self.NewTiles) > 0:
						self.Map.Save()
					self.tab = "Main Menu"
				elif self.tab == "Intro": self.tab == "Main Menu"
				elif self.tab == "Select World" or self.tab == "New Player":
					self.tab = "Select Player"
				elif self.tab == "New World":
					self.tab = "Select World"				
				elif self.tab == "Main Menu":
					self.Exit()

		#if self.MenuButton.isMouseClick(event, self.mousePosition):
		#	if len(self.NewTiles) > 0:
		#		self.Map.Save()	
		#	self.tab = "Main Menu"

if __name__ == "__main__":

	game = Game()
	game.Run()
