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

class InputBox:

	def __init__(self, x, y, w, h, text=''):
		self.rect = pygame.Rect(x, y, w, h)
		self.color = pygame.Color('dodgerblue2') # ('lightskyblue3')
		self.text = text
		self.txt_surface = pygame.font.Font(None, 32).render(text, True, self.color)
		self.active = True # False

	def handle_event(self, event):

		if event.type == pygame.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect.
			if self.rect.collidepoint(event.pos):
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

	def draw(self, screen):
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

		for _, dirnames, filenames in os.walk("images/characters/"+str(self.CharacterName)+"/"):
			for SpriteFolder in dirnames:
				self.Sprites[SpriteFolder] = [[Image(ImagePath(Photo[:-4], "characters/"+self.CharacterName+"/"+SpriteFolder), self.Size, Photo[-4:]) for Photo in images] for _, dirnames, images in os.walk("images/characters/"+self.CharacterName+"/"+SpriteFolder+"/")][0]
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
		
		#-# Window Settings #-#
		self.windowSize = self.windowWidth, self.windowHeight = (1440, 900)
		self.windowTitle = "TIRRARIA"

		super().__init__(self.windowTitle, self.windowSize, 30)
		
		#-# Menu Objects #-#
		self.windowBackground = pygame.image.load(ImagePath("background", "others", "jpg")).convert_alpha()		
		self.windowBackground = pygame.transform.scale(self.windowBackground, (self.windowWidth, self.windowHeight))
		self.tab = "Intro"
		self.Intro = Image(ImagePath("intro", "others", "jpg"), self.windowSize)
		self.IntroRect = [0, 0]
		self.Logo = Object("CENTER", 20, 486, 142, ImagePath("logo", "others"), None, self.windowSize)
		
		self.Play = Object("CENTER", 200, 400, 40, ImagePath("play", "button"), ImagePath("play2", "button"), self.windowSize)
		self.contactUs = Object("CENTER", 250, 400, 40,  ImagePath("contact_us", "button"), ImagePath("contact_us2", "button"), self.windowSize)
		self.ExitButton = Object("CENTER", 300, 400, 40, ImagePath("exit", "button"), ImagePath("exit2", "button"), self.windowSize)

		#-# Button Properties #-#
		self.ButtonProperties = dict(Color = (8, 7, 174),
		ActiveColor = (135, 135, 197),
		CornerRadius = 0,
		BorderSize = 2,
		BorderColor = "black",
		FontSize = 23,
		FontColor = "white",
		ActiveFontColor = "white",
		FontSide = "Center",
		FontMargin = 20,
		IconPath = None,
		IconSize = None,
		IconSide = None,
		IconMargin = None
		)
		
		self.ButtonSize = { "Main Menu" : (233, 40),
		     				"Contact Us" : (233, 40),
							"Select Player" : (233, 40),
						    "Select World" : (233, 40),
						    "New Player" : (233, 40),
						    "New World" : (233, 40)}
		
		self.CreateButton({
							"Contact Us" : [["Go Back", (100, 100)]],
							"Select Player" : [["Select Player", (723, 845)], ["New Player", (601, 310)], ["Go Back", (700, 50)]],
							"Select World" : [["Select World", (723, 845)], ["New World", (601, 310)], ["Go Back", (700, 50)]],
						 	"New Player" : [["Create Player", (723, 845)], ["Go Back", (700, 50)]],	  
						  	"New World" : [["Create World", (723, 845)], ["Go Back", (700, 50)]]
							})
						  
		self.SelectWorld = Image(ImagePath("selectWorld", "others"))
		self.NewWorld = Image(ImagePath("NewWorld", "others"))

		self.WorldNameInput = InputBox(601, 350, 233, 40)
		
		self.SocialMedia = Object("CENTER", 200, 600, 600, ImagePath("social_media", "others"), None, self.windowSize)
		self.NextButton = Object(800, 550, 64, 64, ImagePath("next", "button"), ImagePath("next2", "button"))	
		self.NextButton2 = Object(565, 550, 64, 64, ImagePath("next3", "button"), ImagePath("next4", "button"))	
		
		self.Heart = Image(ImagePath("heart", "objects"))
		self.Heart2 = Image(ImagePath("heart2", "objects"))
		self.Heart3 = Image(ImagePath("heart3", "objects"))
		self.SelectedPlayer, self.SelectedWorld = None, None
		self.CountOfPlayers, self.CountOfWorlds = 0, 0
		self.Page = 1
		self.NextPage = Object(870, 740, 64, 64, ImagePath("next", "button"), ImagePath("next2", "button"))
		self.NextPage2 = Object(510, 740, 64, 64, ImagePath("next3", "button"), ImagePath("next4", "button"))
		
		self.SelectPlayer = Image(ImagePath("selectPlayer", "others"))
		
		self.NewPlayer = Image(ImagePath("NewPlayer", "others"))
		

		self.PlayerNameInput = InputBox(550, 350, 345, 40)


		self.CharactersIdle, self.CharacterNames, self.CharacterSize, self.CharacterNo, self.CharacterWalkCount = [], [], [153, 141], 1, 0 #[153, 141]

		for _, dirnames, filenames in os.walk("images/characters/"):
			for CharacterFolder in sorted(dirnames):
				Idle = []
				for _, dirnames, filenames in os.walk("images/characters/"+CharacterFolder+"/Idle/"):
					for Photo in sorted(filenames):
						Idle.append(Image(ImagePath(Photo[:-4], "characters/"+CharacterFolder+"/Idle"), self.CharacterSize, Photo[-4:]))
					break	

				self.CharactersIdle.append(Idle)
				self.CharacterNames.append(CharacterFolder)
			break

		#-# Game Settings #-#
		self.NewTiles, self.Items = [], []
		self.CursorImage = Image(ImagePath("default", "cursor"))
		#pygame.mouse.set_visible(False)
		self.tileSize = [64, 64]

	def CreateButton(self, TabButtons): # [Tab : ["Name", Position]]

		for Tab, Buttons in TabButtons.items():

			for button in Buttons:
			
				Name, Position = button[0], button[1]

				try:

					self.objects

				except AttributeError:

					self.objects = {}
					self.objects["Intro"] = {}

				if Tab not in self.objects:

					self.objects[Tab] = {}

				if "Buttons" not in self.objects[Tab]:
					
					self.objects[Tab]["Buttons"] = {}

				self.objects[Tab]["Buttons"][Name] = Button((Position, self.ButtonSize[Tab]), Name, **self.ButtonProperties)

	def Run(self):
		
		def EventHandling(event):
				
			if self.tab == "Game":

				#print(len(self.Map.MapData), (self.Player.Hitbox[0] - self.BackgroundRect[0])//64, (self.Player.Hitbox[1] - self.BackgroundRect[1])//64, self.Map.BlockIDs)
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
						if self.BackgroundRect[0] - self.Player.MovSpeed >= -self.Map.Size[0] + self.windowWidth and self.Player.X >= 720 - 37:
							self.BackgroundRect[0] -= self.Player.MovSpeed
						elif self.Player.X + self.Player.MovSpeed <= self.windowWidth - self.Player.W:
							self.Player.X += self.Player.MovSpeed
				else:
					self.Player.Standing = True
					self.Player.Running = False

			if self.tab != "Intro" and self.tab != "Main Menu" and self.tab != "Game":
				
				#-# Go Back Button #-#
				if self.objects[self.tab]["Buttons"]["Go Back"].Click(event, self.mousePosition):
					if self.tab == "Select Player" or self.tab == "Contact Us" or self.tab == "Settings": self.tab = "Main Menu"
					elif self.tab == "New Player": self.tab = "Select Player"
					elif self.tab == "Select World": self.tab = "Select Player"
					elif self.tab == "New World": self.tab = "Select World"

			if self.tab == "Intro":
				if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
					self.tab = "Main Menu"

			elif self.tab == "Main Menu":
				if self.Play.Click(event, self.mousePosition):
					self.Page, self.SelectedPlayer = 1, None
					self.tab = "Select Player"
				elif self.contactUs.Click(event, self.mousePosition):	
					self.tab = "Contact Us"

			elif self.tab == "Select Player":

				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.SelectedPlayer == None:
						if event.button == 5:
							self.SelectedPlayer = 0
					else:
						if event.button == 5 and self.SelectedPlayer + 1 < self.CountOfPlayers:
							if self.SelectedPlayer + 1 == self.Page*4:
								self.Page += 1
							self.SelectedPlayer += 1
						elif event.button == 4 and self.SelectedPlayer > 0:
							if self.SelectedPlayer+1 == self.Page*4 - 3:
								self.Page -= 1
							self.SelectedPlayer -= 1

				if self.Page * 4 >= self.CountOfPlayers and (self.CountOfPlayers%4 != 0 or (self.CountOfPlayers%4 == 0 and self.Page == (self.CountOfPlayers//4) + 1)) and self.objects[self.tab]["Buttons"]["New Player"].Click(event, self.mousePosition):
					self.tab = "New Player"

				elif (self.objects[self.tab]["Buttons"]["Select Player"].Click(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]) and self.SelectedPlayer != None:
					self.tab = "Select World"
					self.Page = 1
				
				if self.CountOfPlayers >= 4:
					if self.NextPage.Click(event, self.mousePosition) and self.Page*4 <= self.CountOfPlayers: self.Page += 1
					if self.NextPage2.Click(event, self.mousePosition) and self.Page > 1: self.Page -=1

				if event.type == pygame.MOUSEBUTTONUP and (self.Page-1)*4 != self.CountOfPlayers:	
					for i in range(4):
						if pygame.Rect(490, 300 + i*110, 466, 100).collidepoint(self.mousePosition) and i + (self.Page-1)*4 + 1 <= self.CountOfPlayers:
							self.SelectedPlayer = (self.Page-1)*4 + i
							break

			elif self.tab == "Select World":
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.SelectedWorld == None:
						if event.button == 5:
							self.SelectedWorld = 0
					else:
						if event.button == 5 and self.SelectedWorld + 1 < self.CountOfWorlds:
							if self.SelectedWorld + 1 == self.Page*4:
								self.Page += 1
							self.SelectedWorld += 1
						elif event.button == 4 and self.SelectedWorld > 0:
							if self.SelectedWorld+1 == self.Page*4 - 3:
								self.Page -= 1
							self.SelectedWorld -= 1

				if self.CountOfWorlds >= 4:
					if self.NextPage.Click(event, self.mousePosition) and self.Page*4 <= self.CountOfWorlds: self.Page += 1
					if self.NextPage2.Click(event, self.mousePosition) and self.Page > 1: self.Page -=1
				
				if (self.objects[self.tab]["Buttons"]["Select World"].Click(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]) and self.SelectedWorld != None:
					
					#-# Map Settings #-#
					self.Map = Map(self.WorldName[:-4])
					self.Background = self.Map.Draw()
					self.Page = 1
					self.BackgroundRect = [-((self.Map.Size[0] - self.windowWidth) // 2), -self.Map.Size[1] + 16*64]

					#-# Player Settings #-#
					self.Player = Player(self.CharacterSize, self.Character, self.Health, self.MaxHealth, self.PlayerItems, self)
					self.tab = "Game"

				elif event.type == pygame.MOUSEBUTTONUP and (self.Page-1)*4 != self.CountOfWorlds:	
					for i in range(4):
						if pygame.Rect(490, 300 + i*110, 466, 100).collidepoint(self.mousePosition) and i + (self.Page-1)*4 + 1 <= self.CountOfWorlds:
							self.SelectedWorld = (self.Page-1)*4 + i
							break

				elif self.Page * 4 >= self.CountOfWorlds and (self.CountOfWorlds%4 != 0 or (self.CountOfWorlds%4 == 0 and self.Page == (self.CountOfWorlds//4) + 1)) and self.objects[self.tab]["Buttons"]["New World"].Click(event, self.mousePosition):
					self.tab = "New World"

			elif self.tab == "New Player":
				self.PlayerNameInput.handle_event(event)
				if self.NextButton.Click(event, self.mousePosition) and self.CharacterNo < len(self.CharactersIdle): self.CharacterNo += 1	
				elif self.NextButton2.Click(event, self.mousePosition) and self.CharacterNo > 1: self.CharacterNo -= 1
				elif self.CreatePlayerButton.Click(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]:
					try:
						PlayerData = open("players/"+self.PlayerNameInput.text+".txt", "r")
					except FileNotFoundError:
						PlayerData = open("players/"+self.PlayerNameInput.text+".txt", "w")
						PlayerData.write("Character = "+self.CharacterNames[self.CharacterNo - 1]+"\nMaxHealth = 100\nHealth = 100\nItems = []")
						self.tab = "Select Player"
					finally:
						PlayerData.close()

			elif self.tab == "New World":
				self.WorldNameInput.handle_event(event)
				if self.objects[self.tab]["Buttons"]["Create World"].Click(event, self.mousePosition) or self.keys[pygame.K_KP_ENTER] or self.keys[pygame.K_RETURN]:
					CreateWorld(self.WorldNameInput.text, [30, 200], self.tileSize, "1")
					self.tab = "Select World"

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
							print("a")
							for Chest, Pos in self.Map.Chests:
								if Pos == [[self.CursorColumn + 2][self.CursorRow]]:
									Chest.Show = True
									
						elif self.CursorRow != self.Player.Rect[0] // 64 and self.CursorColumn != self.Player.Rect[1] // 64:
							for self.Player.Inventory.Box in self.Player.Inventory.Boxs:
								if self.Player.Inventory.Box.ID == self.Player.Inventory.SelectedBox and self.Player.Inventory.Box.Item != None:
									self.NewTiles = self.Map.AddTile(self.CPos, self.Player.Inventory.Box.Item.ID, self)

			#-# Updating the Window #-#
			self.WorldNameInput.update()
			self.PlayerNameInput.update()

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
					
		else:

			#-# Draw Window and Objects #-#
			self.window.blit(self.windowBackground, (0, 0))
			self.Logo.Draw(self.window)

			if self.tab == "Main Menu" or self.tab == "Intro":
				
				self.Play.Draw(self.window, self.mousePosition)
				self.contactUs.Draw(self.window, self.mousePosition)
				self.ExitButton.Draw(self.window, self.mousePosition)
				
				if self.tab == "Intro":

					self.IntroRect[1] -= 5
					self.window.blit(self.Intro, self.IntroRect)

			else:

				if self.tab == "Contact Us":
					
					self.SocialMedia.Draw(self.window)	
					self.objects[self.tab]["Buttons"]["Go Back"].SetPosition((70, 700))
				
				else:

					self.objects[self.tab]["Buttons"]["Go Back"].SetPosition((480, 845))
					
					if self.tab == "Select Player":

						self.window.blit(self.SelectPlayer, (480, 180))
						self.objects[self.tab]["Buttons"]["Select Player"].Draw(self.window)
						
						for _, dirnames, filenames in os.walk("players/"):
							for PlayerName in sorted(filenames):
								self.CountOfPlayers = len(filenames)
								if self.Page*4 - 1>= sorted(filenames).index(PlayerName) > (self.Page - 1)*4 - 1:
									PlayerSurface = pygame.Surface((466, 100), pygame.SRCALPHA)
									if self.SelectedPlayer == sorted(filenames).index(PlayerName):
										self.PlayerName = PlayerName
										PlayerSurface.blit(Image(ImagePath("player2", "others")), (0, 0))
									else:	
										PlayerSurface.blit(Image(ImagePath("player", "others")), (0, 0))
									PlayerSurface.blit(pygame.font.Font(None, 32).render(PlayerName[:-4], True, (255, 255, 255)), (100, 10))

									PlayerData = open("players/"+PlayerName, "r")
									for Line in PlayerData.readlines():
										Veriable = Line.split(" = ")[0]
										Value = Line.split(" = ")[1]

										if Veriable == "Character":
											if self.SelectedPlayer == sorted(filenames).index(PlayerName): self.Character = Value[:-1]
											PlayerSurface.blit(Image(ImagePath("Head ("+ Value[-4:-2] +")", "characters/heads"), [70, 70]), (15, 15))
										elif Veriable == "Health":
											if self.SelectedPlayer == sorted(filenames).index(PlayerName): self.Health = int(Value)
											Health = int(Value)
										elif Veriable == "MaxHealth":
											if self.SelectedPlayer == sorted(filenames).index(PlayerName): self.MaxHealth = int(Value)
											MaxHealth = int(Value)
										elif Veriable == "Items" and self.SelectedPlayer == sorted(filenames).index(PlayerName): self.PlayerItems = [i for i in Value.split(", ")]

									i = -1
									for i in range(Health//10):
										PlayerSurface.blit(self.Heart, (85 + i*35, 15))
									if Health%10 == 5:
										i += 1
										PlayerSurface.blit(self.Heart2, (85 + i*35, 15))
									for j in range(9 - i):
										PlayerSurface.blit(self.Heart3, (85 + (i+j+1)*35, 15))
				
									
									self.window.blit(PlayerSurface, (490, 300 + (sorted(filenames).index(PlayerName) - (self.Page - 1)*4)*110))
									PlayerData.close()	
							break

						if self.Page * 4 >= self.CountOfPlayers:
							if self.CountOfPlayers%4 == 0:
								if self.Page == (self.CountOfPlayers//4) + 1:
									self.objects[self.tab]["Buttons"]["New Player"].SetY(310 + self.CountOfPlayers%4 * 110)
									self.objects[self.tab]["Buttons"]["New Player"].Draw(self.window)
							else:
								self.objects[self.tab]["Buttons"]["New Player"].SetY(310 + self.CountOfPlayers%4 * 110)
								self.objects[self.tab]["Buttons"]["New Player"].Draw(self.window)
						#if self.Page * 4 == self.CountOfPlayers:
						#	self.NextPage.ImagePath1 = "buttons, next2"
						#else:
						#	self.NextPage.ImagePath1 = "buttons, next" #         UNworking
						#if self.Page == 1:
						#	self.NextPage2.ImagePath1 = "buttons, next2"
						#else:
						#	self.NextPage2.ImagePath1 = "buttons, next"
						self.window.blit(pygame.font.Font(None, 50).render("Page " + str(self.Page), True, (255, 255, 255)), (670, 750))
						self.NextPage.Draw(self.window, self.mousePosition)
						self.NextPage2.Draw(self.window, self.mousePosition)
					
					elif self.tab == "Select World":

						self.window.blit(self.SelectWorld, (480, 180))
						self.objects[self.tab]["Buttons"]["Select World"].Draw(self.window)

						for _, dirnames, filenames in os.walk("worlds/"):

							for WorldName in sorted(filenames):

								self.CountOfWorlds = len(filenames)

								if self.Page*4 - 1 >= sorted(filenames).index(WorldName) > (self.Page - 1)*4 - 1:

									WorldData = open("worlds/"+WorldName, "r")
									Data = WorldData.readlines()
									WorldData.close()

									if len(Data) == 102: Size = "Small World"
									elif len(Data) == 202: Size = "Medium World"
									elif len(Data) == 302: Size = "Large World"
									if Data[1].strip("[]\n") == "1": Difficult = "Easy"
									elif Data[1].strip("[]\n") == "2": Difficult = "Normal"
									elif Data[1].strip("[]\n") == "3": Difficult = "Hard"

									WorldSurface = pygame.Surface((466, 100), pygame.SRCALPHA)

									if self.SelectedWorld == sorted(filenames).index(WorldName):
										self.WorldName = WorldName									
										WorldSurface.blit(Image(ImagePath("world2", "others")), (0, 0))
									else:
										WorldSurface.blit(Image(ImagePath("world", "others")), (0, 0))
									
									WorldSurface.blit(pygame.font.Font(None, 32).render(WorldName[:-4], True, (255, 255, 255)), (100, 10))
									WorldSurface.blit(pygame.font.Font(None, 32).render(Difficult, True, (255, 255, 255)), (100, 40))
									WorldSurface.blit(pygame.font.Font(None, 32).render(Size, True, (255, 255, 255)), (100, 70))
									
									self.window.blit(WorldSurface, (490, 300 + (sorted(filenames).index(WorldName) - (self.Page - 1)*4)*110))
									
							break

						if self.Page * 4 >= self.CountOfWorlds:
							if self.CountOfWorlds%4 == 0:
								if self.Page == (self.CountOfWorlds//4) + 1:
									
									self.objects[self.tab]["Buttons"]["New World"].SetY(310 + (self.CountOfWorlds%4) * 110)
									self.objects[self.tab]["Buttons"]["New World"].Draw(self.window)
							else:
								self.objects[self.tab]["Buttons"]["New World"].SetY(310 + (self.CountOfWorlds%4) * 110)
								self.objects[self.tab]["Buttons"]["New World"].Draw(self.window)
						#if self.Page * 4 == self.CountOfPlayers:
						#	self.NextPage.ImagePath1 = "buttons, next2"
						#else:
						#	self.NextPage.ImagePath1 = "buttons, next" #         UNworking
						#if self.Page == 1:
						#	self.NextPage2.ImagePath1 = "buttons, next2"
						#else:
						#	self.NextPage2.ImagePath1 = "buttons, next"

						self.window.blit(pygame.font.Font(None, 50).render("Page " + str(self.Page), True, (255, 255, 255)), (670, 750))
						self.NextPage.Draw(self.window, self.mousePosition)
						self.NextPage2.Draw(self.window, self.mousePosition)

					elif self.tab == "New Player":

						self.window.blit(self.NewPlayer, (480, 180))
						self.PlayerNameInput.draw(self.window)

						self.Character = self.CharactersIdle[self.CharacterNo - 1]
						if self.CharacterWalkCount < len(self.Character) - 1: self.CharacterWalkCount += 1
						else: self.CharacterWalkCount = 1
						self.window.blit(self.Character[self.CharacterWalkCount], [683, 514])

						self.NextButton.Draw(self.window)
						self.NextButton2.Draw(self.window)
						self.CreatePlayerButton.Draw(self.window)

					elif self.tab == "New World":

						self.window.blit(self.NewWorld, (480, 180))
						self.WorldNameInput.draw(self.window)
						self.objects[self.tab]["Buttons"]["Create World"].Draw(self.window)

				self.objects[self.tab]["Buttons"]["Go Back"].Draw(self.window)

		#-# Update All Things to the Screen #-#
		pygame.display.update()		

	def ExitEventsHandling(self, Event, mousePosition):

		if Event.type == pygame.QUIT or (self.ExitButton.Click(Event, mousePosition) and self.tab == "Main Menu"):
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

		#if self.MenuButton.Click(event, self.mousePosition):
		#	if len(self.NewTiles) > 0:
		#		self.Map.Save()	
		#	self.tab = "Main Menu"

if __name__ == "__main__":

	game = Game()
	game.Run()
