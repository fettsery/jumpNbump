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
FONT_SIZE = 10
TICKS = 30
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
MAX_PLAYERS = 7
RECV_PORTION = 1024
SCREEN_HIGHT = 480
SCREEN_LENGTH = 640
RABBIT_SIZE = 50
BOT_MOVING = 3
DEFAULT_STEPS = 30
BOARDING_LEFT_POS = 5
BOARDING_RIGHT_POS = 6
KILL_POS = 7
LEFT_LEN = 6
RIGHT_LEN = 7
KILL_LEN = 8
PLATFORM_POSX_POS = 1
PLATFORM_POSY_POS = 2
PLATFORM_LEN_POS = 3
PLATFORM_HIG_POS = 4
class Server(object):
    """
    Server class, getting actions messages from clients and retranslates it to other clients
    """

    def __init__(self, screen, bots):
        """
        initialisation
        :return:
        """
        self.screen = screen
        self.sock = socket.socket()
        self.sock.bind(('', PORT_NUMBER))
        self.sock.listen(MAX_PLAYERS)
        self.clock = pygame.time.Clock()
        self.players = dict()
        self.objects = list()
        create_level(self.objects, self.screen)
        self.connections = list()
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
                data = conn.recv(RECV_PORTION)
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
                if data == "getmynum":
                    conn.send(str(num) + " itsyournum ")
                    continue
                for i in range(len(self.connections)):
                    if i != num:
                        self.connections[i].send(str(num) + " " + data)

    def connection(self):
        """
        manage connections
        :return:
        """
        i = 0
        while True:
            conn, _ = self.sock.accept()
            self.connections.append(conn)
            self.players[i] = sprites.Player(self.screen, i, ZN_PICTURE, \
                                            self.objects, self.players)
            thread = threading.Thread(target=self.retranslate, args=(i,conn,))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            i += 1


class ClientInfo(object):
    """
    Wrapper for data from server
    """

    def __init__(self, client_info):
        a = client_info.split()
        self.num = int(a[CLIENT_NUMBER_IND])
        if a[CLIENT_INFORMATION] == "died" or a[CLIENT_INFORMATION] == "quit" or a[CLIENT_INFORMATION] == "itsyournum":
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
        #We are asking server what is our num and soon it will answer
        self.sock.send("getmynum")
        self.objects = list()
        self.players = dict()
        self.screen = screen
        create_level(self.objects, screen)
        self.clock = pygame.time.Clock()
        self.background = datas.load_image(BG_PICTURE)
        self.font = pygame.font.Font(os.path.realpath(FONT), FONT_SIZE)
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
                data = self.sock.recv(RECV_PORTION)
            except:
                menu.Menu(pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HIGHT)))
            if data:
                client_info = ClientInfo(data)
                #Yahoo, server sent us out number!
                if client_info.command == "itsyournum":
                    self.player = sprites.Player(self.screen, client_info.num, ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[client_info.num] = self.player
                    continue
                #Ohh, there is somebody except us!
                try:
                    player = self.players[client_info.num]
                except KeyError:
                    player = sprites.Player(self.screen, client_info.num, ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[client_info.num] = player
                #Somebody is superman!
                if client_info.command == "died":
                    player.kill()
                #Ohh, somebody left us:(
                elif client_info.command == "quit":
                    self.players.pop(client_info.num)
                else:
                    player.goto(client_info.posx, client_info.posy)

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

    def common(self):
        """


        """
        while self.running:
            self.clock.tick(TICKS)
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
                        menu.Menu(pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HIGHT)))

class PlayerClient(Client):
    """
    A client that is controlled by player
    """
    def main_loop(self):
        """
        main game loop
        :return:
        """
        self.commonthread = threading.Thread(target=self.common)
        self.commonthread.setDaemon(True)
        self.commonthread.start()
        while self.running:
            self.clock.tick(TICKS)
            self.player.update()
            self.sock.send(str(self.player.posx) + " " + str(self.player.posy))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
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

class BotClient(Client):
    """
    A client, that controls itself without player
    """
    def bot_update(self):
        #find nearest player
        min = MAGIC
        mini = 0
        for j in self.players.values():
            if j != self.player:
                dist = (self.player.posx - j.posx) ** 2 + \
                    (self.player.posy - j.posy) ** 2
                if dist < min:
                    min = dist
                    mini = j.num
        if abs(self.player.posx - self.players[mini].posx) < 2 and not self.player.jumping:
            self.search = True
        if self.steps > 0:
            self.steps -= 1
            self.player.posx -= BOT_MOVING * self.dest
        if self.search and not self.player.onboard:
            self.player.posx -= BOT_MOVING * self.dest
        if self.search and self.player.onboard:
            self.search = False
            self.steps = DEFAULT_STEPS
        if self.player.posx <= 0:
            self.dest *= -1
        if self.player.posx >= SCREEN_LENGTH:
            self.dest *= -1
        if self.player.posx > self.players[mini].posx and not self.search and self.steps == 0:
            self.player.posx -= BOT_MOVING
        elif not self.search and self.steps == 0:
            self.player.posx += BOT_MOVING
        if self.player.posy > self.players[mini].posy:
            if self.player.onboard:
                self.player.move("space")
        if abs(self.player.posx - self.players[mini].posx) < RABBIT_SIZE and \
            abs(self.player.posy - self.players[mini].posy) < RABBIT_SIZE:
                self.player.move("space")

    def main_loop(self):
        """
        main game loop
        :return:
        """
        self.dest = 1
        self.steps = 0
        self.search = False
        self.commonthread = threading.Thread(target=self.common)
        self.commonthread.setDaemon(True)
        self.commonthread.start()
        while self.running:
            self.clock.tick(TICKS)
            try:
                self.bot_update()
            except KeyError or AttributeError:
                pass
            self.player.update()
            self.sock.send(str(self.player.posx) + " " + str(self.player.posy))
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    pass


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
        if len(a) == LEFT_LEN or len(a) == RIGHT_LEN:
            if int(a[BOARDING_LEFT_POS]) == 0:
                boardingleft = False
            else:
                boardingleft = True
        if len(a) == RIGHT_LEN:
            if int(a[BOARDING_RIGHT_POS]) == 0:
                boardingright = False
            else:
                boardingright = True
        if len(a) == KILL_LEN:
            killing = bool(a[KILL_POS])
        var = globals()[a[0]]
        objects.append(sprites.Platform(screen, var, int(a[PLATFORM_POSX_POS]), int(a[PLATFORM_POSY_POS]), \
                                        int(a[PLATFORM_LEN_POS]), int(a[PLATFORM_HIG_POS]), \
                                        boardingleft, boardingright, killing))
