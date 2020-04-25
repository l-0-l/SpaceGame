from asteroid import Asteroid
from invader import Invader
from random import randint, uniform
from const import Const
from resources import Resources
from direction import Direction
import pygame


class Enemies:
    def __init__(self, screen):
        self.screen = screen
        self.asteroids = []
        self.invaders = []

    def get_enemies(self):
        """
        Return all enemies
        """
        return self.asteroids + self.invaders

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

    def add_invader(self, x, y, speed, direction):
        invader = Invader(images=Resources.invader1,
                          explode_images=Resources.explosion,
                          explode_sounds=Resources.wav_explosion,
                          x=x, y=y,
                          direction=direction,
                          speed=speed)
        self.invaders.append(invader)

    def set_invaders_speed(self, speed):
        for invader in self.invaders:
            invader.set_speed(speed)

    def all_invaders_appeared(self):
        for invader in self.invaders:
            if invader.get_xy()[0] < 0 or invader.get_xy()[1] < 0:
                return False
        return True

    def current_number_of_invaders(self):
        return len(self.invaders)

    def move(self):
        """
        Moves all existing enemies.
        """
        enemies = self.asteroids + self.invaders
        to_remove = []
        # Move all the enemies
        for enemy in enemies:
            enemy.move()
            if enemy.is_away():
                to_remove.append(enemy)
            # This will blow up other enemies within reach
            if enemy.is_hit():
                for other_enemy in enemies:
                    if not other_enemy.is_hit() and enemy.hitbox.colliderect(other_enemy.hitbox):
                        other_enemy.hit()
        # If some enemies have moved away from the screen, they must be removed
        for enemy in to_remove:
            if enemy in self.asteroids:
                self.asteroids.remove(enemy)
            elif enemy in self.invaders:
                self.invaders.remove(enemy)

    def draw(self):
        """
        Draws all existing enemies.
        """
        for asteroid in self.asteroids:
            self.screen.window.blit(asteroid.get_current_pic(), asteroid.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.screen.window, (255, 255, 0), asteroid.get_hitbox(), 1)
        for invader in self.invaders:
            self.screen.window.blit(invader.get_current_pic(), invader.get_xy())
            if Const.DEBUG:
                pygame.draw.rect(self.screen.window, (255, 0, 0), invader.get_hitbox(), 1)
