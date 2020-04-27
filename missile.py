from time import clock
from random import randint
from direction import Direction
from resources import Resources
from const import Const
from interstellar import Interstellar
import pygame


class Missile(Interstellar):
    def __init__(self, spaceship, side, enemies, launch_sound, game):
        super().__init__(Resources.missile, speed=0, x=0, y=0)
        self.spaceship = spaceship
        self.speed = (0, Const.MISSILE_INITIAL_SPEED)
        self.width, self.height = self.images[0].get_rect().size
        self.hitsize = (0, 0, self.width, self.height - Const.MISSILE_FLAME_SIZE)
        self.away = False
        self.next_frame = 0
        self.current_pic_num = 0
        self.on_board = True
        self.side = side
        self.enemies = enemies
        self.launch_sound = launch_sound[0]
        self.x = 0
        self.y = 0
        self.game = game

    def move(self):
        """
        If the missile is on board, it will be moving with the spaceship
        on the x axis, and when fired - it will move on the y axis
        """
        if self.on_board:
            # The missile is on board
            self.x, self.y = self.spaceship.get_xy()
            if self.side == Direction.left:
                self.x += Const.MISSILE_STOWED_OFFSET_X_LEFT
            else:
                self.x += Const.MISSILE_STOWED_OFFSET_X_RIGHT
            self.y += Const.MISSILE_STOWED_OFFSET_Y
            self.speed = (self.spaceship.get_horizontal_speed() / Const.MISSILE_HORIZONTAL_SPEED_DELTA, 0)
        else:
            # The missile is on its way to the target
            if self.y > Const.OFF_THE_SCREEN_TOP:
                self.speed = tuple(map(sum, zip((0, Const.MISSILE_ACCELERATION), self.speed)))
                self.y -= self.speed[1]
                self.x += self.speed[0]
            else:
                self.away = True
        super().move()

        # Check if we collide into anything
        for enemy in self.enemies.get_enemies():
            if not self.on_board and pygame.Rect(self.hitbox).colliderect(enemy.hitbox):
                self.away = True
                enemy.hit()
                self.game.add_score(enemy)

    def get_current_pic(self):
        """
        Return the current missile image
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

    @staticmethod
    def rotate(image, angle):
        """
        Rotate an image while keeping its center and size
        """
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def launch(self):
        """
        Launch the missile - means detach it from the spaceship
        """
        if self.on_board:
            # Set the missile angle
            angle = -self.speed[0]*3
            if abs(angle) > 1:
                self.images = []
                for image in self.original_images:
                    self.images.append(Missile.rotate(image, angle))
            self.on_board = False
            self.launch_sound.play()

    def reload(self):
        """
        Reset the missile status, and attach it back to the spaceship
        """
        self.on_board = True
        self.away = False
        self.images = self.original_images
        self.speed = (0, Const.MISSILE_INITIAL_SPEED)

    def draw(self):
        """
        Draw the missile
        """
        self.spaceship.screen.window.blit(self.get_current_pic(), self.get_xy())
        if Const.DEBUG:
            pygame.draw.rect(self.spaceship.screen.window, (255, 0, 0), self.hitbox, 1)
