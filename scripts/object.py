#-# Importing Packages #-#
import pygame
from scripts.path import *
from images import *

#-# Object Class #-#
class Object(object):

	def __init__(self, position: tuple = ("CENTER", "CENTER"), size: tuple = (None, None), imagePaths = {}, surfaceSize: tuple = None):
		
		self.surface = None
		self.surfaceSize = surfaceSize
		self.size = self.width, self.height = size
		self.imagePaths = imagePaths
		
		self.SetPosition(position)
		self.images = {}
		
		for name, path in self.imagePaths.items():
			
			self.AddImage(name, path)

	def AddImage(self, name, imagePath):

		self.AddImagePath(name, imagePath)
		newImage = Image(imagePath, self.size)
		self.images[name] = newImage

	def AddImagePath(self, name, imagePath):

		self.imagePaths[name] = imagePath

	def SetPosition(self, position: tuple) -> None:

		self.position = (0, 0)
		self.SetX(position[0])
		self.SetY(position[1])
		
	def SetX(self, x: int) -> None:

		if x == "CENTER":
		
			self.x = (self.surfaceSize[0] - self.width) / 2

		else:

			self.x = x
		
		self.position = self.x, self.position[1]

		if hasattr(self, "rect"):
		
			self.rect.topleft = self.position

		else:

			self.rect = pygame.Rect(self.position, self.size)

	def SetY(self, y: int) -> None:
		
		if y == "CENTER":
			
			self.y = (self.surfaceSize[1] - self.height) / 2
		
		else:

			self.y = y
			
		self.position = self.position[0], self.y
		
		if hasattr(self, "rect"):
		
			self.rect.topleft = self.position

		else:

			self.rect = pygame.Rect(self.position, self.size)

	def isMouseOver(self, mousePosition: tuple) -> bool:
		
		if mousePosition != None and self.rect.collidepoint(mousePosition):

			return True
		
		return False

	def isMouseClick(self, event: pygame.event.Event, mousePosition: tuple) -> bool:

		if self.isMouseOver(mousePosition) and event.type == pygame.MOUSEBUTTONUP:

			return True
		
		return False

	def HandleEvents(self, event, mousePosition):
		
		if "Mouse Click" in self.images and self.isMouseClick(event, mousePosition):
			
			self.surface = self.images["Mouse Click"]

		elif "Mouse Over" in self.images and self.isMouseOver(mousePosition):

			self.surface = self.images["Mouse Over"]

		elif "Normal" in self.images:

			self.surface = self.images["Normal"]

	def Draw(self, surface) -> None:

		if self.surface:
			
			surface.blit(self.surface, self.rect)
			
		elif "Normal" in self.images:

			self.surface = self.images["Normal"]
			surface.blit(self.surface, self.rect)
		