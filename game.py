#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
"""
module with server and client
"""
import pygame, os, sys, socket, threading
import sprites, datas, menu

PORT_NUMBER = 9093
ZN_PICTURE = "data/zn2.png"
BG_PICTURE = "data/background.png"
FONT = "data/fonts/font.ttf"
LEVEL = "data/level"
BUSH1_PICTURE = "data/bush-2.png"
BUSH2_PICTURE = "data/bush-3.png"
LAVA_PICTURE = "data/lava.png"
BRICK_PICTURE = "data/brick1.png"
BRICK_BLUE_PICTURE = "data/brickblue1.png"
CLOUD_PICTURE = "data/cloud.png"

class Server(object):
    """
    Server class, getting actions messages from clients and retranslates it to other clients
    """

    def __init__(self, screen):
        """
        initialisation
        :return:
        """
        self.screen = screen
        self.sock = socket.socket()
        self.sock.bind(('', PORT_NUMBER))
        self.sock.listen(7)
        self.players = dict()
        self.objects = list()
        create_level(self.objects, self.screen)
        self.connections = list()
        self.clock = pygame.time.Clock()
        self.running = True
        self.thread = threading.Thread(target=self.connection)
        self.thread.setDaemon(True)
        self.thread.start()
        self.threads = list()
        thread = threading.Thread(target=self.main_loop)
        thread.setDaemon(True)
        thread.start()

    def retranslate(self, num, conn):
        """
        receiving commands thread
        :param: num - number of client
        :param: conn - its socket
        :return:
        """
        while True:
            try:
                data = conn.recv(1024)
            except:
                self.players.pop(num)
                for i in self.connections:
                    try:
                        i.send(str(num) + " quit")
                    except:
                        self.connections.remove(i)
                return
            j = 0
            if data:
                self.players[num].move(data)

    def connection(self):
        """
        manage connections
        :return:
        """
        i = 0
        while 1:
            conn, _ = self.sock.accept()
            self.connections.append(conn)
            self.players[i] = sprites.Player(self.screen, i, ZN_PICTURE, \
                                            self.objects, self.players)
            thread = threading.Thread(target=self.retranslate, args=(i,conn,))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            i += 1

    def main_loop(self):
        """
        main game loop
        :return:
        """
        while self.running:
            self.clock.tick(30)
            for i in self.connections:
                for j in self.players.values():
                    i.send(str(j.num) + " " + str(j.posx) + " " + str(j.posy))
            for i in self.players.values():
                i.update()
                if i.send_died:
                    i.send_died = False
                    for j in self.connections:
                        j.send(str(i.num) + " died")



class Client(object):
    """
    Client class, that gets events from keyboard, processes collisions, sends and gets information
    from server and draws everything.
    """

    def __init__(self, screen):
        """
        :param screen: main view screen
        :return:
        """
        self.sock = socket.socket()
        try:
            self.sock.connect(('localhost', PORT_NUMBER))
        except:
            return
        self.objects = list()
        self.players = dict()
        self.screen = screen
        create_level(self.objects, screen)
        self.clock = pygame.time.Clock()
        self.background = datas.load_image(BG_PICTURE)
        self.font = pygame.font.Font(os.path.realpath(FONT), 10)
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
            try:
                data = self.sock.recv(1024)
            except:
                menu.Menu(pygame.display.set_mode((640, 480)))

            if data:
                a = data.split()
                try:
                    player = self.players[int(a[0][0])]
                except KeyError:
                    player = sprites.Player(self.screen, int(a[0][0]), ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[int(a[0][0])] = player
                if a[1] == "died":
                    player.kill()
                if a[1] == "quit":
                    self.players.pop(int(a[0][0]))
                else:
                    try:
                        player.goto(float(a[1]), float(a[2]))
                    except ValueError:
                        continue
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
            try:
                pygame.display.flip()
            except:
                sys.exit()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.Menu(pygame.display.set_mode((640, 480)))
                    if event.key == pygame.K_RIGHT:
                        self.send_info("right")
                    if event.key == pygame.K_LEFT:
                        self.send_info("left")
                    if event.key == pygame.K_SPACE:
                        self.send_info("space")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.send_info("rightup")
                    if event.key == pygame.K_LEFT:
                        self.send_info("leftup")

    def draw(self):
        """
        draw everything
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        for i in self.objects:
            i.draw()
        for i in self.players.values():
            i.draw()


def create_level(objects, screen):
    """
    creating level
    :param: objects - game objects
    :param: screen - main view screen
    :return:
    """
    f = open(LEVEL)
    for line in f:
        a = line.split()
        cond = False
        if len(a) == 6:
            cond = bool(a[5])
        var = globals()[a[0]]
        objects.append(sprites.Platform(screen, var, int(a[1]), int(a[2]), int(a[3]), int(a[4]), cond))