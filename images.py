#-# Importing Packages #-#
import pygame
from scripts.path import *

#-# Image Function #-#
def Image(path: ImagePath, Size=[0, 0], Extension=".png", ReturnSize=False):

	if Size == [0, 0] and ReturnSize == False:
		return pygame.image.load(path).convert_alpha()
	
	Img = pygame.image.load(path).convert_alpha()
	
	if Size[0] == 0: Size[0] = Img.get_width()
	if Size[1] == 0: Size[1] = Img.get_height()
	if Size[0] == 1/3: Size[0] = Img.get_width()//5
	if Size[1] == 1/3: Size[1] = Img.get_height()//5
	if ReturnSize: return [pygame.transform.scale(pygame.image.load(path).convert_alpha(), Size), Size]
	return pygame.transform.scale(pygame.image.load(path).convert_alpha(), Size)


class Object(object):
	def __init__(self, X = "CENTER", Y = "CENTER", Width = None, Height = None, Imagepath = None, Imagepath2 = None, Surface = ""):		
		self.Rect = [self.X, self.Y] = X, Y
		self.Size = [self.Width, self.Height] = Width, Height
		self.Images = [self.Imagepath, self.Imagepath2] = Imagepath, Imagepath2
		self.Surface = Surface
		self.Image1 = Image(self.Imagepath, self.Size)
		if Imagepath2 != None: self.Image2 = Image(self.Imagepath2, self.Size)
		if X == "CENTER": self.X = (Surface[0] - self.Width) / 2
		if Y == "CENTER": self.Y = (Surface[1] - self.Height) / 2

	def MouseOnObject(self, MousePosition):
		if MousePosition != None and pygame.Rect(self.X, self.Y, self.Width, self.Height).collidepoint(MousePosition):
			return True
		return False

	def Click(self, Event, MousePosition):
		if self.MouseOnObject(MousePosition) and Event.type == pygame.MOUSEBUTTONUP:
			return True
		return False

	def Draw(self, Window, MousePosition = None):
		self = Object(self.X, self.Y, self.Width, self.Height, self.Imagepath, self.Imagepath2, self.Surface)
		if self.MouseOnObject(MousePosition) and self.Imagepath2 != None:
			Window.blit(self.Image2, (self.X, self.Y))		
		else:
			Window.blit(self.Image1, (self.X, self.Y))