import pygame

class Leyend:
    WHITE = (255,255,255)
    BLACK = (0,0,0)

    def __init__(self, pos, updater, color=WHITE, bgcolor=BLACK):
        self.pos = pos
        self.updater = updater
        self.string = ''
        self.color = color
        self.bgcolor = bgcolor
        self.font = pygame.font.Font(None, 24)
        
    def update(self, elapsed):
        self.string = self.updater(elapsed)

    def draw(self, screen):
        screen.blit(
            self.font.render(
                self.string,
                True,
                self.color,
                self.bgcolor,
            ),
            self.pos
        )
