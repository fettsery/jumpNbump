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

    def __init__(self):
        """
        initialisation
        :return:
        """
        self.sock = socket.socket()
        self.sock.bind(('', PORT_NUMBER))
        self.sock.listen(7)
        self.objects = list()
        self.connections = list()
        self.clock = pygame.time.Clock()
        self.running = True
        self.thread = threading.Thread(target=self.connection)
        self.thread.setDaemon(True)
        self.thread.start()
        self.threads = list()

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
                j = 0
                for i in self.connections:
                    if num == j:
                        self.connections.remove(i)
                    if num != j:
                        try:
                            i.send("p" + str(j) + " quit")
                        except:
                            self.connections.remove(i)
                j += 1
                return
            j = 0
            if data:
                for i in self.connections:
                    if num != j:
                        try:
                            i.send("p" + str(j) + " " + data)
                        except:
                            self.connections.remove(i)
                    j += 1

    def connection(self):
        """
        manage connections
        :return:
        """
        i = 0
        while 1:
            conn, _ = self.sock.accept()
            self.connections.append(conn)
            thread = threading.Thread(target=self.retranslate, args=(i,conn,))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            i += 1



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
        self.sock.connect(('localhost', PORT_NUMBER))
        self.objects = list()
        self.players = dict()
        self.screen = screen
        create_level(self.objects, screen)
        self.player = sprites.Player(screen, 0, ZN_PICTURE, self.objects, \
                                     self.players)
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
                    player = self.players[int(a[0][1])]
                except KeyError:
                    player = sprites.Player(self.screen, int(a[0][1]), ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[int(a[0][1])] = player
                if a[1] == "died":
                    print "dead"
                    player.kill()
                if a[1] == "quit":
                    self.players.pop(int(a[0][1]))
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
            self.send_info(str(self.player.posx) + " " + str(self.player.posy))
            self.draw()
            pygame.display.flip()
            self.player.update()
            if self.player.send_died:
                self.send_info("died")
                self.player.send_died = False
            for i in self.players.values():
                i.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu.Menu(pygame.display.set_mode((640, 480)))
                    if event.key == pygame.K_RIGHT:
                        self.player.move("right")
                    if event.key == pygame.K_LEFT:
                        self.player.move("left")
                    if event.key == pygame.K_SPACE:
                        self.player.move("space")
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.move("rightup")
                    if event.key == pygame.K_LEFT:
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