from random import randint
from const import Const
from interstellar import Interstellar
import pygame


class Planet(Interstellar):
    def __init__(self, images, speed, x=0, y=0):
        super().__init__(images, speed, x, y)
        orig_width, orig_height = self.original_images.get_rect().size
        new_size = randint(Const.PLANET_MIN_SIZE, orig_width) / orig_width  # Assuming the planets are square images
        new_angle = randint(0, 179)
        self.image = pygame.transform.rotozoom(self.original_images, new_angle, new_size)
        self.width, self.height = self.image.get_rect().size

    def move(self):
        """
        Move the planet.
        """
        if not self.away:
            self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.speed)))
            if self.off_the_screen():
                self.away = True
        # Planets have no hitbox, so no need to call the super class method
