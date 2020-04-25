from math import copysign
from random import randint
from const import Const
from enemy import Enemy
from time import clock


class Asteroid(Enemy):
    def __init__(self, images, explode_images, speed, acceleration, explode_sounds, x=0, y=0):
        super().__init__(images, speed, explode_images, explode_sounds, x, y)
        self.__set_asteroid_random_size()
        self.current_image_set = self.images
        self.width, self.height = self.images[0].get_rect().size
        hitsize_delta = self.width // Const.ASTEROID_HITSIZE_COEFFICIENT
        self.hitsize = (hitsize_delta, hitsize_delta,
                        self.width - hitsize_delta, self.height - hitsize_delta)
        self.acceleration = acceleration
        self.score = int(self.original_images[0].get_rect().size[0] - self.width) * 10  # More score for small ones
        # Animation speed is affected by the asteroid's vertical speed
        self.frame_time = (1 - self.speed[1] / Const.ASTEROID_SPEED_VERTICAL_MAX) / Const.ASTEROID_ANIMATE_COEFFICIENT

    def __set_asteroid_random_size(self):
        """
        Asteroids are being created with random sizes, which means we need to resize all asteroid images
        """
        orig_width, _ = self.original_images[0].get_rect().size
        # Alter the original size only if the current size is above the minimum
        if Const.ASTEROID_MIN_SIZE < orig_width:
            new_size = randint(Const.ASTEROID_MIN_SIZE, orig_width)  # Assuming the asteroids are square images
            self.images = self.rescale(images_source=self.original_images, scale_x=new_size, scale_y=new_size)

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
                if self.frame_num >= self.num_of_images:
                    self.frame_num = 0
                elif self.frame_num < 0:
                    self.frame_num = self.num_of_images - 1
            self.next_frame = clock() + self.frame_time
        return self.current_image_set[self.frame_num]
