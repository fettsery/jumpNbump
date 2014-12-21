#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import pygame, os, sys, socket, threading
from sprites import *


def load_image(filename):
    filename = os.path.realpath(filename)
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, \
                                       (image.get_width() * 2, image.get_height() * 2))
    except pygame.error:
        raise SystemExit, "Unable to load: " + filename
    return image.convert_alpha()


class Game(object):
    def __init__(self, screen, server=True):
        self.server = server
        self.getconnections = True
        if server == True:
            self.sock = socket.socket()
            self.sock.bind(('', 9092))
            self.sock.listen(7)
        if server == False:
            self.sock = socket.socket()
            self.sock.connect(('localhost', 9092))
        self.objects = list()
        self.players = list()
        self.screen = screen
        self.create_level()
        self.Player = Player(screen, 0, "data/zn2.png", self.objects, \
                             self.players, self.sock)
        self.clock = pygame.time.Clock()
        self.bg = load_image("data/background.png")
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 10)
        self.running = True
        if self.server == True:
            self.t = threading.Thread(target=self.connection, args=(self,))
            self.t.start()
            self.connected = True
        if self.server == False:
            self.t = threading.Thread(target=self.getdata, args=(self,))
            self.t.start()
            self.connected = True
        self.main_loop()

    def connection(self, some):
        i = 1
        while self.getconnections:
            conn, addr = self.sock.accept()
            self.players.append(Player(self.screen, i, "data/zn2.png", \
                                       self.objects, self.players, conn))
            i += 1

    def getdata(self, some):
        while True:
            data = self.sock.recv(1024)
            if data:
                try:
                    player = self.players[int(data)]
                except:
                    self.players.append(Player(self.screen, int(data), "data/zn2.png",\
                                               self.objects, self.players, self.sock))
                    player = self.players[int(data)]
                data = self.sock.recv(1024)
                player.move(data)

    def send_info(self, action):
        if self.server == False:
            self.sock.send(action)
        if self.server == True:
            for i in self.players:
                i.conn.send("0")
                i.conn.send(action)

    def main_loop(self):
        while self.running:
            self.clock.tick(30)
            self.draw()
            pygame.display.flip()
            self.Player.update()
            for i in self.players:
                i.update()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        self.getconnections = False
                        sys.exit()
                    if e.key == pygame.K_RIGHT:
                        self.send_info("right")
                        self.Player.move("right")
                    if e.key == pygame.K_LEFT:
                        self.send_info("left")
                        self.Player.move("left")
                    if e.key == pygame.K_SPACE:
                        self.send_info("space")
                        self.Player.move("space")
                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_RIGHT:
                        self.send_info("rightup")
                        self.Player.move("rightup")
                    if e.key == pygame.K_LEFT:
                        self.send_info("leftup")
                        self.Player.move("leftup")

    def create_level(self):
        self.objects.append(Platform(self.screen, "data/bush-2.png", 0, 450, 50, 25))
        self.objects.append(Platform(self.screen, "data/bush-3.png", 50, 450, 50, 25))
        self.objects.append(Platform(self.screen, "data/bush-3.png", 100, 450, 60, 25))
        self.objects.append(Platform(self.screen, "data/lava.png", 160, 460, 40, 25, True))
        self.objects.append(Platform(self.screen, "data/lava.png", 200, 460, 40, 25, True))
        self.objects.append(Platform(self.screen, "data/lava.png", 240, 460, 40, 25, True))
        self.objects.append(Platform(self.screen, "data/bush-2.png", 270, 450, 70, 25))
        self.objects.append(Platform(self.screen, "data/bush-2.png", 340, 450, 60, 25))
        self.objects.append(Platform(self.screen, "data/bush-3.png", 400, 450, 60, 25))
        self.objects.append(Platform(self.screen, "data/lava.png", 460, 460, 40, 25, True))
        self.objects.append(Platform(self.screen, "data/lava.png", 500, 460, 60, 25, True))
        self.objects.append(Platform(self.screen, "data/bush-2.png", 560, 450, 50, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 160, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 190, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 220, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 430, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 460, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 490, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 520, 360, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 260, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 290, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 320, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 520, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 550, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 580, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 0, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 30, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 60, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 90, 280, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 60, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 90, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brick1.png", 120, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 320, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 350, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 380, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 410, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 440, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/brickblue1.png", 470, 180, 30, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 50, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 90, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 120, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 160, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 200, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 240, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 400, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 440, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 480, 50, 0, 25))
        self.objects.append(Platform(self.screen, "data/cloud.png", 520, 50, 0, 25))

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for i in self.objects:
            i.draw()
        self.Player.draw()
        for i in self.players:
            i.draw()



