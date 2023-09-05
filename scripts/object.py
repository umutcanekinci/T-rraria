#-# Importing Packages #-#
import pygame
from scripts.path import *
from images import *

#-# Object Class #-#
class Object(pygame.Surface):

	def __init__(self, position: tuple = ("CENTER", "CENTER"), size: tuple = (0, 0), imagePaths = {}, surfaceSize: tuple = None, show = True):
		
		self.status = None
		self.surfaces = {}

		self.size = size
		self.surfaceSize = surfaceSize
		self.show = show

		self.AddImages(imagePaths)
		self.SetSize(size)
		self.SetPosition(position)

	def AddImages(self, imagePaths):

		for name, path in imagePaths.items():
			
			self.AddImage(name, path)

	def AddImage(self, name, imagePath):

		self.AddSurface(name, Image(imagePath, self.size))

	def AddSurface(self, name: str, surface: pygame.Surface):
		
		self.surfaces[name] = surface

	def SetSize(self, size):
		
		if not size and size[0] and size[1]:

			if len(self.images) > 0:

				if "Normal" in self.images:
					size = self.images["Normal"].get_rect().size
				
				else:
					size = self.images.values()[0].get_rect().size

				self.size = self.width, self.height = size
		else:

			self.size = self.width, self.height = size

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
		
		if mousePosition != None and self.rect.collidepoint(mousePosition) and self.show:

			return True
		
		return False

	def isMouseClick(self, event: pygame.event.Event, mousePosition: tuple) -> bool:

		if self.isMouseOver(mousePosition) and event.type == pygame.MOUSEBUTTONUP:

			return True
		
		return False

	def Show(self):
		
		self.show = True

	def Hide(self):

		self.show = False

	def HandleEvents(self, event, mousePosition):
		
		if "Mouse Click" in self.surfaces and self.isMouseClick(event, mousePosition):
			
			self.SetStatus("Mouse Click")

		elif "Mouse Over" in self.surfaces and self.isMouseOver(mousePosition):

			self.SetStatus("Mouse Over")

		elif "Normal" in self.surfaces:

			self.SetStatus("Normal")

	def SetStatus(self, status: str):

		self.status = status

	def Draw(self, surface) -> None:

		if self.show:

			if self.status:
				
				surface.blit(self.surfaces[self.status], self.rect)
				
			elif "Normal" in self.surfaces:

				self.SetStatus("Normal")
				surface.blit(self.surfaces[self.status], self.rect)
		