from time import clock
from random import randint
from direction import Direction


class Missile:
    def __init__(self, player, speed, acceleration, pic, frame_time, side):
        self.player = player
        self.speed = speed
        self.given_speed = self.speed
        self.acceleration = acceleration
        self.pic = pic
        self.width, self.height = pic[0].get_rect().size
        self.away = False
        self.frame_time = frame_time
        self.next_frame = clock() + self.frame_time
        self.current_pic = 0
        self.on_board = True
        self.side = side
        self.x = 0
        self.y = 0

    def move(self):
        """
        If the missile is on board, it will be moving with the player
        on the x axis, and when fired - it will move on the y axis.
        """
        if self.on_board:
            # The missile is on board
            self.x, self.y = self.player.get_xy()
            if self.side == Direction.left:
                self.x += 18  # TODO: Magic number here
            else:
                self.x += 48  # TODO: Magic number here
            self.y += 27  # TODO: Magic number here
        else:
            # The missile is on its way to the target
            if self.y > -self.height:
                self.speed += self.acceleration
                self.y -= self.speed
            else:
                self.away = True

    def get_xy(self):
        """
        Returns the position.
        """
        return self.x, self.y

    def get_current_pic(self):
        """
        Returns the current missile image.
        """
        if self.on_board:
            # The picture is static
            pic = self.pic[0]
        else:
            # Change the picture
            if clock() > self.next_frame:
                # Make sure we're not randomly getting the same picture
                previous_number = self.current_pic
                while previous_number == self.current_pic:
                    self.current_pic = randint(1, len(self.pic) - 1)
                self.next_frame += self.frame_time
            pic = self.pic[self.current_pic]
        return pic

    def launch(self):
        """
        Launch the missile - means detach from player.
        """
        self.on_board = False

    def is_away(self):
        """
        Returns the away status, i.e. when the missile is off the screen.
        """
        if self.away:
            return True
        else:
            return False

    def reload(self):
        """
        Reset the missile status, and attach it back to the player.
        """
        self.on_board = True
        self.away = False
        self.speed = self.given_speed

    def draw(self):
        """
        Draw the missile.
        """
        self.player.screen.window.blit(self.get_current_pic(), self.get_xy())
