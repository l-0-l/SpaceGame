from time import clock
from random import randint
from direction import Direction
from images import Images
from const import Const


class Missile:
    def __init__(self, player, side):
        self.player = player
        self.speed = Const.MISSILE_INITIAL_SPEED
        self.width, self.height = Images.pic_missile[0].get_rect().size
        self.away = False
        self.next_frame = clock() + Const.FRAME_TIME
        self.current_pic_num = 0
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
                self.x += Const.MISSILE_STOWED_OFFSET_X_LEFT
            else:
                self.x += Const.MISSILE_STOWED_OFFSET_X_RIGHT
            self.y += Const.MISSILE_STOWED_OFFSET_Y
        else:
            # The missile is on its way to the target
            if self.y > -self.height:
                self.speed += Const.MISSILE_ACCELERATION
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
            # The picture is static, without flame
            self.current_pic_num = 0
        else:
            # Change the picture
            if clock() > self.next_frame:
                # Make sure we're not randomly getting the same picture
                previous_number = self.current_pic_num
                while previous_number == self.current_pic_num:
                    self.current_pic_num = randint(1, len(Images.pic_missile) - 1)
                self.next_frame += Const.FRAME_TIME
        return Images.pic_missile[self.current_pic_num]

    def launch(self):
        """
        Launches the missile - means detach it from player.
        """
        self.on_board = False

    def is_away(self):
        """
        Returns the away status, i.e. when the missile is off the screen.
        """
        return self.away

    def reload(self):
        """
        Resets the missile status, and attach it back to the player.
        """
        self.on_board = True
        self.away = False
        self.speed = Const.MISSILE_INITIAL_SPEED

    def draw(self):
        """
        Draws the missile.
        """
        self.player.screen.window.blit(self.get_current_pic(), self.get_xy())
