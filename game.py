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
                self.players.pop(num)
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
                                            self.objects, self.players)
            thread = threading.Thread(target=self.retranslate, args=(i,conn,))
            thread.setDaemon(True)
            thread.start()
            self.threads.append(thread)
            i += 1

    def main_loop(self):
        while True:
            for i in range(len(self.players) - 1):
                for j in range(i, len(self.players)):
                    if self.players[j].posx - DIST_DIFF <= self.players[i].posx <= self.players[j].posx + DIST_DIFF\
                            and self.players[j].posy - DIST_DIFF <= self.players[i].posy \
                                    <= self.players[j].posy + DIST_DIFF and self.players[j].num != self.players[i].num:
                        if self.players[i].posy >= self.players[j].posy:
                            for k in self.connections:
                                k.send(str(self.players[i].num) + " " + DIED_COMMAND +" ")
                        else:
                            for k in self.connections:
                                k.send(str(self.players[j].num) + " " + DIED_COMMAND +" ")

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
                if client_info.command == ITSYOURNUM_COMMAND:
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
                if client_info.command == DIED_COMMAND:
                    player.kill()
                    continue
                #Ohh, somebody left us:(
                if client_info.command == QUIT_COMMAND:
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

    def main_loop(self):
        """
        Logic that is common for every client
        """
        self.initAdditional()
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
                self.handler(event)
            self.update()
            try:
                self.player.update()
            except AttributeError:
                #wait for itsyournum command
                continue
            try:
                self.sock.send(str(self.player.posx) + " " + str(self.player.posy))
            except socket.error:
                sys.exit()

class PlayerClient(Client):
    """
    A client that is controlled by player
    """
    def initAdditional(self):
        """
        Initialising derive Class variables
        """
        self.controller = Controller()
        self.movingright = False
        self.movingleft = False
        pass

    def handler(self, event):
        """
        Handling events, that derive class should process
        """
        if event.type == self.controller.keydown:
            if event.key == self.controller.rightbutton:
                self.movingright = True
            if event.key == self.controller.leftbutton:
                self.movingleft = True
            if event.key == self.controller.jumpbutton:
                self.player.move(JUMP)
        if event.type == self.controller.keyup:
            if event.key == self.controller.rightbutton:
                self.movingright = False
            if event.key == self.controller.leftbutton:
                self.movingleft = False

    def update(self):
        """
        Do derive class logic
        """
        try:
            if self.movingright:
                self.player.move(RIGHT)
            if self.movingleft:
                self.player.move(LEFT)
        except AttributeError:
            pass
        pass


class BotClient(Client):
    """
    A client, that controls itself without player
    """

    def initAdditional(self):
        """
        Initialising derive Class variables
        """
        self.dest = 1
        self.steps = 0
        self.search = False

    def bot_update(self):
        """
        Bot logic
        """
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
            if self.dest < 0:
                self.player.move(LEFT)
            else:
                self.player.move(RIGHT)
        if self.search and not self.player.onboard:
            if self.dest < 0:
                self.player.move(LEFT)
            else:
                self.player.move(RIGHT)
        if self.search and self.player.onboard:
            self.search = False
            self.steps = DEFAULT_STEPS
        if self.player.posx <= 0:
            self.dest *= -1
        if self.player.posx >= SCREEN_LENGTH:
            self.dest *= -1
        if self.player.posx > self.players[mini].posx and not self.search and self.steps == 0:
            self.player.move(LEFT)
        elif not self.search and self.steps == 0:
            self.player.move(RIGHT)
        if self.player.posy > self.players[mini].posy:
            if self.player.onboard:
                self.player.move(JUMP)
        if abs(self.player.posx - self.players[mini].posx) < RABBIT_SIZE and \
            abs(self.player.posy - self.players[mini].posy) < RABBIT_SIZE:
                self.player.move(JUMP)

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
            self.bot_update()
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
