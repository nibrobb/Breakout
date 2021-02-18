import pygame

BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    """ Denne klassen kontrollerer rekkerten.
        Rekkerten skal være av en pygame.sprite-type """

    def __init__(self, color, width, height, screen):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
    
    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self, pixels):
        self.rect.x += pixels
        # Definerer grensen på hvor langt rekkerten kan bevege seg
        if self.rect.x > self.screen.get_width() - self.width:
            self.rect.x = self.screen.get_width() - self.width
