from interstellar import Interstellar
from const import Const
from random import randint
import enum


class Enemy(Interstellar):
    def __init__(self, images, speed, explode_images, explode_sounds, enemy_type, x=0, y=0, *groups):
        super().__init__(images, speed, x, y, *groups)
        self.explode_images = explode_images
        self.explode_sounds = explode_sounds
        self.type = enemy_type
        self.num_of_explosion_frames = len(self.explode_images) - 1
        self.num_of_explode_sounds = len(explode_sounds) - 1
        self.exploding = False

    class Type(enum.Enum):
        asteroid = 0
        invader = 1

    def get_type(self):
        """
        Returns the enemy type.
        """
        return self.type

    def is_hit(self):
        """
        Check whether the enemy is already hit.
        """
        return self.exploding

    def hit(self):
        """
        Cause the enemy to become hit.
        """
        self.exploding = True
        self.frame_num = 0
        self.frame_time = Const.EXPLOSION_ANIMATE_SPEED
        self.current_image_set = self.explode_images
        orig_width = self.width
        orig_height = self.height
        self.width, self.height = self.current_image_set[0].get_rect().size
        self.x = self.x - self.width // 2 + orig_width // 2
        self.y = self.y - self.height // 2 + orig_height // 2
        self.hitsize = (Const.EXPLOSION_HIT_DELTA, Const.EXPLOSION_HIT_DELTA,
                        self.width - Const.EXPLOSION_HIT_DELTA, self.height - Const.EXPLOSION_HIT_DELTA)
        sound = self.explode_sounds[randint(0, self.num_of_explode_sounds)]
        sound.play()
