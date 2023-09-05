import pygame
from images import *
from random import choice
from items import Item, Inventory
from scripts.path import *

def CreateWorld(Name, TileNumber, TileSize, Difficult):

	Data = open("worlds/"+Name+".txt", "w")
	Data.write(str(TileSize)+"\n")
	Data.write(Difficult+"\n")

	GroundRow = TileNumber[0] - TileNumber[0]//5

	for i in range(TileNumber[1]):
		Column = []

		if i%20 == 0:
			Biome = choice((1, 8))
			TileType = Biome + choice((1, 2, 3))

		Tree = choice((1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
		TreeLong = choice((5, 6, 7, 8, 9, 10))

		for j in range(TileNumber[0]):
			if j == GroundRow:
				Column.append(TileType)
			elif Tree and GroundRow - TreeLong <= j < GroundRow:
				Column.append(24)
			elif j == GroundRow - 1:					
				Column.append(choice((0, 19, 20, 21, 22)))
			elif j > GroundRow:
				Column.append(Biome)
			else:
				Column.append(0)

		Data.write(str(Column) + "\n")

	Data.close()

class Map(object):

	def __init__(self, Name):

		self.Name = Name

		self.Data = open("worlds/"+self.Name+".txt", "r")
		self.MapData = [[int(self.Row) if not "[" in self.Row else self.Row for self.Row in self.Column.strip("[]\n").split(", ")] for self.Column in self.Data.readlines()]
		self.Data.close()
	
		self.TileNumber = [len(self.MapData[2]), len(self.MapData)]
		self.TileSize = [int(self.MapData[0][0]), int(self.MapData[0][1])]
		self.Size = [self.TileNumber[1]*self.TileSize[0], self.TileNumber[0]*self.TileSize[1]]
		self.Difficult = self.MapData[1][0]
		self.TileSurface = pygame.Surface(self.Size, pygame.SRCALPHA)
		self.BackgroundSurface = pygame.Surface(self.Size)		
		self.Background = Image(ImagePath("background", "others"), [0, 1920], ReturnSize=True)		
		for i in range((self.Size[0] // self.Background[1][0]) + 1):
			self.BackgroundSurface.blit(self.Background[0], (i*self.Background[1][0], 0))

		self.Chests = []

		self.BlockIDs = range(1, 15)
		self.ChestIDs = range(15, 19)
		self.FlowerIDs = range(19, 23)

	def Draw(self):

		self.Surface = self.BackgroundSurface
		self.C = -1

		for self.Column in self.MapData[2:]:

			self.C += 1
			self.R = -1

			for self.Row in self.Column:
				
				self.R += 1
				if type(self.Row) is str:
					print(self.Row)
					self.Inventory = Inventory([0, 0], (int(self.Row[:2]) - 14) * 5)
					self.Chests.append([self.Inventory, [self.C, self.R]])
				elif self.Row != 0:
					self.Surface.blit(Image(ImagePath(str(self.Row), "tiles")), (self.C*64, self.R*64))

		return self.Surface

	def AddTile(self, Position, Type, Game):
		Position[1] += 2

		if (self.MapData[Position[1]][Position[0]] == 0 or self.MapData[Position[1]][Position[0]] in self.FlowerIDs) and (self.MapData[Position[1]+1][Position[0]] in self.BlockIDs or self.MapData[Position[1]-1][Position[0]] in self.BlockIDs or self.MapData[Position[1]][Position[0]+1] in self.BlockIDs or self.MapData[Position[1]][Position[0]-1] in self.BlockIDs):
			if self.MapData[Position[1]][Position[0]] in self.FlowerIDs:
				for i in range(self.TileNumber[0]):
					if self.MapData[Position[1]][Position[0] + i] in self.BlockIDs:
						self.MaxFallPoint = (Position[0] + i)*64
						break
				Game.Items.append(Item(self.MapData[Position[1]][Position[0]], [(Position[1] - 2)*64, Position[0]*64], False, self.MaxFallPoint))
			if Type in self.ChestIDs:
				self.Inventory = Inventory([(Position[1] - 2)*64 + 32, Position[0]*64 - 74], [5, (Type - 14)])
				self.Chests.append([self.Inventory,  [Position[1], Position[0]]])
			self.MapData[Position[1]][Position[0]] = str(Type) + "[]"
			Surface = self.TileSurface
			Surface.blit(Image(ImagePath(str(Type), "tiles")), ((Position[1] - 2)*64, Position[0]*64))
			if not Surface in Game.NewTiles:
				Game.NewTiles.append(Surface)
		
		return Game.NewTiles

	def Save(self):

		self.Data = open("worlds/"+self.Name+".txt", "w")
		for Column in self.MapData: self.Data.write(str(Column).strip("'") + "\n")
		self.Data.close()
		
