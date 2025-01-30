import random
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 87, 51)
YELLOW = (255, 200, 50)
GRAY = (204, 204, 204)
GRASS = (0, 92, 8)
SKY = (33, 174, 255)
NIGHT = (35, 2, 82)
SUN = (255, 220, 56)
SET = (254, 76, 21)
MOON = (211, 211, 211)
PINK = (224, 43, 185)
BRI_YELLOW = (229, 255, 0)
BRI = (230, 205, 46)
DARK_RED = (102, 0, 0)
SPD = 3
IDK = [200, 970]
s_loc = [50, 160]
n1 = [10, 10]
x_speed = 0
score = 0
score_speed = 1
day_night = random.choice([SKY, NIGHT, SET])
COLOR = random.choice([WHITE, YELLOW])
FPS = 60
resets = 0

GRAVITY = 1

# LAYOUT = [
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '111111111    111111111111',
#     '1111111  1111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111',
#     '1111111111111111111111111'
# ]

# LAYOUT = [
#     '1111111111111111111111111',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1gggggggggggggggggggggggg1',
#     '1111111111111111111111111'
# ]

LAYOUT =[
    '1111111111111111111111111',
    '1111111111111111111111111',
    '1                       1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1           rml         1',
    '1           342         1',
    '1           RML         1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1                       1',
    '1111111111111111111111111',
    '1111111111111111111111111'
    '1111111111111111111111111',
    '1111111111111111111111111',
]

# print(len(LAYOUT[0]), len(LAYOUT))
BRICK_WIDTH = 50
big_width = 200
BRICK_HEIGHT = 50
PLAYER_WIDTH = 35
PLAYER_HEIGHT = 35
WIDTH = 32*20
HEIGHT = 32*20
x_speed = 5
# print(WIDTH)
# 1250
wid = 25
hid = 25
frewid = 15
frehid = 15
ENEMY_WIDTH = 40 
ENEMY_HEIGHT = 40
slime_width = 50
slime_height = 50

test = 250

TILESIZE = 32
# 32
# 32
