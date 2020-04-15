from time import clock
from random import randint
from direction import Direction
from resources import Resources
from const import Const
from interstellar import Interstellar
import pygame


class Missile(Interstellar):
    def __init__(self, player, side, enemy, launch_sound):
        super().__init__(Resources.missile, speed=0, x=0, y=0)
        self.player = player
        self.speed = (0, Const.MISSILE_INITIAL_SPEED)
        self.width, self.height = self.images[0].get_rect().size
        self.hitsize = pygame.Rect(0, 0, self.width, self.height - Const.MISSILE_FLAME_SIZE)
        self.away = False
        self.next_frame = 0
        self.current_pic_num = 0
        self.on_board = True
        self.side = side
        self.enemy = enemy
        self.launch_sound = launch_sound[0]
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
            if self.y > Const.OFF_THE_SCREEN_TOP:
                self.speed = tuple(map(sum, zip((0, Const.MISSILE_ACCELERATION), self.speed)))
                self.y -= self.speed[1]
            else:
                self.away = True
        super().move()

        # Check if we collide into anything
        for asteroid in self.enemy.asteroids:
            if not self.on_board and self.hitbox.colliderect(asteroid.hitbox):
                self.away = True
                asteroid.hit()

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
                    self.current_pic_num = randint(1, len(self.images) - 1)
                self.next_frame = clock() + Const.FRAME_TIME_SEC
        return self.images[self.current_pic_num]

    def launch(self):
        """
        Launches the missile - means detach it from player.
        """
        if self.on_board:
            self.on_board = False
            self.launch_sound.play()

    def reload(self):
        """
        Resets the missile status, and attach it back to the player.
        """
        self.on_board = True
        self.away = False
        self.speed = (0, Const.MISSILE_INITIAL_SPEED)

    def draw(self):
        """
        Draws the missile.
        """
        self.player.screen.window.blit(self.get_current_pic(), self.get_xy())
        if Const.DEBUG:
            pygame.draw.rect(self.player.screen.window, (255, 0, 0), self.hitbox, 1)
