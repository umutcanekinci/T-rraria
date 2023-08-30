import pygame
from images import *
from random import choice
from pygame.math import Vector2
from math import degrees, atan2
from scripts.path import *

class Item(object):
	def __init__(self, ID, Rect=[0,0], Picked=True, MaxFallPoint=None):
		self.ID, self.Rect, self.Picked, self.MaxFallPoint = ID, Rect, Picked, MaxFallPoint
		self.Image = Image(ImagePath(str(self.ID), "items"))
		self.FirstRect = self.Rect[1]
		self.Facing = choice((-2, 0, 2))
		self.Velocity = Vector2(1, 0)

	def Draw(self, Window, Game=None):
		if not self.Picked:
			if self.FirstRect == None:
				if self.Rect[1] <= self.MaxFallPoint - 52:
					self.Rect[1] += 8
					self.Rect[0] += self.Facing
				elif Game.Player.X <= self.Rect[0] + 16 + Game.BackgroundRect[0] <= Game.Player.X + Game.Player.Hitbox[2] and Game.Player.Y <= self.Rect[1] + 16 + Game.BackgroundRect[1] <= Game.Player.Y + Game.Player.Hitbox[3]:
					self.DistanceX, self.DistanceY = self.Rect[0] + 16 + Game.BackgroundRect[0] - Game.Player.X - Game.Player.Hitbox[2]/2, self.Rect[1] + 16 + Game.BackgroundRect[1] - Game.Player.Y - Game.Player.Hitbox[3]/2
					self.Distance = (abs(self.DistanceX)**2 + abs(self.DistanceY)**2)**(1 / 2)
					#print(self.Distance)
					if self.Distance > 0:
						self.Radian = atan2(-self.DistanceY, self.DistanceX)
						self.Angle = degrees(self.Radian)			
						if self.Distance == 0:
								Game.Player.Inventory.AddItem(self.ID)
								Game.Items.remove(self)
						else:
							self.Rect += self.Velocity.rotate(-self.Angle)
			else:
				if self.FirstRect - 32 < self.Rect[1] <= self.FirstRect:
					self.Rect[1] -= 8
					self.Rect[0] += self.Facing
				else:
					self.FirstRect = None
			
			Window.blit(self.Image, (self.Rect[0] + 16 + Game.BackgroundRect[0], self.Rect[1] + 16 + Game.BackgroundRect[1]))			
		else:
			Window.blit(self.Image, (self.Rect[0] + 16, self.Rect[1] + 16))

class Box(object):
	
	def __init__(self, ID, Rect):
		self.ID = ID
		self.Rect = Rect
		self.Size = self.W, self.H = [64, 64]

		self.Image = pygame.Surface(self.Size, pygame.SRCALPHA)
		self.Image.fill((255, 255, 255, 0))
		self.Image.blit(Image(ImagePath("box", "objects")), (0, 0))

		self.OnImage = pygame.Surface(self.Size, pygame.SRCALPHA)
		self.OnImage.fill((255, 255, 255, 50))
		self.OnImage.blit(Image(ImagePath("box2", "objects")), (0, 0))

		self.SelectedImage = pygame.Surface(self.Size, pygame.SRCALPHA)
		self.SelectedImage.fill((255, 255, 255, 50))
		self.SelectedImage.blit(Image(ImagePath("box3", "objects")), (0, 0))

		self.Item = None

	def AddItem(self, ID, Rect=[0,0], Picked = True):
		self.Item = Item(ID, Rect, Picked)

class Inventory(object):
	
	def __init__(self, Location, Size=[10, 1], Show=False):
		self.Size = Size
		self.Boxs, self.Items = [], []
		self.OnBox, self.SelectedBox = None, 0
		self.DrawCursor = True
		self.Show = Show
		self.Location = Location
		
		for RowNumber in range(self.Size[0]):
			for ColumnNumber in range(self.Size[1]):
				self.AddBox()

	def AddBox(self):
		print(self.Boxs, self.Size, self.Location)
		self.Boxs.append(Box(len(self.Boxs), [self.Location[0] - (self.Size[0]*64)//2 + len(self.Boxs)*64, self.Location[1]]))

	def AddItem(self, ID, Rect=[0,0], Picked = True):
		for self.Box in self.Boxs:
			if self.Box.Item == None:
				self.Box.AddItem(ID, Rect, Picked)
				break

	def Draw(self, Window, CursorPosition):
		self.DrawCursor = True
		for self.Box in self.Boxs:
			
			if pygame.Rect(self.Box.Rect[0], self.Box.Rect[1], self.Box.Size[0], self.Box.Size[1]).collidepoint(CursorPosition):
				self.OnBox = self.Box.ID
			elif self.OnBox == self.Box.ID and not pygame.Rect(self.Box.Rect[0], self.Box.Rect[1], self.Box.Size[0], self.Box.Size[1] + 20).collidepoint(CursorPosition):
				self.OnBox = None

			if self.SelectedBox == self.Box.ID:
				self.Box.Rect[1] = 810
				if pygame.Rect(self.Box.Rect[0], self.Box.Rect[1], self.Box.Size[0], self.Box.Size[1]).collidepoint(CursorPosition):
					self.DrawCursor = False
				Window.blit(self.Box.SelectedImage, self.Box.Rect)
			elif self.OnBox == self.Box.ID:
				self.Box.Rect[1] = 790
				self.DrawCursor = False
				Window.blit(self.Box.OnImage, self.Box.Rect)
			else:
				Window.blit(self.Box.Image, self.Box.Rect)
				self.Box.Rect[1] = 810
				

			if self.Box.Item != None:
				self.Box.Item.Rect = self.Box.Rect
				self.Box.Item.Draw(Window)
