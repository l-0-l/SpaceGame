from random import randint
from const import Const
from interstellar import Interstellar
import pygame


class Planet(Interstellar):
    """
    A planet is just there for the background. It has no hitsize, and therefore is completely passive.
    """
    def __init__(self, images, speed, x=0, y=0):
        super().__init__(images=images, speed=speed, x=x, y=y)
        orig_width, orig_height = self.original_images[0].get_rect().size
        new_size = randint(Const.PLANET_MIN_SIZE, orig_width) / orig_width  # Assuming the planets are square images
        new_angle = randint(0, 179)
        self.images = [pygame.transform.rotozoom(self.original_images[0], new_angle, new_size)]
        self.width, self.height = self.images[0].get_rect().size
