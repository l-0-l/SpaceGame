from direction import Direction
from screen import Screen
from player import Player
from missile import Missile
import pygame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BG_COLOR = (0, 128, 128)
PLAYER_ACCELERATION = 0.5
MAX_PLAYER_SPEED = 20
FRAME_TIME = 0.05
MISSILE_SPEED = 0.1
MISSILE_ACCELERATION = 0.3


pic_move_right = [pygame.image.load("res/spaceship_N_00.png"),
                  pygame.image.load("res/spaceship_R_01.png"),
                  pygame.image.load("res/spaceship_R_02.png"),
                  pygame.image.load("res/spaceship_R_03.png"),
                  pygame.image.load("res/spaceship_R_04.png"),
                  pygame.image.load("res/spaceship_R_05.png"),
                  pygame.image.load("res/spaceship_R_06.png")]

pic_move_left = [pygame.image.load("res/spaceship_N_00.png"),
                 pygame.image.load("res/spaceship_L_01.png"),
                 pygame.image.load("res/spaceship_L_02.png"),
                 pygame.image.load("res/spaceship_L_03.png"),
                 pygame.image.load("res/spaceship_L_04.png"),
                 pygame.image.load("res/spaceship_L_05.png"),
                 pygame.image.load("res/spaceship_L_06.png")]

pic_missile = [pygame.image.load("res/missile_00.png"),
               pygame.image.load("res/missile_01.png"),
               pygame.image.load("res/missile_02.png"),
               pygame.image.load("res/missile_03.png"),
               pygame.image.load("res/missile_04.png"),
               pygame.image.load("res/missile_05.png")]

pic_flame = [pygame.image.load("res/flame_01.png"),
             pygame.image.load("res/flame_02.png"),
             pygame.image.load("res/flame_03.png"),
             pygame.image.load("res/flame_04.png"),
             pygame.image.load("res/flame_05.png")]


class Space(object):
    def __init__(self):
        # Initialization
        pygame.init()
        self.screen = Screen(width=WINDOW_WIDTH,
                             height=WINDOW_HEIGHT,
                             bg_color=BG_COLOR)
        self.player = Player(x=self.screen.width/2,
                             y=self.screen.height-self.screen.height/10,
                             screen=self.screen,
                             acceleration=PLAYER_ACCELERATION,
                             max_speed=MAX_PLAYER_SPEED,
                             pic_move_right=pic_move_right,
                             pic_move_left=pic_move_left,
                             pic_flame=pic_flame,
                             frame_time=FRAME_TIME)
        self.missile_left = Missile(player=self.player,
                                    speed=MISSILE_SPEED,
                                    acceleration=MISSILE_ACCELERATION,
                                    pic=pic_missile,
                                    frame_time=FRAME_TIME,
                                    side=Direction.left)
        self.missile_right = Missile(player=self.player,
                                     speed=MISSILE_SPEED,
                                     acceleration=MISSILE_ACCELERATION,
                                     pic=pic_missile,
                                     frame_time=FRAME_TIME,
                                     side=Direction.right)

        # Caption and icon
        pygame.display.set_caption("Space")
        pic_logo = pygame.image.load("res/spaceship_N_00.png")
        pygame.display.set_icon(pic_logo)

        # Begin running :)
        self.running = True

    def main(self):
        """ Main game loop """

        while self.running:

            # Check for events
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    self.running = False
                # Respond to keys
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player.set_direction(Direction.left)
                    if event.key == pygame.K_RIGHT:
                        self.player.set_direction(Direction.right)
                    if event.key == pygame.K_z:
                        self.missile_left.launch()
                    if event.key == pygame.K_x:
                        self.missile_right.launch()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        # Check the direction change is relevant
                        if self.player.get_direction() == Direction.left:
                            self.player.set_direction(Direction.none)
                    elif event.key == pygame.K_RIGHT:
                        # Check the direction change is relevant
                        if self.player.get_direction() == Direction.right:
                            self.player.set_direction(Direction.none)

            # Calculate the next player location on the x axis
            self.player.move()
            self.missile_left.move()
            self.missile_right.move()

            # A bit of missile logic
            if self.missile_left.is_away():
                self.missile_left.reload()
            if self.missile_right.is_away():
                self.missile_right.reload()

            # Update the display
            self.screen.window.fill(self.screen.bg_color)
            self.missile_left.draw()
            self.missile_right.draw()
            self.player.draw()
            pygame.display.update()


if __name__ == '__main__':
    space = Space()
    space.main()
