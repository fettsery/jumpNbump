#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
"""
module with server and client
"""
import pygame, os, sys, socket, threading
import sprites, datas, menu
import math

PORT_NUMBER = 9093
ZN_PICTURE = "data/zn2.png"
BG_PICTURE = "data/background.png"
FONT = "data/fonts/font.ttf"
CLIENT_NUMBER_IND = 0
CLIENT_INFORMATION = 1
CLIENT_POSX = 1
CLIENT_POSY = 2
LEVEL = "data/level"
BUSH1_PICTURE = "data/bush-2.png"
BUSH2_PICTURE = "data/bush-3.png"
LAVA_PICTURE = "data/lava.png"
BRICK_PICTURE = "data/brick1.png"
BRICK_BLUE_PICTURE = "data/brickblue1.png"
CLOUD_PICTURE = "data/cloud.png"
MAGIC = 1000000

class Server(object):
    """
    Server class, getting actions messages from clients and retranslates it to other clients
    """

    def __init__(self, screen, bots):
        """
        initialisation
        :return:
        """
        self.bots = list()
        self.dest = 1
        self.steps = 0
        self.search = False
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
                try:
                    self.bots.remove(num)
                except ValueError:
                    #it is not a bot
                    pass
                for i in self.bots:
                    print i
                for i in self.connections:
                    try:
                        i.send(str(num) + " quit")
                    except:
                        self.connections.remove(i)
                return
            j = 0
            if data:
                if (data == "bot"):
                    self.bots.append(num)
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
                    try:
                        i.send(str(j.num) + " " + str(j.posx) + " " + str(j.posy))
                    except:
                        pass
            self.bots_update()
            for i in self.players.values():
                i.update()
                if i.send_died:
                    i.send_died = False
                    for j in self.connections:
                        j.send(str(i.num) + " died")

    def bots_update(self):
        for i in self.bots:
            #find nearest player
            min = MAGIC
            mini = 0
            for j in self.players.keys():
                if j != i:
                    dist = (self.players[i].posx - self.players[j].posx) ** 2 + \
                        (self.players[i].posy - self.players[j].posy) ** 2
                    if dist < min:
                        min = dist
                        mini = j
            if abs(self.players[i].posx - self.players[mini].posx) < 2 and not self.players[i].jumping:
                self.search = True
            if self.steps > 0:
                self.steps -= 1
                self.players[i].posx -= 3 * self.dest
            if self.search and not self.players[i].onboard:
                self.players[i].posx -= 3 * self.dest
            if self.search and self.players[i].onboard:
                self.search = False
                self.steps = 30
            if self.players[i].posx <= 0:
                self.dest *= -1
            if self.players[i].posx >= 640:
                self.dest *= -1
            if self.players[i].posx > self.players[mini].posx and not self.search and self.steps == 0:
                self.players[i].posx -= 3
            elif not self.search and self.steps == 0:
                self.players[i].posx += 3
            if self.players[i].posy > self.players[mini].posy:
                if self.players[i].onboard:
                    self.players[i].move("space")
            if abs(self.players[i].posx - self.players[mini].posx) < 50 and \
                abs(self.players[i].posy - self.players[mini].posy) < 50:
                    self.players[i].move("space")

class ClientInfo(object):
    """
    Wrapper for data from server
    """

    def __init__(self, client_info):
        a = client_info.split()
        self.num = int(a[CLIENT_NUMBER_IND])
        if a[CLIENT_INFORMATION] == "died" or a[CLIENT_INFORMATION] == "quit":
            self.command = a[CLIENT_INFORMATION]
        else:
            self.posx = float(a[CLIENT_POSX])
            self.posy = float(a[CLIENT_POSY])
            self.command = "void"


class Client(object):
    """
    Common client methods
    """

    def __init__(self, screen):
        """
        :param screen: main view screen
        :return:
        """
        self.connected = True
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
        while self.connected:
            try:
                data = self.sock.recv(1024)
            except:
                menu.Menu(pygame.display.set_mode((640, 480)))
            if data:
                client_info = ClientInfo(data)

                try:
                    player = self.players[client_info.num]
                except KeyError:
                    player = sprites.Player(self.screen, client_info.num, ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[client_info.num] = player
                if client_info.command == "died":
                    player.kill()
                elif client_info.command == "quit":
                    self.players.pop(client_info.num)
                else:
                    player.goto(client_info.posx, client_info.posy)

    def send_info(self, action):
        """
        send command
        :param action: what to send
        :return:
        """
        self.sock.send(action)

    def draw(self):
        """
        draw everything
        :return:
        """
        try:
            self.screen.blit(self.background, (0, 0))
        except:
            sys.exit()
        for i in self.objects:
            i.draw()
        for i in self.players.values():
            i.draw()

class PlayerClient(Client):
    """
    A client that is controlled by player
    """
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
                        self.connected = False
                        self.sock.close()
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

class BotClient(Client):
    """
    A client, that sends server information that it is a bot and it can't control itself
    """
    def main_loop(self):
        """
        main game loop
        :return:
        """
        self.send_info("bot")
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
                        self.connected = False
                        self.sock.close()
                        menu.Menu(pygame.display.set_mode((640, 480)))

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
        boardingleft = 0
        boardingright = 0
        killing = 0
        if len(a) == 6 or len(a) == 7:
            if int(a[5]) == 0:
                boardingleft = False
            else:
                boardingleft = True
        if len(a) == 7:
            if int(a[6]) == 0:
                boardingright = False
            else:
                boardingright = True
        if len(a) == 8:
            killing = bool(a[7])
        var = globals()[a[0]]
        objects.append(sprites.Platform(screen, var, int(a[1]), int(a[2]), int(a[3]), int(a[4]), boardingleft, boardingright, killing))
