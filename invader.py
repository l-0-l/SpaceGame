from enemy import Enemy
from time import clock
from const import Const


class Invader(Enemy):
    def __init__(self, images, explode_images, explode_sounds, x, y,
                 descend_speed, horizontal_speed, descend_steps):
        super().__init__(images, (0, 0), explode_images, explode_sounds, x=x, y=y)
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
        self.hitsize = tuple(map(sum, zip((0, 0, self.width, self.height), Const.INVADER_HITSIZE)))
        self.descend_steps = descend_steps
        self.descend_step = 0
        self.descend_speed = descend_speed
        self.move_aside_step = 0
        self.horizontal_speed = horizontal_speed
        self.descend_finished = False
        self.entry_finished = False
        self.speed = (0, Const.INVADER_ENTRY_SPEED)
        self.allow_off_the_screen = True

    def set_speed(self, speed):
        self.speed = speed

    def move_aside(self, direction):
        self.move_aside_step = 0
        self.speed = (self.horizontal_speed * direction.value, 0)

    def swap_direction(self):
        self.horizontal_speed = -self.horizontal_speed

    def descend(self):
        self.descend_step = 0
        self.descend_finished = False
        self.speed = (0, self.descend_speed)

    def get_descend_finished(self):
        return self.descend_finished

    def arrived(self, direction):
        self.entry_finished = True
        self.allow_off_the_screen = False
        self.move_aside(direction)

    def move(self):
        if self.entry_finished:
            if not self.descend_finished:
                self.descend_step += 1
                if self.descend_step >= self.descend_steps:
                    self.descend_finished = True
                    self.speed = (self.horizontal_speed, 0)
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
