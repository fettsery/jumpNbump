#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import datas, random, mutex
from constants import *

def void(some):
    pass
class Player(object):
    """
    player Class, checks collisions, checks state of player
    """

    def __init__(self, screen, num, image, sprites):
        """
        initialising
        :param screen: main view screen
        :param num: number of client
        :param image: image of player
        :param sprites: another objects in game
        :param players: another players
        :return:
        """
        self.active = False
        self.sprites = sprites
        self.movingright = False
        self.movingleft = False
        self.num = num
        self.__posx = random.randint(0, LENGTH_BOUND)
        self.__posy = random.randint(MAGIC_TWNT, HIGH_BOUND - DIST_DIFF)
        self.playerview = PlayerView(screen, self, image)
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
        self.mutex = mutex.mutex()

    def lefthandler(self):
        self.__posx -= MOVE
        self.playerview.setleft()

    def righthandler(self):
        self.__posx += MOVE
        self.playerview.setright()

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
        self.mutex.lock(function=void, argument=0)
        if posx < self.__posx:
            self.playerview.setleft()
        if posx > self.__posx:
            self.playerview.setright()
        self.__posx = posx
        self.__posy = posy
        self.mutex.unlock()

    def update(self):
        """
        updating condition
        :return:
        """
        self.mutex.lock(function=void, argument=0)
        try:
            if self.movingright:
                self.move(RIGHT)
            if self.movingleft:
                self.move(LEFT)
        except AttributeError:
            pass
        self.__posx += self.dx
        self.check_collision()
        if self.jumping and not self.died:
            self.jump_speed += self.jump_acceleration
            if self.jump_speed > 0 and self.landed:
                self.jump_speed = 0
                self.jumping = False
                self.landed = False
            self.__posy += self.jump_speed
        if self.died:
            self.__posy += self.jump_speed
        if self.died and self.__posy >= HIGH_BOUND:
            self.died = False
            self.__posy = random.randint(0, HIGH_BOUND - DIST_DIFF)
            self.__posx = random.randint(MAGIC_TWNT, LENGTH_BOUND)
            self.playerview.setright()
            self.jump_speed = 0
        if self.__posx < 0:
            self.__posx = 0
        if self.__posx > LENGTH_BOUND:
            self.__posx = LENGTH_BOUND
        if self.__posy > HIGH_BOUND:
            self.__posy = HIGH_BOUND
            self.jumping = False
        self.mutex.unlock()

    def check_collision(self):
        """
        checking collision with other objects
        :return:
        """
        falling = True
        for i in self.sprites:
            if self.__posx >= i.posx - i.length and self.__posx <= i.posx:
                if self.__posy >= i.posy - i.high - MAGIC_TEN and self.__posy <= i.posy - i.high + MAGIC_FTEN:
                    if self.__posx >= i.posx - i.length and self.__posx <= i.posx - i.length + MAGIC_TEN and i.boardingleft:
                        self.onboard = True
                    elif self.__posx >= i.posx - MAGIC_FOUR and self.__posx <= i.posx and i.boardingright:
                        self.onboard = True
                    else:
                        self.onboard = False
                    if i.kills:
                        self.kill()
                    falling = False
                    if self.jumping and self.jump_speed > 0 and not self.died:
                        self.landed = True
                        self.__posy = i.posy - i.high
        if falling == True and not self.jumping and not self.landed:
            self.jumping = True
            self.jump_speed = DEAD_SPEED
            self.jump_acceleration = 0.6

    def kill(self):
        """
        kill player
        :return:
        """
        self.mutex.lock(function=void, argument=0)
        self.playerview.setdied()
        self.jump_speed = JUMP_SPEED
        self.died = True
        self.send_died = True
        self.mutex.unlock()

    def getposx(self):
        return self.__posx

    def getposy(self):
        return self.__posy

class PlayerView(object):
    def __init__(self, screen, player, image):
        self.screen = screen
        self.player = player
        self.imagel = datas.load_image(image)
        self.imager = datas.load_image(ZNR_PICTURE)
        self.imaged = datas.load_image(ZN_DEAD)
        self.image = self.imager

    def setleft(self):
        self.image = self.imagel

    def setright(self):
        self.image = self.imager

    def setdied(self):
        self.image = self.imaged

    def draw(self):
        """
        drawing player
        :return:
        """
        if self.player.active:
            self.screen.blit(self.image, (self.player.getposx(), self.player.getposy() - DIST_DIFF))

class Bot(object):
    def __init__(self, player, players):
        self.player = player
        self.players = players
        self.dest = 1
        self.steps = 0
        self.search = False

    def update(self):
        """
        Bot logic
        """
        #find nearest player
        min = MAGIC
        mini = 0
        for j in self.players.values():
            if j != self.player:
                dist = (self.player.getposx() - j.getposx()) ** 2 + \
                    (self.player.getposy() - j.getposy()) ** 2
                if dist < min:
                    min = dist
                    mini = j.num
        if abs(self.player.getposx() - self.players[mini].getposx()) < 2 and not self.player.jumping:
            self.search = True
        if self.steps > 0:
            self.steps -= 1
            if self.dest < 0:
                self.player.move(LEFT)
            else:
                self.player.move(RIGHT)
        if self.search and not self.player.onboard:
            if self.dest < 0:
                self.player.move(LEFT)
            else:
                self.player.move(RIGHT)
        if self.search and self.player.onboard:
            self.search = False
            self.steps = DEFAULT_STEPS
        if self.player.getposx() <= 0:
            self.dest *= -1
        if self.player.getposx() >= LENGTH_BOUND:
            self.dest *= -1
        if self.player.getposx() > self.players[mini].getposx() and not self.search and self.steps == 0:
            self.player.move(LEFT)
        elif not self.search and self.steps == 0:
            self.player.move(RIGHT)
        if self.player.getposy() > self.players[mini].getposy():
            if self.player.onboard:
                self.player.move(JUMP)
        if abs(self.player.getposx() - self.players[mini].getposx()) < RABBIT_SIZE and \
            abs(self.player.getposy() - self.players[mini].getposy()) < RABBIT_SIZE:
                self.player.move(JUMP)

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