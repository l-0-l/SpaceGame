from random import randint
from const import Const
from interstellar import Interstellar
import pygame


class Planet(Interstellar):
    def __init__(self, image, speed, x=0, y=0):
        super().__init__(image, speed, x, y)
        orig_width, orig_height = self.original_image.get_rect().size
        new_size = randint(Const.PLANET_MIN_SIZE, orig_width) / orig_width # Assuming the planets are square images
        new_angle = randint(0, 179)
        self.image = pygame.transform.rotozoom(self.original_image, new_angle, new_size)
        self.width, self.height = self.image.get_rect().size

    def off_the_screen(self):
        if self.x > Const.SCREEN_WIDTH or self.y > Const.SCREEN_HEIGHT or \
                self.x + self.width < 0 or self.y + self.height < 0:
            return True
        else:
            return False

    def move(self):
        if not self.away:
            self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.speed)))
            if self.off_the_screen():
                self.away = True
