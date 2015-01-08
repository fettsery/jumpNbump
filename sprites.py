#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import datas, random
from constants import *

class Player(object):
    """
    player Class, checks collisions, checks state of player
    """

    def __init__(self, screen, num, image, sprites, players):
        """
        initialising
        :param screen: main view screen
        :param num: number of client
        :param image: image of player
        :param sprites: another objects in game
        :param players: another players
        :return:
        """
        self.screen = screen
        self.players = players
        self.sprites = sprites
        self.imagel = datas.load_image(image)
        self.imager = datas.load_image(ZNR_PICTURE)
        self.image = self.imager
        self.num = num
        self.posx = random.randint(0, LENGTH_BOUND)
        self.posy = random.randint(MAGIC_TWNT, HIGH_BOUND - DIST_DIFF)
        self.dx = 0
        self.jumping = False
        self.jump_speed = 0
        self.jump_acceleration = 0
        self.landed = False
        self.died = False
        self.send_died = False
        self.score = 0
        self.onboard = False
        self.movingactions = dict()
        self.movingactions[LEFT] = self.lefthandler
        self.movingactions[RIGHT] = self.righthandler
        self.movingactions[JUMP] = self.jumphandler

    def draw(self):
        """
        drawing player
        :return:
        """
        self.screen.blit(self.image, (self.posx, self.posy - DIST_DIFF))

    def lefthandler(self):
        self.posx -= MOVE
        self.image = self.imagel

    def righthandler(self):
        self.posx += MOVE
        self.image = self.imager

    def jumphandler(self):
        if not self.jumping:
            self.jump_speed = GRAVITY
            self.jumping = True
            self.jump_acceleration = ACCELERATION

    def move(self, action):
        """
        moving actions
        :param action:
        :return:
        """
        self.movingactions[action]()

    def goto(self, posx, posy):
        if posx < self.posx:
            self.image = self.imagel
        if posx > self.posx:
            self.image = self.imager
        self.posx = posx
        self.posy = posy

    def update(self):
        """
        updating condition
        :return:
        """

        self.posx += self.dx
        self.check_collision()
        if self.jumping and not self.died:
            self.jump_speed += self.jump_acceleration
            if self.jump_speed > 0 and self.landed:
                self.jump_speed = 0
                self.jumping = False
                self.landed = False
            self.posy += self.jump_speed
        if self.died:
            self.posy += self.jump_speed
        if self.died and self.posy >= HIGH_BOUND:
            self.died = False
            self.posy = random.randint(0, HIGH_BOUND - DIST_DIFF)
            self.posx = random.randint(MAGIC_TWNT, LENGTH_BOUND)
            self.image = self.imager
            self.jump_speed = 0
        if self.posx < 0:
            self.posx = 0
        if self.posx > LENGTH_BOUND:
            self.posx = LENGTH_BOUND
        if self.posy > HIGH_BOUND:
            self.posy = HIGH_BOUND
            self.jumping = False

    def check_collision(self):
        """
        checking collision with other objects
        :return:
        """
        falling = True
        for i in self.sprites:
            if self.posx >= i.posx - i.length and self.posx <= i.posx:
                if self.posy >= i.posy - i.high - MAGIC_TEN and self.posy <= i.posy - i.high + MAGIC_FTEN:
                    if self.posx >= i.posx - i.length and self.posx <= i.posx - i.length + MAGIC_TEN and i.boardingleft:
                        self.onboard = True
                    elif self.posx >= i.posx - MAGIC_FOUR and self.posx <= i.posx and i.boardingright:
                        self.onboard = True
                    else:
                        self.onboard = False
                    if i.kills:
                        self.kill()
                    falling = False
                    if self.jumping and self.jump_speed > 0 and not self.died:
                        self.landed = True
                        self.posy = i.posy - i.high
        if falling == True and not self.jumping and not self.landed:
            self.jumping = True
            self.jump_speed = DEAD_SPEED
            self.jump_acceleration = 0.6

    def kill(self):
        """
        kill player
        :return:
        """
        self.image = datas.load_image(ZN_DEAD)
        self.jump_speed = JUMP_SPEED
        self.died = True
        self.send_died = True


class Platform(object):
    """
    class for every object in game
    """

    def __init__(self, screen, image, posx, posy, length, high, boardingleft = False, boardingright = False, kills=False):
        """
        initialisation
        :param screen: main view screen
        :param image: image of object
        :param posx:
        :param posy:
        :param length: length in x coord
        :param high: length in y coord
        :param kills: if True it kills player on collision
        :return:
        """
        self.boardingleft = boardingleft
        self.boardingright = boardingright
        self.kills = kills
        self.length = length
        self.high = high
        self.screen = screen
        self.image = datas.load_image(image)
        self.posx = posx
        self.posy = posy

    def draw(self):
        """
        drawing object
        :return:
        """
        self.screen.blit(self.image, (self.posx, self.posy))