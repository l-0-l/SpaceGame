from math import copysign
from random import randint
from const import Const
from interstellar import Interstellar
from time import clock
import pygame


class Asteroid(Interstellar):
    def __init__(self, image, speed, acceleration, x=0, y=0):
        super().__init__(image, speed, x, y)

        orig_width, orig_height = self.original_image[0].get_rect().size

        # Alter the original size only if the current size is above the minimum
        if Const.ASTEROID_MIN_SIZE < orig_width:
            self.image = []
            new_size = randint(Const.ASTEROID_MIN_SIZE, orig_width)  # Assuming the asteroids are square images
            for image in self.original_image:
                self.image.append(pygame.transform.scale(image, (new_size, new_size)))

        self.width, self.height = self.image[0].get_rect().size
        self.hitsize = (self.width//9, self.height//9, self.width-self.width//9, self.height-self.height//9)
        self.acceleration = acceleration
        self.frame_time = (1 - self.speed[1] / Const.ASTEROID_SPEED_VERTICAL_MAX) / Const.ASTEROID_ROTATION_COEFFICIENT
        self.next_frame = 0
        self.frame_num = 0
        self.num_of_images = len(self.image)

    def off_the_screen(self):
        if self.x > Const.SCREEN_WIDTH or self.y > Const.SCREEN_HEIGHT or \
                self.x + self.width < 0 or self.y + self.height < Const.ASTEROID_APPEAR_HEIGHT:
            return True
        else:
            return False

    def move(self):
        if not self.away:
            self.x, self.y = tuple(map(sum, zip((self.x, self.y), self.speed)))
            if self.off_the_screen():
                self.away = True
        super().move()

    def get_current_pic(self):
        """
        Return the current picture.
        """
        # Change the picture
        if clock() > self.next_frame:
            # Chose animation direction by the asteroid's horizontal direction
            self.frame_num += int(copysign(1, self.speed[0]+self.acceleration[0]))
            if self.frame_num >= self.num_of_images:
                self.frame_num = 0
            elif self.frame_num < 0:
                self.frame_num = self.num_of_images - 1
            self.next_frame = clock() + self.frame_time
        return self.image[self.frame_num]
