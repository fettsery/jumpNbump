#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import game, pygame, threading


class Player:
    def __init__(self, screen, num, image, sprites, players, conn):
        self.conn = conn
        if num != 0:
            self.t = threading.Thread(target=self.connection, args=(self,))
            self.t.start()
        self.screen = screen
        self.players = players
        self.sprites = sprites
        self.imagel = game.load_image(image)
        self.imager = game.load_image("data/zn2r.png")
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
        self.screen.blit(self.image, (self.posx, self.posy - 30))

    def move(self, action):
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

    def connection(self, some):
        while True:
            data = self.conn.recv(1024)
            if data:
                for i in self.players:
                    if i.num != self.num:
                        i.conn.send(str(i.num))
                        i.conn.send(data)
                self.move(data)

    def update(self):

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
        falling = True
        for i in self.sprites:
            if self.posx >= i.posx - i.len and self.posx <= i.posx:
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
        self.image = game.load_image("data/dead.png")
        self.jump_speed = 5
        self.died = True


class Platform:
    def __init__(self, screen, image, posx, posy, len, high, kills=False):
        self.kills = kills
        self.len = len
        self.high = high
        self.screen = screen
        self.image = game.load_image(image)
        self.posx = posx
        self.posy = posy

    def draw(self):
        self.screen.blit(self.image, (self.posx, self.posy))