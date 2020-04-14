import pygame


class Interstellar(pygame.sprite.Sprite):
    def __init__(self, image, speed, x=0, y=0, *groups):
        super().__init__(*groups)
        self.original_image = image
        self.image = self.original_image
        self.speed = speed
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.away = False
        self.hitbox = (0, 0, 0, 0)
        self.hitsize = (0, 0, 0, 0)

    def get_xy(self):
        """
        Returns the position.
        """
        return self.x, self.y

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
        self.hitbox = tuple(map(sum, zip((self.x, self.y, 0, 0), self.hitsize)))

    def get_current_pic(self):
        """
        Return the current picture.
        """
        return self.image

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
