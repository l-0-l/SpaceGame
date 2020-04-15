from asteroid import Asteroid
from invader import Invader
from random import randint, uniform
from const import Const
from resources import Resources
from direction import Direction
import pygame


class Enemy:
    def __init__(self, screen):
        self.screen = screen
        self.asteroids = []
        self.invaders = []

    def add_asteroid(self):
        """
        Adds a new asteroid with random values.
        """
        speed_vertical = uniform(Const.ASTEROID_SPEED_VERTICAL_MIN, Const.ASTEROID_SPEED_VERTICAL_MAX)
        speed_horizontal = uniform(Const.ASTEROID_SPEED_HORIZONTAL_MIN, Const.ASTEROID_SPEED_HORIZONTAL_MAX)
        acc_vertical = uniform(Const.ASTEROID_ACCELERATION_VERTICAL_MIN, Const.ASTEROID_ACCELERATION_VERTICAL_MAX)
        acc_horizontal = uniform(Const.ASTEROID_ACCELERATION_HORIZONTAL_MIN, Const.ASTEROID_ACCELERATION_HORIZONTAL_MAX)
        asteroid = Asteroid(
            images=Resources.asteroid1,
            explode_images=Resources.explosion,
            speed=(speed_horizontal, speed_vertical),
            acceleration=(acc_horizontal, acc_vertical),
            explode_sounds=Resources.wav_explosion
        )
        x = randint(Const.ASTEROID_BORDER_LEFT, Const.ASTEROID_BORDER_RIGHT - asteroid.get_width())
        y = Const.ASTEROID_APPEAR_HEIGHT
        asteroid.set_xy(x, y)
        self.asteroids.append(asteroid)

    def add_invader(self):
        invader = Invader(images=Resources.invader1,
                          explode_images=Resources.explosion,
                          explode_sounds=Resources.wav_explosion,
                          x=550, y=100,
                          direction=Direction.right,
                          speed=(1, 0))
        self.invaders.append(invader)

    def move(self):
        """
        Moves all existing enemies.
        """
        to_remove = []
        # Move all the asteroids
        for asteroid in self.asteroids:
            asteroid.move()
            if asteroid.is_away():
                to_remove.append(asteroid)
            # This will blow up other asteroids within reach
            if asteroid.is_hit():
                for other_asteroid in self.asteroids:
                    if not other_asteroid.is_hit() and asteroid.hitbox.colliderect(other_asteroid.hitbox):
                        other_asteroid.hit()
        # If some asteroids have moved away from the screen, they must be removed
        for asteroid in to_remove:
            self.asteroids.remove(asteroid)

        to_remove = []
        # Move all invaders
        for invader in self.invaders:
            invader.move()
            if invader.is_away():
                to_remove.append(invader)
        # If some invaders have moved away from the screen, they must be removed
        for invader in to_remove:
            self.invaders.remove(invader)

    def draw(self):
        """
        Draws all existing enemies.
        """
        for asteroid in self.asteroids:
            self.screen.window.blit(asteroid.get_current_pic(), asteroid.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.screen.window, (255, 0, 0), asteroid.get_hitbox(), 1)
        for invader in self.invaders:
            self.screen.window.blit(invader.get_current_pic(), invader.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.screen.window, (255, 0, 0), invader.get_hitbox(), 1)
