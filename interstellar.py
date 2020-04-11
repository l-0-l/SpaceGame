import pygame


class Interstellar(pygame.sprite.Sprite):
    def __init__(self, image, speed, x=0, y=0, *groups):
        super().__init__(*groups)
        self.original_image = image
        self.image = self.original_image
        self.speed = speed
        self.x = x
        self.y = y
        self.away = False

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
        Move the object. <Requires override>
        """
        pass

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
