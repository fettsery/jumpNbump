#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import pygame, os, sys, socket, threading
import sprites, data

class Server(object):
    def __init__(self, screen):
        self.getconnections = True
        self.sock = socket.socket()
        self.sock.bind(('', 9092))
        self.sock.listen(7)
        self.objects = list()
        self.players = list()
        self.screen = screen
        self.level = Level(self.objects, screen)
        self.level.create_level()
        self.player = sprites.Player(screen, 0, "data/zn2.png", self.objects, \
                             self.players, self.sock)
        self.clock = pygame.time.Clock()
        self.background = data.load_image("data/background.png")
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 10)
        self.running = True
        self.thread = threading.Thread(target=self.connection)
        self.thread.setDaemon(True)
        self.thread.start()
        self.main_loop()

    def connection(self):
        """
        manage connections
        :return:
        """
        i = 1
        while self.getconnections:
            conn, _ = self.sock.accept()
            self.players.append(sprites.Player(self.screen, i, "data/zn2.png", \
                                       self.objects, self.players, conn))
            i += 1

    def send_info(self, action):
        """
        send command
        :param action: what to send
        :return:
        """
        for i in self.players:
            i.conn.send("0")
            i.conn.send(action)

    def main_loop(self):
        """
        main game loop
        :return:
        """
        while self.running:
            self.clock.tick(30)
            self.draw()
            pygame.display.flip()
            self.player.update()
            for i in self.players:
                i.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.getconnections = False
                        sys.exit()
                    if event.key == pygame.K_RIGHT:
                        self.send_info("right")
                        self.player.move("right")
                    if event.key == pygame.K_LEFT:
                        self.send_info("left")
                        self.player.move("left")
                    if event.key == pygame.K_SPACE:
                        self.send_info("space")
                        self.player.move("space")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.send_info("rightup")
                        self.player.move("rightup")
                    if event.key == pygame.K_LEFT:
                        self.send_info("leftup")
                        self.player.move("leftup")
    def draw(self):
        """
        draw everything
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        for i in self.objects:
            i.draw()
        self.player.draw()
        for i in self.players:
            i.draw()

class Client(object):
    """
    main Game class
    """
    def __init__(self, screen):
        """
        :param screen:
        :param server: True if it is server, False if it is client
        :return:
        """
        self.sock = socket.socket()
        self.sock.connect(('localhost', 9092))
        self.objects = list()
        self.players = list()
        self.screen = screen
        self.level = Level(self.objects, screen)
        self.level.create_level()
        self.player = sprites.Player(screen, 0, "data/zn2.png", self.objects, \
                             self.players, self.sock)
        self.clock = pygame.time.Clock()
        self.background = data.load_image("data/background.png")
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 10)
        self.running = True
        self.thread = threading.Thread(target=self.getdata)
        self.thread.setDaemon(True)
        self.thread.start()
        self.main_loop()

    def getdata(self):
        """
        receiving data from clients
        :return:
        """
        while True:
            data = self.sock.recv(1024)
            if data:
                try:
                    player = self.players[int(data)]
                except IndexError:
                    self.players.append(sprites.Player(self.screen, int(data), "data/zn2.png", \
                                               self.objects, self.players, self.sock))
                    player = self.players[int(data)]
                data = self.sock.recv(1024)
                player.move(data)

    def send_info(self, action):
        """
        send command
        :param action: what to send
        :return:
        """
        self.sock.send(action)

    def main_loop(self):
        """
        main game loop
        :return:
        """
        while self.running:
            self.clock.tick(30)
            self.draw()
            pygame.display.flip()
            self.player.update()
            for i in self.players:
                i.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    if event.key == pygame.K_RIGHT:
                        self.send_info("right")
                        self.player.move("right")
                    if event.key == pygame.K_LEFT:
                        self.send_info("left")
                        self.player.move("left")
                    if event.key == pygame.K_SPACE:
                        self.send_info("space")
                        self.player.move("space")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.send_info("rightup")
                        self.player.move("rightup")
                    if event.key == pygame.K_LEFT:
                        self.send_info("leftup")
                        self.player.move("leftup")

    def draw(self):
        """
        draw everything
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        for i in self.objects:
            i.draw()
        self.player.draw()
        for i in self.players:
            i.draw()

class Level(object):
    def __init__(self, objects, screen):
        self.objects = objects
        self.screen = screen

    def create_level(self):
        """
        creating level
        :return:
        """
        self.objects.append(sprites.Platform(self.screen, "data/bush-2.png", 0, 450, 50, 25))
        self.objects.append(sprites.Platform(self.screen, "data/bush-3.png", 50, 450, 50, 25))
        self.objects.append(sprites.Platform(self.screen, "data/bush-3.png", 100, 450, 60, 25))
        self.objects.append(sprites.Platform(self.screen, "data/lava.png", 160, 460, 40, 25, True))
        self.objects.append(sprites.Platform(self.screen, "data/lava.png", 200, 460, 40, 25, True))
        self.objects.append(sprites.Platform(self.screen, "data/lava.png", 240, 460, 40, 25, True))
        self.objects.append(sprites.Platform(self.screen, "data/bush-2.png", 270, 450, 70, 25))
        self.objects.append(sprites.Platform(self.screen, "data/bush-2.png", 340, 450, 60, 25))
        self.objects.append(sprites.Platform(self.screen, "data/bush-3.png", 400, 450, 60, 25))
        self.objects.append(sprites.Platform(self.screen, "data/lava.png", 460, 460, 40, 25, True))
        self.objects.append(sprites.Platform(self.screen, "data/lava.png", 500, 460, 60, 25, True))
        self.objects.append(sprites.Platform(self.screen, "data/bush-2.png", 560, 450, 50, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 160, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 190, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 220, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 430, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 460, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 490, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 520, 360, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 260, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 290, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 320, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 520, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 550, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 580, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 0, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 30, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 60, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 90, 280, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 60, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 90, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brick1.png", 120, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 320, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 350, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 380, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 410, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 440, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/brickblue1.png", 470, 180, 30, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 50, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 90, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 120, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 160, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 200, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 240, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 400, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 440, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 480, 50, 0, 25))
        self.objects.append(sprites.Platform(self.screen, "data/cloud.png", 520, 50, 0, 25))