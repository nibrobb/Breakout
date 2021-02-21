#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Pre-code for INF-1400

22 January 2020 Revision 5 (Vetle Hofsøy-Woie)
Removed unnecessary tuple return from intersect_circles and
intersect_rectangle_circle.

21 January 2019 Revision 4 (Joakim Alslie):
Deleted Vector2D and replaced it with pygames own Vector2-class. Applied
changes to intersect_circles and intersect_rectangle_circle to be custom for
Vector2. Applied changes to example_code avoid type-errors.

16 January 2017 Revision 3 (Mads Johansen):
Rewritten to conform to Python 3 standard. Made class iterable, added property
as_point, replaced magnitude with __abs__ (to reflect mathematical vector
notation), added rotate method.

22 January 2012 Revision 2 (Martin Ernstsen):
Reraise exception after showing error message.

11 February 2011 Revision 1 (Martin Ernstsen):
Fixed bug in intersect_circle. Updated docstrings to Python standard.
Improved __mul__. Added some exception handling. Put example code in separate
function.

"""

from random import randint

import pygame

from pygame import Vector2

from paddle import Paddle   # Rekkerten
from brick import Brick     # Brikkene
from ball import Ball       # Ballen

# Definerer fargene som vil bli brukt i spillet
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def intersect_rectangle_circle(rec_pos, sx, sy,
                               circle_pos, circle_radius, circle_speed):
    """ Determine if a rectangle and a circle intersects.

    Only works for a rectangle aligned with the axes.

    Parameters:
    rec_pos     - A Vector2 representing the position of the rectangles upper,
                  left corner.
    sx          - Width of rectangle.
    sy          - Height of rectangle.
    circle_pos  - A Vector2 representing the circle's position.
    circle_radius - The circle's radius.
    circle_speed - A Vector2 representing the circles speed.

    Returns:
    None if no intersection. 
    If the rectangle and the circle intersect,returns a 
    normalized Vector2 pointing in the direction the circle will
    move after the collision.
    """

    # Position of the walls relative to the ball
    top = (rec_pos.y) - circle_pos.y
    bottom = (rec_pos.y + sy) - circle_pos.y
    left = (rec_pos.x) - circle_pos.x
    right = (rec_pos.x + sx) - circle_pos.x

    r = circle_radius
    intersecting = left <= r and top <= r and right >= -r and bottom >= -r

    if intersecting:
        # Now need to figure out the vector to return.
        impulse = circle_speed.normalize()

        if abs(left) <= r and impulse.x > 0:
            impulse.x = -impulse.x
        if abs(right) <= r and impulse.x < 0:
            impulse.x = -impulse.x
        if abs(top) <= r and impulse.y > 0:
            impulse.y = -impulse.y
        if abs(bottom) <= r and impulse.y < 0:
            impulse.y = -impulse.y
        return impulse.normalize()
    return None


def intersect_circles(circle_a_position, circle_a_radius,
                      circle_b_position, circle_b_radius):
    """ Determine if two circles intersect
    Parameters:
    circle_a_position       - A Vector2D representing circle A's position
    circle_a_radius    - Circle A's radius
    circle_b_position       - A Vector2D representing circle B's position
    circle_b_radius    - Circle B's radius

    Returns:
    None if no intersection.
    If the circles intersect, returns a normalized
    Vector2 pointing from circle A to circle B.
    """
    # vector from A to B
    dp1p2 = circle_b_position - circle_a_position

    if circle_a_radius + circle_b_radius >= pygame.math.Vector2.length(dp1p2):
        return dp1p2.normalize()
    else:
        return None




def create_font(text, font_family="Arial", size=48, color=(255, 255, 255), bold=False, italic=False):
    """ Hjelper-funksjon som lager et font-objekt med tilhørende 'bounding-box' """
    font = pygame.font.SysFont(font_family, size, bold, italic)
    text = font.render(text, False, color)
    text_rect = text.get_rect()
    return text, text_rect



def game():
    pygame.init()

    score = 0
    lives = 3

    # Stiller inn spill-vinduet
    screen_res = (800, 600)     # Optimal oppløsning
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption("The amazing Breakout clone by Robin Kristiansen (c) 2021")

    # Lager en ny sprite-gruppe, den skal inneholde alle sprites som tegnes på skjermen
    sprites = pygame.sprite.Group()

    paddle = Paddle(WHITE, 100, 20, screen)
    paddle.rect.x = (screen.get_width() - paddle.width) // 2
    paddle.rect.y = screen.get_height() - 3 * paddle.height

    sprites.add(paddle)         # Legger rekkert-objektet inn i sprites-gruppen


    ball = Ball(WHITE, 16)      # Instansierer et ball-objekt, med farge hvit og radius 16 pixler
    sprites.add(ball)           # Legger ball-spriten inn i sprites gruppen


    # Litt aritmetikk for å finne rett størrelse på mellomrommet mellom brikkene
    tile_width = 90
    tile_height = 20
    tiles_per_row = 8
    margin = (screen.get_width() - (tiles_per_row)*tile_width) / (tiles_per_row + 1)
    top_offset = 60

    n_rows = 2

    bricks = pygame.sprite.Group()
    
    # For-løkker som tegner n_rows antall rader med fargede brikker
    for red_rows in range(n_rows):
        for i in range(tiles_per_row):
            brick = Brick(RED, tile_width, tile_height)
            brick.rect.x = margin + i*(tile_width+margin)
            brick.rect.y = top_offset
            sprites.add(brick)
            bricks.add(brick)
        top_offset += tile_height + margin

    for green_rows in range(n_rows):
        for i in range(tiles_per_row):
            brick = Brick(GREEN, tile_width, tile_height)
            brick.rect.x = margin + i*(tile_width+margin)
            brick.rect.y = top_offset
            sprites.add(brick)
            bricks.add(brick)
        top_offset += tile_height + margin

    for blue_rows in range(n_rows):
        for i in range(tiles_per_row):
            brick = Brick(BLUE, tile_width, tile_height)
            brick.rect.x = margin + i*(tile_width+margin)
            brick.rect.y = top_offset
            sprites.add(brick)
            bricks.add(brick)
        top_offset += tile_height + margin


    playing = True              # Game-loop vaiabelen, holder seg True mens spillet pågår
                                # Blir satt til False når score = 0 eller spilleren avslutter

    clock = pygame.time.Clock()

    started = False             # Variabel som tyder på om spillet er startet eller ikke

    bounce_factor = 10          # Faktor som multipliseres med normalvektoren som gjengis av kollisjonsfunksjonen


    while playing:
        # Event handling
        # Håndterer exit-contitions; ved et trykk på krysset i hjørnet av vinduet,
        # eller ved å trykke q-tasten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False                 # Setter er flagg slik at vi kan hoppe ut av loopen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     # Hvis Q-trykkes avsluttes spillet
                    playing = False

        # Fyller skjermen med en heldekkende farge, klar til å tegnes på
        screen.fill(BLACK)


        # Introskjermen, denne teksten vises hver gang spillet starter, og forsvinner når brukeren trykker mellomrom
        if not started:
            pressed_key = pygame.key.get_pressed()
            if pressed_key[pygame.K_SPACE]:
                started = True
                ball.velocity = [randint(5, 10), randint(5, 10)]

            start_text, start_box = create_font("Press SPACE to start!", size=72, color=WHITE)
            sb_center_x, sb_center_y = screen.get_width() // 2, screen.get_height() //2
            start_box = start_text.get_rect(center=(sb_center_x, sb_center_y))
            screen.blit(start_text, start_box)

            # Plasserer ballen på rekkerten slik at spilleren kan bestemme hvor hen vil starte
            ball.rect.x = paddle.rect.x + (paddle.width / 2) - ball.radius
            ball.rect.y = paddle.rect.y - ball.radius


        # Event-handling for bruker-input
        # Flytter rekkerten til venstre eller høyre avhengig av piltasten som trykkes
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left(15)
        if keys[pygame.K_RIGHT]:
            paddle.move_right(15)

        brick_list = bricks.sprites()
        
        if started:
            for brick in brick_list:        # Looper gjennom alle elementer i bricks-gruppen og sjekker for kollisjon
                # Kollisjonshåndtering
                impulse = intersect_rectangle_circle(Vector2(brick.rect.x, brick.rect.y), brick.rect.width, brick.rect.height, Vector2(ball.rect.x, ball.rect.y), ball.radius, Vector2(ball.velocity))
                if impulse:
                    ball.velocity = [impulse.x*bounce_factor, impulse.y*bounce_factor]
                    brick.kill()            # Brick objektet som har blitt kollidert med fjernes fra alle sprite-grupper
                                            # og blir dermed fjernet fra brettet
                    score += 1              # Inkrementer score med 1 da bruker knuste en brikke
            
            # Sjekk for kollisjon mellom ball og rekkert
            impulse = intersect_rectangle_circle(Vector2(paddle.rect.x, paddle.rect.y), paddle.rect.width, paddle.rect.height, Vector2(ball.rect.x, ball.rect.y), ball.radius, Vector2(ball.velocity))
            if impulse:
                ball.velocity = [impulse.x*bounce_factor, impulse.y*bounce_factor]
        
        

        sprites.update()

        if started:
            # simpel kode for å snu retningen til ballen når den treffer en vegg
            if ball.rect.x >= screen.get_width() - 2*ball.radius -2:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.x <= 0:
                ball.velocity[0] = -ball.velocity[0]
            if ball.rect.y >= screen.get_height() - 2*ball.radius -2:
                ball.velocity[1] = -ball.velocity[1]
                lives -= 1                  # Dekrementer liv med 1 ved bunn-treff
                if lives <= 0:
                    game_over(screen, clock, score)
                    break
            if ball.rect.y <= 0:
                ball.velocity[1] = -ball.velocity[1]
            


        

        # Linjen øverst på skjermen som viser poengsum og antall liv igjen
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        # Render'er ovennevnte poeng og liv, ved hjelp av blit'ing
        font = pygame.font.SysFont("Arial", 24)

        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20, 10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650, 10))

        sprites.draw(screen)        # Tegner alle sprites på skjermen


        # Denne koden styrer paddelen med musa
        # mouse_x, mouse_y = pygame.mouse.get_pos()
        # pygame.draw.rect(screen, (255, 255, 255), ((mouse_x - 30, 480 - 24), (60, 20)))

        pygame.display.flip()

        # Setting the framerate
        clock.tick(60)



def game_over(screen, clock, score):
    """
        docstring
    """
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()                 # Setter er flagg slik at vi kan hoppe ut av loopen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     # Hvis Q-trykkes avsluttes spillet
                    pygame.quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            break

        # Game over text, vertically and horizontally centered
        gameover_text, gameover_box = create_font("GAME OVER", "Arial", 128, RED)
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        gameover_box = gameover_text.get_rect(center=(center_x, center_y))

        highscore_text, highscore_box = create_font("Score: " + str(score), size=80, color=BLUE)
        hs_x, hs_y, = screen.get_width() // 2, (screen.get_height() // 2) - 100
        highscore_box = highscore_text.get_rect(center=(hs_x, hs_y))
        screen.blit(highscore_text, highscore_box)

        # Restart text, only horizontally centered, and biased to the bottom
        restart_text, restart_box = create_font("Press SPACE to exit")
        restart_box = int((screen.get_width() - restart_text.get_width()) // 2), screen.get_height() - restart_text.get_height()
        screen.blit(restart_text, restart_box)

        screen.blit(gameover_text, gameover_box)
        clock.tick(60)
        pygame.display.flip()



if __name__ == '__main__':
    game()
    pygame.quit()
