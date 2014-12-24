#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import datas, random

ZNR_PICTURE = "data/zn2r.png"
ZN_DEAD = "data/dead.png"

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
        self.posx = random.randint(0, 650)
        self.posy = random.randint(0, 420)
        self.dx = 0
        self.jumping = False
        self.jump_speed = 0
        self.jump_acceleration = 0
        self.landed = False
        self.died = False
        self.send_died = False
        self.score = 0

    def draw(self):
        """
        drawing player
        :return:
        """
        self.screen.blit(self.image, (self.posx, self.posy - 30))

    def move(self, action):
        """
        moving actions
        :param action:
        :return:
        """
        if action == "right":
            self.dx += 3
            self.image = self.imager
        if action == "left":
            self.dx -= 3
            self.image = self.imagel
        if action == "leftup":
            self.dx += 3
        if action == "rightup":
            self.dx -= 3
        if action == "space":
            if not self.jumping:
                self.jump_speed = -11.4
                self.jumping = True
                self.jump_acceleration = 0.6

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
        if self.jumping:
            self.jump_speed += self.jump_acceleration
            if self.jump_speed > 0 and self.landed:
                self.jump_speed = 0
                self.jumping = False
                self.landed = False
            self.posy += self.jump_speed
        if self.died:
            self.posy += self.jump_speed
        if self.died and self.posy >= 450:
            self.died = False
            self.posy = random.randint(0, 420)
            self.posx = random.randint(20, 650)
            self.image = self.imager
            self.jump_speed = 0
        if self.posx < 0:
            self.posx = 0
        if self.posx > 640:
            self.posx = 640
        if self.posy > 450:
            self.posy = 450
            self.jumping = False

    def check_collision(self):
        """
        checking collision with other objects
        :return:
        """
        falling = True
        for i in self.sprites:
            if self.posx >= i.posx - i.length and self.posx <= i.posx:
                if self.posy >= i.posy - i.high - 10 and self.posy <= i.posy - i.high + 15:
                    if i.kills:
                        self.kill()
                    falling = False
                    if self.jumping and self.jump_speed > 0:
                        self.landed = True
                        self.posy = i.posy - i.high
        for i in self.players.values():
            if i.posx - 30 <= self.posx <= i.posx + 30 and i.posy - 30 <= self.posy <= i.posy + 30 and i.num != self.num:
                if self.posy >= i.posy:
                    self.kill()
                    i.score += 1
                else:
                    self.score += 1
                    i.kill()
        if falling == True and not self.jumping and not self.landed:
            self.jumping = True
            self.jump_speed = 5
            self.jump_acceleration = 0.6

    def kill(self):
        """
        kill player
        :return:
        """
        self.image = datas.load_image(ZN_DEAD)
        self.jump_speed = 5
        self.died = True
        self.send_died = True


class Platform(object):
    """
    class for every object in game
    """

    def __init__(self, screen, image, posx, posy, length, high, kills=False):
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