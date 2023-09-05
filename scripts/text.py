import pygame
from scripts.object import *
from scripts.color import *

class Text(Object):

    def __init__(self, position, text, textSize, antialias=True, color=White, backgorundColor=None) -> None:
        
        super().__init__(position)

        self.position, self.text, self.textSize, self.antialias, self.color, self.backgroundColor = position, text, textSize, antialias, color, backgorundColor

        self.UpdateText(self.text)

    def UpdateText(self, text: str):

        self.AddSurface("Normal", pygame.font.Font(None, self.textSize).render(text, self.antialias, self.color, self.backgroundColor))


