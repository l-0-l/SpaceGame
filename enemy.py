from interstellar import Interstellar
from direction import Direction
from resources import Resources

import enum


class Enemy(Interstellar):
    def __init__(self,
                 images,
                 speed,
                 explode_images=Resources.explosion,
                 explode_sounds=Resources.wav_explosion,
                 x=0, y=0):
        super().__init__(images=images,
                         speed=speed,
                         explode_images=explode_images,
                         explode_sounds=explode_sounds,
                         x=x, y=y)
        self.score = 0

    class Type(enum.Enum):
        asteroid = 0
        invader = 1

    def get_score(self):
        """
        Return the score of this enemy
        """
        return self.score

    def set_speed(self, speed):
        """
        Set enemy's speed (given as a tuple of horizontal and vertical speeds)
        """
        self.speed = speed

    def get_horizontal_direction(self):
        """
        Returns the horizontal direction of the enemy
        """
        if self.speed[0] > 0:
            return Direction.right
        elif self.speed[0] < 0:
            return Direction.left
        else:
            return Direction.none

    def move(self):
        if not self.away:
            self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.speed)))
            if self.off_the_screen():
                self.away = True
        super().move()
