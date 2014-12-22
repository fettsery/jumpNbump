#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import threading
import data

class Player(object):
    """
    player Class
    """
    def __init__(self, screen, num, image, sprites, players, conn):
        """
        initialising
        :param screen:
        :param num:
        :param image:
        :param sprites:
        :param players:
        :param conn:
        :return:
        """
        self.conn = conn
        if num != 0:
            self.thread = threading.Thread(target=self.connection)
            self.thread.setDaemon(True)
            self.thread.start()
        self.screen = screen
        self.players = players
        self.sprites = sprites
        self.imagel = data.load_image(image)
        self.imager = data.load_image("data/zn2r.png")
        self.image = self.imager
        self.num = num
        self.posx = 20
        self.posy = 420
        self.dx = 0
        self.jumping = False
        self.jump_speed = 0
        self.jump_acceleration = 0
        self.landed = False
        self.died = False
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

    def connection(self):
        """
        receiving commands thread
        :return:
        """
        while True:
            data = self.conn.recv(1024)
            if data:
                for i in self.players:
                    if i.num != self.num:
                        i.conn.send(str(i.num))
                        i.conn.send(data)
                self.move(data)

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
            self.posy = 420
            self.posx = 20
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
        for i in self.players:
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
        self.image = data.load_image("data/dead.png")
        self.jump_speed = 5
        self.died = True


class Platform(object):
    """
    class for every object in game
    """
    def __init__(self, screen, image, posx, posy, length, high, kills=False):
        """
        initialisation
        :param screen:
        :param image:
        :param posx:
        :param posy:
        :param length:
        :param high:
        :param kills:
        :return:
        """
        self.kills = kills
        self.length = length
        self.high = high
        self.screen = screen
        self.image = data.load_image(image)
        self.posx = posx
        self.posy = posy

    def draw(self):
        """
        drawing object
        :return:
        """
        self.screen.blit(self.image, (self.posx, self.posy))