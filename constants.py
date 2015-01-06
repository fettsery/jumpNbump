#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
"""
Constants for JumpNbump
"""

#Screen sizes
SCREEN_HIGHT = 480
SCREEN_LENGTH = 640
#Rabbit pics
ZNR_PICTURE = "data/zn2r.png"
ZN_PICTURE = "data/zn2.png"
ZN_DEAD = "data/dead.png"
#Background picture
BG_PICTURE = "data/background.png"
#Screen bounds
HIGH_BOUND = 450
LENGTH_BOUND = 610
#Constants for determining collisions
DIST_DIFF = 30
MAGIC_TEN = 10
MAGIC_FTEN = 15
MAGIC_TWNT = 20
MAGIC_FOUR = 4
#Speed constants
JUMP_SPEED = 10
DEAD_SPEED = 5
ACCELERATION = 0.6
GRAVITY = -11.4
#Socket info
PORT_NUMBER = 9093
MAX_PLAYERS = 7
RECV_PORTION = 1024
#Font info
FONT = "data/fonts/font.ttf"
SMFONT = "data/fonts/super-mario-64.ttf"
FONT_SIZE = 10
FONT1_SIZE = 16
FONT2_SIZE = 45
#Main cycle ticks
TICKS = 30
#Information indexes in sending information
CLIENT_NUMBER_IND = 0
CLIENT_INFORMATION = 1
CLIENT_POSX = 1
CLIENT_POSY = 2
#Building level constants
LEVEL = "data/level"
BOARDING_LEFT_POS = 5
BOARDING_RIGHT_POS = 6
KILL_POS = 7
LEFT_LEN = 6
RIGHT_LEN = 7
KILL_LEN = 8
PLATFORM_POSX_POS = 1
PLATFORM_POSY_POS = 2
PLATFORM_LEN_POS = 3
PLATFORM_HIG_POS = 4
#Menu constants
MENU_PICTURE = "data/menu.png"
MENU_CENTX = 300
MENU_CENTY = 400
MMAGIC = 320
JNBM_MAGIC = 180
PY_MAGIC = 235
#Bot control constants
MAGIC = 1000000
RABBIT_SIZE = 50
BOT_MOVING = 3
DEFAULT_STEPS = 30