from math import copysign
from random import randint
from const import Const
from interstellar import Interstellar
from time import clock
import pygame


class Asteroid(Interstellar):
    def __init__(self, images, explode_images, speed, acceleration, explode_sounds, x=0, y=0):
        super().__init__(images, speed, x, y)
        self.__set_asteroid_random_size()
        self.width, self.height = self.images[0].get_rect().size
        hitsize_delta = self.width // Const.ASTEROID_HITSIZE_COEFFICIENT
        self.hitsize = (hitsize_delta, hitsize_delta,
                        self.width - hitsize_delta * 2, self.height - hitsize_delta * 2)
        self.acceleration = acceleration
        # Animation speed is affected by the asteroid's vertical speed
        self.frame_time = (1 - self.speed[1] / Const.ASTEROID_SPEED_VERTICAL_MAX) / Const.ASTEROID_ANIMATE_COEFFICIENT
        self.next_frame = 0
        self.frame_num = 0
        self.exploding = False
        self.explode_images = explode_images
        self.num_of_images = len(self.images) - 1
        self.num_of_explosion_frames = len(self.explode_images) - 1
        self.current_image_set = self.images
        self.explode_sounds = explode_sounds
        self.num_of_explode_sounds = len(explode_sounds) - 1

    def __set_asteroid_random_size(self):
        orig_width, _ = self.original_images[0].get_rect().size
        # Alter the original size only if the current size is above the minimum
        if Const.ASTEROID_MIN_SIZE < orig_width:
            self.images = []
            new_size = randint(Const.ASTEROID_MIN_SIZE, orig_width)  # Assuming the asteroids are square images
            for image in self.original_images:
                self.images.append(pygame.transform.scale(image, (new_size, new_size)))

    def move(self):
        """
        Move the asteroid.
        """
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
            if self.exploding:
                if self.frame_num < self.num_of_explosion_frames:
                    self.frame_num += 1
                else:
                    self.away = True
            else:
                # Chose animation direction by the asteroid's horizontal direction
                self.frame_num += int(copysign(1, self.speed[0]+self.acceleration[0]))
                if self.frame_num > self.num_of_images:
                    self.frame_num = 0
                elif self.frame_num < 0:
                    self.frame_num = self.num_of_images
            self.next_frame = clock() + self.frame_time

        return self.current_image_set[self.frame_num]

    def is_hit(self):
        """
        Return whether the asteroid is already hit.
        """
        return self.exploding

    def hit(self):
        """
        Cause the asteroid to become hit.
        """
        self.exploding = True
        self.frame_num = 0
        self.frame_time = Const.ASTEROID_EXPLOSION_ANIMATE_SPEED
        self.current_image_set = self.explode_images
        orig_width = self.width
        orig_height = self.height
        self.width, self.height = self.current_image_set[0].get_rect().size
        self.x = self.x - self.width // 2 + orig_width // 2
        self.y = self.y - self.height // 2 + orig_height // 2
        self.hitsize = (Const.ASTEROID_EXPLOSION_HIT_DELTA,
                        Const.ASTEROID_EXPLOSION_HIT_DELTA,
                        self.width - Const.ASTEROID_EXPLOSION_HIT_DELTA*2,
                        self.height - Const.ASTEROID_EXPLOSION_HIT_DELTA*2)
        sound = self.explode_sounds[randint(0, self.num_of_explode_sounds)]
        sound.play()
