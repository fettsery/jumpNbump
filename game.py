#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
"""
module with server and client
"""
import pygame, os, sys, socket, threading
import sprites, datas, menu
from constants import *

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
        main = threading.Thread(target=self.main_loop)
        main.setDaemon(True)
        main.start()

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
                #self.players.pop(num)
                self.players[num].active = False
                for i in self.connections:
                    try:
                        i.send(str(num) + " " + QUIT_COMMAND)
                    except:
                        self.connections.remove(i)
                return
            j = 0
            if data:
                if data == GETMYNUM_COMMAND:
                    conn.send(str(num) + " " +ITSYOURNUM_COMMAND+ " ")
                    continue
                a = data.split()
                self.players[num].goto(float(a[0]), float(a[1]))
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
                                            self.objects)
            self.players[i].active = True
            thread = threading.Thread(target=self.retranslate, args=(i,conn,))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            i += 1

    def main_loop(self):
        """
        Players bumping logic
        """
        while True:
            for i in range(len(self.players) - 1):
                for j in range(i, len(self.players)):
                    if self.players[i].active and self.players[j].active:
                        try:
                            if self.players[j].getposx() - DIST_DIFF <= self.players[i].getposx() <= self.players[j].getposx() + DIST_DIFF\
                                    and self.players[j].getposy() - DIST_DIFF <= self.players[i].getposy() \
                                            <= self.players[j].getposy() + DIST_DIFF and self.players[j].num != self.players[i].num:
                                if self.players[i].getposy() >= self.players[j].getposy():
                                    for k in self.connections:
                                        k.send(str(self.players[i].num) + " " + DIED_COMMAND +" ")
                                else:
                                    for k in self.connections:
                                        k.send(str(self.players[j].num) + " " + DIED_COMMAND +" ")
                        except KeyError:
                            pass

class Controller(object):
    def __init__(self):
        self.keydown = pygame.KEYDOWN
        self.keyup = pygame.KEYUP
        self.leftbutton = pygame.K_LEFT
        self.rightbutton = pygame.K_RIGHT
        self.jumpbutton = pygame.K_SPACE

class ClientInfo(object):
    """
    Wrapper for data from server
    """

    def __init__(self, client_info):
        a = client_info.split()
        self.num = int(a[CLIENT_NUMBER_IND])
        if a[CLIENT_INFORMATION] == DIED_COMMAND \
                or a[CLIENT_INFORMATION] == QUIT_COMMAND or a[CLIENT_INFORMATION] == ITSYOURNUM_COMMAND:
            self.command = a[CLIENT_INFORMATION]
        else:
            self.posx = float(a[CLIENT_POSX])
            self.posy = float(a[CLIENT_POSY])
            self.command = VOID_COMMAND


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
        self.sock.send(GETMYNUM_COMMAND)
        self.objects = list()
        self.players = dict()
        self.screen = screen
        create_level(self.objects, screen)
        self.player = sprites.Player(self.screen, 0, ZN_PICTURE, \
                        self.objects)
        self.clock = pygame.time.Clock()
        self.running = True
        self.clientview = ClientView(screen, self.objects, self.players)
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
                if client_info.command == ITSYOURNUM_COMMAND:
                    self.player.num = client_info.num
                    self.players[client_info.num] = self.player
                    self.player.active = True
                    continue
                #Ohh, there is somebody except us!
                try:
                    player = self.players[client_info.num]
                    self.players[client_info.num].active = True
                except KeyError:
                    player = sprites.Player(self.screen, client_info.num, ZN_PICTURE, \
                                            self.objects)
                    self.players[client_info.num] = player
                #Somebody is superman!
                if client_info.command == DIED_COMMAND:
                    player.kill()
                    continue
                #Ohh, somebody left us:(
                if client_info.command == QUIT_COMMAND:
                    self.players[client_info.num].active = False
                else:
                    player.goto(client_info.posx, client_info.posy)

    def main_loop(self):
        """
        Logic that is common for every client
        """
        self.initAdditional()
        while self.running:
            self.clock.tick(TICKS)
            self.clientview.draw()
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
                self.handler(event)
            self.update()
            try:
                self.player.update()
            except AttributeError:
                #wait for itsyournum command
                continue
            try:
                if self.player.active:
                    self.sock.send(str(self.player.getposx()) + " " + str(self.player.getposy()))
            except socket.error:
                sys.exit()

class ClientView(object):
    """
    Class for drawing
    """
    def __init__(self, screen, objects, players):
        self.screen = screen
        self.objects = objects
        self.players = players
        self.background = datas.load_image(BG_PICTURE)
        pass

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
            i.playerview.draw()

class PlayerClient(Client):
    """
    A client that is controlled by player
    """
    def initAdditional(self):
        """
        Initialising derive Class variables
        """
        self.controller = Controller()
        pass

    def handler(self, event):
        """
        Handling events, that derive class should process
        """
        if event.type == self.controller.keydown:
            if event.key == self.controller.rightbutton:
                self.player.movingright = True
            if event.key == self.controller.leftbutton:
                self.player.movingleft = True
            if event.key == self.controller.jumpbutton:
                self.player.move(JUMP)
        if event.type == self.controller.keyup:
            if event.key == self.controller.rightbutton:
                self.player.movingright = False
            if event.key == self.controller.leftbutton:
                self.player.movingleft = False

    def update(self):
        """
        Do derive class logic
        """
        pass


class BotClient(Client):
    """
    A client, that controls itself without player
    """

    def initAdditional(self):
        """
        Initialising derive Class variables
        """
        self.bot = sprites.Bot(self.player, self.players)

    def handler(self, event):
        """
        Handling events, that derive class should process
        """
        pass

    def update(self):
        """
        Do derive class logic
        """
        try:
            self.bot.update()
        except KeyError:
            pass
        except AttributeError:
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
