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

import os
import pygame

from pygame import Vector2
#from pygame.draw import rect

from random import randint
from paddle import Paddle   # Rekkerten
from brick import Brick     # Brikkene
from ball import Ball       # Ballen

# Definerer fargene som vil bli brukt i spillet
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
REBECCAPURPLE = (102, 51, 153)


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


def example_code():
    """ Example showing the use of the above code. """

    screen_res = (640, 480)
    pygame.init()

    rectangle_a_position = Vector2(320, 320)
    rectangle_a_size_x = rectangle_a_size_y = 128

    rectangle_b_position = Vector2(250, 250)
    rectangle_b_size_x = rectangle_b_size_y = 10

    circle_a_position = Vector2(10, 10)
    circle_a_radius = 6
    circle_a_speed = Vector2(5, 5)

    circle_b_position = Vector2(150, 150)
    circle_b_radius = 10

    screen = pygame.display.set_mode(screen_res)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.sys.exit()

        pygame.draw.rect(screen, (0, 0, 0), ((0, 0), screen_res))
        clock.tick(30)

        x, y = pygame.mouse.get_pos()
        circle_a_position = Vector2(x, y)

        pygame.draw.rect(screen, (255, 255, 255),
                         (rectangle_a_position.x,
                         rectangle_a_position.y,
                         rectangle_a_size_x,
                         rectangle_a_size_y))

        pygame.draw.rect(screen, (255, 255, 255),
                         (rectangle_b_position.x,
                         rectangle_b_position.y,
                         rectangle_b_size_x,
                         rectangle_b_size_y))

        pygame.draw.circle(screen, (255, 255, 255),
                           (int(circle_b_position.x),
                           int(circle_b_position.y)),
                           circle_b_radius)

        pygame.draw.circle(screen, (255, 0, 0),
                           (int(circle_a_position.x),
                           int(circle_a_position.y)),
                           circle_a_radius)

        def draw_vec_from_ball(vec, col):
            """ Draw a vector from the mouse controlled circle. """
            pygame.draw.line(screen, col,
                             (circle_a_position.x, circle_a_position.y),
                             (circle_a_position.x + vec.x * 20,
                              circle_a_position.y + vec.y * 20), 3)

        draw_vec_from_ball(circle_a_speed, (255, 255, 0))

        impulse = intersect_rectangle_circle(rectangle_a_position,
                                             rectangle_a_size_x,
                                             rectangle_a_size_y,
                                             circle_a_position,
                                             circle_a_radius,
                                             circle_a_speed)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255, 255))

        impulse = intersect_rectangle_circle(rectangle_b_position,
                                             rectangle_b_size_x,
                                             rectangle_b_size_y,
                                             circle_a_position,
                                             circle_a_radius,
                                             circle_a_speed)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255, 255))

        impulse = intersect_circles(circle_a_position, circle_a_radius,
                                    circle_b_position, circle_b_radius)
        if impulse:
            draw_vec_from_ball(impulse, (0, 255, 255))

        pygame.display.update()


def example2():
    V1 = Vector2(300, 300)
    V2 = Vector2(100, 100)

    V3 = V1 + V2

    print(V3)


def create_font(text, font_family="Arial", size=48, color=(255, 255, 255), bold=False, italic=False):
    """ Hjelper-funksjon som lager et font-objekt med tilhørende 'bounding-box' """
    font = pygame.font.SysFont(font_family, size, bold, italic)
    text = font.render(text, False, color)
    text_rect = text.get_rect()
    return text, text_rect



def my_code():
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

    sprites.add(paddle)


    ball = Ball(WHITE, 16)
    sprites.add(ball)


    # Litt aritmetikk for å finne rett størrelse på mellomrommet mellom brikkene
    tiles_per_row = 8
    tile_width = 90
    tile_height = 20
    margin = (screen.get_width() - (tiles_per_row)*tile_width) / (tiles_per_row + 1)
    top_offset = 60

    n_rows = 2

    bricks = pygame.sprite.Group()
    
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


    playing = True

    clock = pygame.time.Clock()

    # `initial_open' er en variabel som tyder på om du nettopp åpnet spillet
    # denne brukes for å lage en liten "splash screen" før selve spillet starter
    initial_open = True

    while initial_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                initial_open = False
                playing = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            initial_open = False
            ball.rect.x = (screen.get_width() - 2*ball.radius) // 2
            ball.rect.y = paddle.rect.y - ball.radius
            ball.velocity = [randint(4, 8), randint(-8, 8)]


        screen.fill((0,0,0))    # Velger bakgrunnsfargen

        start_text, start_box = create_font("Press SPACE to start!", size=72, color=WHITE)
        sb_center_x, sb_center_y = screen.get_width() // 2, screen.get_height() //2
        start_box = start_text.get_rect(center=(sb_center_x, sb_center_y))
        screen.blit(start_text, start_box)


        """
        # Game over text, vertically and horizontally centered
        gameover_text, gameover_box = create_font("GAME OVER", "Arial", 128, RED)
        center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
        gameover_box = gameover_text.get_rect(center=(center_x, center_y))

        # Restart text, only horizontally centered, and biased to the bottom
        restart_text, restart_box = create_font("Press SPACE to restart")
        restart_box = int((screen.get_width() - restart_text.get_width()) // 2), screen.get_height() - restart_text.get_height()
        screen.blit(restart_text, restart_box)

        screen.blit(gameover_text, gameover_box)
        """

        pygame.display.flip()
        clock.tick(60)


    while playing:
        # Event handling
        # Den ene sjekker for om spilleren trykker på krysset i hjørnet
        # den andre sjekker for om spilleren trøkker Q-tasten
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False                 # Setter er flagg slik at vi kan hoppe ut av loopen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:     # Hvis Q-trykkes avsluttes spillet
                    playing = False

        # Flytter rekkerten med piltastene istedenfor musepekeren
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left(15)
        if keys[pygame.K_RIGHT]:
            paddle.move_right(15)

        brick_list = bricks.sprites()
        for brick in brick_list:
            # Sjekk for kollisjon mellom ball og brick
            impulse = intersect_rectangle_circle(Vector2(brick.rect.x, brick.rect.y), brick.rect.width, brick.rect.height, Vector2(ball.rect.x, ball.rect.y), ball.radius, Vector2(ball.velocity))
            if impulse:
                print("Ball has hit a brick!")
                ball.velocity[0] = impulse.x*10
                ball.velocity[1] = impulse.y*10
                #bricks.remove(brick)
                #sprites.remove(brick)
                brick.kill()            # Denne fjerner en brick fra sprites gruppa
                #bricks.update()        # Disse visste seg å være unødvendig
                #sprites.update()
                score += 1
        
        # Sjekk for kollisjon mellom ball og rekkert
        impulse = intersect_rectangle_circle(Vector2(paddle.rect.x, paddle.rect.y), paddle.rect.width, paddle.rect.height, Vector2(ball.rect.x, ball.rect.y), ball.radius, Vector2(ball.velocity))
        if impulse:
            print("Hit the paddle!")
            ball.velocity[0] = impulse.x*10
            ball.velocity[1] = impulse.y*10
        
        

        # Game logic
        sprites.update()

        # simpel kode for å snu retningen til ballen når den treffer en vegg
        if ball.rect.x >= screen.get_width() - 2*ball.radius:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y >= screen.get_height() - 2*ball.radius:
            ball.velocity[1] = -ball.velocity[1]
            lives -= 1                  # Dekrementer liv med 1 ved bunn-treff
        if ball.rect.y <= 0:
            ball.velocity[1] = -ball.velocity[1]
            # hvis du treffer taket har du vel vunnet, right? Break out?


        # Fyller skjermen med en heldekkende farge, klar til å tegnes på
        screen.fill(BLACK)

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



def game_over(screen):
    """
        docstring
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()                 # Setter er flagg slik at vi kan hoppe ut av loopen
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:     # Hvis Q-trykkes avsluttes spillet
                pygame.quit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # Restart the game
        pass

    # Game over text, vertically and horizontally centered
    gameover_text, gameover_box = create_font("GAME OVER", "Arial", 128, RED)
    center_x, center_y = screen.get_width() // 2, screen.get_height() // 2
    gameover_box = gameover_text.get_rect(center=(center_x, center_y))

    # Restart text, only horizontally centered, and biased to the bottom
    restart_text, restart_box = create_font("Press SPACE to restart")
    restart_box = int((screen.get_width() - restart_text.get_width()) // 2), screen.get_height() - restart_text.get_height()
    screen.blit(restart_text, restart_box)

    screen.blit(gameover_text, gameover_box)


if __name__ == '__main__':
    my_code()
    pygame.quit()
