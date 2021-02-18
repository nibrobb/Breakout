import pygame
from random import randint

BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    """ Denne klassen beskriver ballen i spillet og arver fra Sprite-klassen """
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Tegn en rektangulær ball
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Starthastigheten settes til 0 da jeg vil at den skal stå i ro på rekkerten
        # før spilleren sender den avgårdet
        self.velocity = [0, 0]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]