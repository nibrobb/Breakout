import pygame

BLACK = (0, 0, 0)

class Paddle(pygame.sprite.Sprite):
    """ Denne klassen definerer en rekkert og arver fra Sprite-klassen. """

    def __init__(self, color, width, height, screen):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        
        # Instansierer en overflate for å tegne rekkerten på
        self.image = pygame.Surface([width, height])
        
        # Bestemmer bakgrunnsfargen til å være svart
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Forteller pygame at den skal tegne et rektangel fra (0,0)
        #     til høyden og bredden av rekkerten relativt til overflaten
        # Sender også inn fargen fra __init__
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()
    
    # Metode for å bevege rekkerten mot venstre
    def move_left(self, pixels):
        self.rect.x -= pixels
        if self.rect.x < 0:
            self.rect.x = 0

    # Metode for å bevege rekkerten mot høyre
    def move_right(self, pixels):
        self.rect.x += pixels
        # Definerer grensen på hvor langt rekkerten kan bevege seg
        # Generell implementasjon, kan forandre størrelsen på rekkerten seinere
        #     uten at det påvirker funksjonaliteten.
        if self.rect.x > self.screen.get_width() - self.width:
            self.rect.x = self.screen.get_width() - self.width
