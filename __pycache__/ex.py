import pygame, os, sys
from images import Image

Window = pygame.display.set_mode((2000, 500))
Run = True

CharactersIdle, CharacterSize, CharacterWalkCount = [], [153, 141], 0 #[153, 141]

for _, dirnames, filenames in os.walk("images/characters/"):
	for CharacterFolder in sorted(dirnames):
		Idle = []
		for _, dirnames, filenames in os.walk("images/characters/"+CharacterFolder+"/Idle/"):
			for Photo in sorted(filenames):
				Idle.append(Image("characters/"+CharacterFolder+"/Idle"+", "+Photo[:-4], CharacterSize, Photo[-4:]))
			break	

		CharactersIdle.append(Idle)
	break

while Run:
	Window.fill((255,255,0))
	
	for Event in pygame.event.get():
		if Event.type == pygame.QUIT: Run = False

	Hitboxes = [(0, 5, 75, 122), (150, 0, 75, 122), (300, 0, 75, 122), (450, 0, 75, 122), (600, 0, 75, 122), (750, 0, 75, 122), (900, 0, 75, 122), (1050, 0, 75, 122), (1200, 0, 75, 122), (1350, 0, 75, 122), (1500, 0, 75, 122), (1650, 0, 75, 122), (1800, 0, 75, 122), (1950, 0, 75, 122), (0, 0, 75, 122)]
	for Character in CharactersIdle:

		#if CharacterWalkCount < len(Character) - 1: CharacterWalkCount += 1
		#else: CharacterWalkCount = 1
		
		Window.blit(Character[0], [CharactersIdle.index(Character) * 150, 0])
		pygame.draw.rect(Window, (255,0,0), Hitboxes[CharactersIdle.index(Character)], 2)

	pygame.display.update()
	
