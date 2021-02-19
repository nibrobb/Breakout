import pygame

BLACK = (0, 0, 0)

class Brick (pygame.sprite.Sprite):
    """ Denne klassen beskriver brikkene i spillet og arver fra Sprite-klassen """
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
