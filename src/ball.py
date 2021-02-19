import pygame


BLACK = (0, 0, 0)

class Ball(pygame.sprite.Sprite):
    """ Denne klassen beskriver ballen i spillet og arver fra Sprite-klassen """
    def __init__(self, color, radius):
        super().__init__()
        self.radius = radius
        self.image = pygame.Surface([2*radius, 2*radius])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.circle(self.image, color, (radius, radius), radius)

        # Starthastigheten settes til 0 da jeg vil at den skal stå i ro på rekkerten
        # før spilleren sender den avgårdet
        self.velocity = [0, 0]

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

    def bounce(self):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = -self.velocity[1]
