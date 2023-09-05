#-# Import Packages #-#
import pygame
from scripts.images import *

#-# Player Class #-#
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