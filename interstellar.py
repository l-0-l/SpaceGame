import pygame
from const import Const


class Interstellar(pygame.sprite.Sprite):
    def __init__(self, images, speed, x=0, y=0, *groups):
        super().__init__(*groups)
        self.original_images = images
        self.images = self.original_images
        self.speed = speed
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.away = False
        self.hitbox = (0, 0, 0, 0)
        self.hitsize = (0, 0, 0, 0)
        if self.images:
            self.num_of_images = len(self.images)
        else:
            self.num_of_images = 0
        self.frame_time = Const.FRAME_TIME_SEC
        self.next_frame = 0
        self.frame_num = 0
        self.current_image_set = self.images

    def get_xy(self):
        """
        Returns the position.
        """
        return self.x, self.y

    def get_hitbox(self):
        """
        Returns the hitbox.
        """
        return self.hitbox

    def set_xy(self, x, y):
        """
        Sets the position.
        """
        self.x = x
        self.y = y

    def move(self):
        """
        Move the object.
        """
        self.hitbox = pygame.Rect(tuple(map(sum, zip((self.x, self.y, -self.hitsize[0], -self.hitsize[1]),
                                                     self.hitsize))))

    def get_current_pic(self):
        """
        Return the current picture.
        """
        return self.images[self.frame_num]

    def is_away(self):
        """
        Return true if the object is off the screen.
        """
        return self.away

    def get_width(self):
        """
        Return object's width.
        """
        return self.width

    def get_height(self):
        """
        Return object's height.
        """
        return self.height

    @staticmethod
    def rescale(images_source, scale_x, scale_y):
        """
        Rescale images
        """
        images_target = []
        for image in images_source:
            images_target.append(pygame.transform.scale(image, (scale_x, scale_y)))
        return images_target

    def off_the_screen(self):
        """
        Return true if the asteroid has vanished from the screen
        """
        if self.x > Const.OFF_THE_SCREEN_RIGHT or self.y > Const.OFF_THE_SCREEN_BOTTOM or \
                self.x + self.width < Const.OFF_THE_SCREEN_LEFT or self.y + self.height < Const.OFF_THE_SCREEN_TOP:
            return True
        else:
            return False
