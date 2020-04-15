from interstellar import Interstellar
from time import clock
from const import Const
import pygame


class Invader(Interstellar):
    def __init__(self, images, explode_images, explode_sounds, x, y):
        super().__init__(images, speed=(0, 0), x=0, y=0)
        self.x = x
        self.y = y
        self.num_of_images = len(self.images) - 1
        self.next_frame = 0
        self.frame_num = 0
        self.frame_direction = 1
        self.exploding = False
        self.explode_images = explode_images
        self.num_of_explosion_frames = len(self.explode_images) - 1
        self.explode_sounds = explode_sounds
        self.num_of_explode_sounds = len(explode_sounds) - 1
        self.frame_time = Const.ASTEROID_EXPLOSION_ANIMATE_SPEED
        self.__resize_invaders()
        self.current_image_set = self.images
        self.width, self.height = self.images[0].get_rect().size
        print(self.width, self.height)
        self.hitsize = tuple(map(sum, zip((0, 0, self.width, self.height, 0, 0), Const.INVADER_HITSIZE)))

    def __resize_invaders(self):
        self.images = []
        for image in self.original_images:
            self.images.append(pygame.transform.scale(image, (Const.INVADER_SIZE, Const.INVADER_SIZE)))

    def move(self):
        super().move()
        pass

    def get_current_pic(self):
        if clock() > self.next_frame:
            if self.exploding:
                if self.frame_num < self.num_of_explosion_frames:
                    self.frame_num += 1
                else:
                    self.away = True
            else:
                self.frame_num += self.frame_direction
                if self.frame_num > self.num_of_images:
                    self.frame_direction = - self.frame_direction
                    # The last frame will be shown twice, for showing it once multiply the direction by 2 below.
                    self.frame_num += self.frame_direction
                elif self.frame_num < 0:
                    self.frame_direction = - self.frame_direction
                    # The first frame will be shown twice, for showing it once multiply the direction by 2 below.
                    self.frame_num += self.frame_direction
            self.next_frame = clock() + self.frame_time
        return self.current_image_set[self.frame_num]
