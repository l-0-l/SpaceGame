class Const:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    BG_COLOR = (0, 0, 0)

    SPACESHIP_ACCELERATION = 0.5
    SPACESHIP_MAX_SPEED = 20
    SPACESHIP_FLAME_OFFSET_X_LEFT = 22
    SPACESHIP_FLAME_OFFSET_X_RIGHT = 44
    SPACESHIP_FLAME_OFFSET_Y = 73
    SPACESHIP_ANIMATION_TO_SPEED_RATIO = 2
    SPACESHIP_SPEED_DROP_ON_SIDE_IMPACT = 1.5
    SPACESHIP_HITSIZE = (7, 15, -7, -15)

    FRAME_TIME_SEC = 0.1

    MISSILE_INITIAL_SPEED = 0.0
    MISSILE_ACCELERATION = 0.3
    MISSILE_STOWED_OFFSET_X_LEFT = 18
    MISSILE_STOWED_OFFSET_X_RIGHT = 48
    MISSILE_STOWED_OFFSET_Y = 32
    MISSILE_FLAME_SIZE = 12

    STAR_NUM_SMALL = 60
    STAR_NUM_BRIGHT = 20
    STAR_SPEED_SMALL = (0.04, 0.08)
    STAR_SPEED_BRIGHT = (0.08, 1.2)
    STAR_COORD_APPEAR = -5
    STAR_ANIMATION_CHANCE = 30  # The larger the number here - the smaller the chance is

    PLANET_SPEED_X = (-0.01, 0.01)
    PLANET_SPEED_Y = (-0.01, 0.01)
    PLANET_MIN_SIZE = 200

    OFF_THE_SCREEN_LEFT = -150
    OFF_THE_SCREEN_RIGHT = SCREEN_WIDTH + 150
    OFF_THE_SCREEN_TOP = -150
    OFF_THE_SCREEN_BOTTOM = SCREEN_HEIGHT + 150

    ASTEROID_MIN_SIZE = 20
    ASTEROID_SPEED_HORIZONTAL_MIN = -1.5
    ASTEROID_SPEED_HORIZONTAL_MAX = 1.5
    ASTEROID_SPEED_VERTICAL_MIN = 1
    ASTEROID_SPEED_VERTICAL_MAX = 5
    ASTEROID_ACCELERATION_HORIZONTAL_MIN = 0
    ASTEROID_ACCELERATION_HORIZONTAL_MAX = 0.1
    ASTEROID_ACCELERATION_VERTICAL_MIN = 0
    ASTEROID_ACCELERATION_VERTICAL_MAX = 0.5
    ASTEROID_BORDER_LEFT = 80
    ASTEROID_BORDER_RIGHT = SCREEN_WIDTH - ASTEROID_BORDER_LEFT
    ASTEROID_APPEAR_HEIGHT = -150
    ASTEROID_ANIMATE_COEFFICIENT = 7  # Asteroid's rotation speed is determined by its vertical speed
    ASTEROID_HITSIZE_COEFFICIENT = 9

    EXPLOSION_ANIMATE_SPEED = 0.05
    EXPLOSION_HIT_DELTA = 50

    INITIAL_X_POS = SCREEN_WIDTH / 2
    INITIAL_Y_POS = SCREEN_HEIGHT - SCREEN_HEIGHT / 10

    INVADER_SIZE = 70
    INVADER_DESCEND = 20
    INVADER_HITSIZE = (INVADER_SIZE / 11, INVADER_SIZE / 4.6, - INVADER_SIZE / 17, - INVADER_SIZE / 5.7)
    INVADER_RIGHT_BORDER = SCREEN_WIDTH - INVADER_SIZE
    INVADER_LEFT_BORDER = 0
    INVADER_STARTING_X = - INVADER_SIZE * 2
    INVADER_STARTING_Y = 50
    INVADER_ENTRY_SPEED = 5
    INVADER_TOP_BORDER = 20

    DEBUG = False
