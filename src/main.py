#!/usr/bin/env python

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

import pygame
import os

from pygame import Vector2
from pygame.draw import rect

from paddle import Paddle   # Rekkerten


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
    rectangle_a_size_x = rectangle_a_size_y = 20

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
    """This is a docstring"""
    V1 = Vector2(300, 300)
    V2 = Vector2(100, 100)

    V3 = V1 + V2

    print(V3)

class Brick:
    """ The Brick class, a class that defines bricks """
    brick_width  = 60
    brick_height = 20
    def __init__(self, color):
        self.color = color
    
    def create(self, color):
        pass

    def destroy(self):
        pass # Brick is kill


def my_code():
    """This is a docstring"""

    pygame.init()

    # Defining some beatuiful colors
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    REBECCAPURPLE = (102, 51, 153)

    score = 0
    lives = 3

    # Setting up the game window
    screen_res = (800, 600)
    screen = pygame.display.set_mode(screen_res)
    pygame.display.set_caption("The amazing Breakout clone by Robin Kristiansen (c) 2021")

    sprites = pygame.sprite.Group()


    #brick = Brick(RED)
    #brick.create(GREEN)

    paddle = Paddle(WHITE, 60, 20)
    paddle.rect.x = 350
    paddle.rect.y = 560

    sprites.add(paddle)

    playing = True

    clock = pygame.time.Clock()
    
    initial_open = True

    while initial_open:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                initial_open = False
                playing = False

        # Display some sort of waiting start screen
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            initial_open = False
            
        
        screen.fill((0,0,0))
        
        font = pygame.font.Font(None, 72)
        text = font.render("Press Space to start!", 1, WHITE)
        screen.blit(text, (150, 300))

        pygame.display.flip()
        clock.tick(60)

    while playing:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False             # Setter er flagg slik at vi kan hoppe ut av loopen
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    playing = False         # -||-

        # Flytter rekkerten med piltastene istedenfor musepekeren        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move_left(10)
        if keys[pygame.K_RIGHT]:
            paddle.move_right(10)

        # Game logic
        sprites.update()
        

        # Fyller skjermen med en heldekkende farge, klar til å tegnes på
        screen.fill(REBECCAPURPLE)
        
        # Linjen øverst på skjermen som viser poengsum og antall liv igjen
        pygame.draw.line(screen, WHITE, [0, 38], [800, 38], 2)

        # Render'er ovennevnte poeng og liv, ved hjelp av blit'ing
        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(score), 1, WHITE)
        screen.blit(text, (20, 10))
        text = font.render("Lives: " + str(lives), 1, WHITE)
        screen.blit(text, (650, 10))
        
        sprites.draw(screen)        # Tegner alle sprites på skjermen


        # Denne koden styrer paddelen med musa
        #mouse_x, mouse_y = pygame.mouse.get_pos()
        #pygame.draw.rect(screen, (255, 255, 255), ((mouse_x - 30, 480 - 24), (60, 20)))

        # Mens den andre koden styrer paddelen med høyre/venstre piltast


        pygame.display.flip()

        # Setting the tickrate
        clock.tick(60)
        
if __name__ == '__main__':
    my_code()
    pygame.quit()
