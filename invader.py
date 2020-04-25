from enemy import Enemy
from time import clock
from const import Const
from direction import Direction
import math


class Invader(Enemy):
    def __init__(self, images, explode_images, explode_sounds, x, y, direction, speed):
        super().__init__(images, (0, 0), explode_images, explode_sounds, Enemy.Type.invader, x=0, y=0)
        self.speed = speed
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
        self.frame_time = Const.EXPLOSION_ANIMATE_SPEED
        self.images = self.rescale(images_source=self.original_images,
                                   scale_x=Const.INVADER_SIZE,
                                   scale_y=Const.INVADER_SIZE)  # Square invader
        self.current_image_set = self.images
        self.width, self.height = self.images[0].get_rect().size
        self.hitsize = tuple(map(sum, zip((0, 0, self.width, self.height, 0, 0), Const.INVADER_HITSIZE)))
        self.direction = direction
        self.move_down_track = []
        self.move_down_step = 0
        self.entry_finished = False

    def get_direction(self):
        return self.direction

    def set_speed(self, speed):
        self.speed = speed

    def __calculate_curve(self):
        self.move_down_track = []
        n = Const.INVADER_CURVE * math.pi / 2  # Half a circumference
        if self.x > Const.SCREEN_WIDTH // 2:
            sign = -1
        else:
            sign = 1
        i = 0
        while i < int(n // 2 + 1):
            x = self.x + (math.cos(2 * math.pi / n * i + sign * math.pi / 2) * (n / 2))
            y = self.y + n // 2 + (math.sin(2 * math.pi / n * i + sign * math.pi / 2) * (n / 2))
            self.move_down_track.append((int(x), int(y)))
            i += self.speed[0]
        if sign > 0:
            self.move_down_track.reverse()

    def set_direction(self, direction):
        if direction != self.direction:
            if direction == Direction.left or direction == Direction.right:
                self.direction = direction
            elif direction == Direction.down:
                self.direction = direction
                self.move_down_step = 0
                self.__calculate_curve()

    def move(self):
        if self.direction == Direction.left or self.direction == Direction.right:
            self.x += self.speed[0] * self.direction.value
            if self.x >= Const.INVADER_RIGHT_BORDER and self.direction == Direction.right or \
                    self.x <= Const.INVADER_LEFT_BORDER and self.direction == Direction.left:
                if not self.entry_finished:
                    self.set_direction(Direction.down)
        elif self.direction == Direction.down:
            self.move_down_step += 1
            if self.move_down_step > len(self.move_down_track) - 1:
                if self.x - self.width // 2 > Const.SCREEN_WIDTH // 2:
                    self.set_direction(Direction.left)
                else:
                    self.set_direction(Direction.right)
            else:
                self.x, self.y = self.move_down_track[self.move_down_step]
        super().move()

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
