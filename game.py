#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
"""
module with server and client
"""
import pygame, os, sys, socket, threading
import sprites, datas, menu, constants

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
        self.sock.bind(('', constants.PORT_NUMBER))
        self.sock.listen(constants.MAX_PLAYERS)
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
                data = conn.recv(constants.RECV_PORTION)
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
            self.players[i] = sprites.Player(self.screen, i, constants.ZN_PICTURE, \
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
        self.num = int(a[constants.CLIENT_NUMBER_IND])
        if a[constants.CLIENT_INFORMATION] == "died" or a[constants.CLIENT_INFORMATION] == "quit" or a[constants.CLIENT_INFORMATION] == "itsyournum":
            self.command = a[constants.CLIENT_INFORMATION]
        else:
            self.posx = float(a[constants.CLIENT_POSX])
            self.posy = float(a[constants.CLIENT_POSY])
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
            self.sock.connect(('localhost', constants.PORT_NUMBER))
        except:
            return
        #We are asking server what is our num and soon it will answer
        self.sock.send("getmynum")
        self.objects = list()
        self.players = dict()
        self.screen = screen
        create_level(self.objects, screen)
        self.clock = pygame.time.Clock()
        self.background = datas.load_image(constants.BG_PICTURE)
        self.font = pygame.font.Font(os.path.realpath(constants.FONT), constants.FONT_SIZE)
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
                data = self.sock.recv(constants.RECV_PORTION)
            except:
                menu.Menu(pygame.display.set_mode((constants.SCREEN_LENGTH, constants.SCREEN_HIGHT)))
            if data:
                client_info = ClientInfo(data)
                #Yahoo, server sent us out number!
                if client_info.command == "itsyournum":
                    self.player = sprites.Player(self.screen, client_info.num, constants.ZN_PICTURE, \
                                            self.objects, self.players)
                    self.players[client_info.num] = self.player
                    continue
                #Ohh, there is somebody except us!
                try:
                    player = self.players[client_info.num]
                except KeyError:
                    player = sprites.Player(self.screen, client_info.num, constants.ZN_PICTURE, \
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

    def main_loop(self):
        """
        Logic that is common for every client
        """
        self.initAdditional()
        while self.running:
            self.clock.tick(constants.TICKS)
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
                        menu.Menu(pygame.display.set_mode((constants.SCREEN_LENGTH, constants.SCREEN_HIGHT)))
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
        pass

    def handler(self, event):
        """
        Handling events, that derive class should process
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.player.move(constants.ON_RIGHT)
            if event.key == pygame.K_LEFT:
                self.player.move(constants.ON_LEFT)
            if event.key == pygame.K_SPACE:
                self.player.move(constants.JUMP)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.player.move(constants.ON_RIGHT_UP)
            if event.key == pygame.K_LEFT:
                self.player.move(constants.ON_LEFT_UP)

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
        self.dest = 1
        self.steps = 0
        self.search = False

    def bot_update(self):
        """
        Bot logic
        """
        #find nearest player
        min = constants.MAGIC
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
                self.player.move(constants.LEFT)
            else:
                self.player.move(constants.RIGHT)
        if self.search and not self.player.onboard:
            if self.dest < 0:
                self.player.move(constants.LEFT)
            else:
                self.player.move(constants.RIGHT)
        if self.search and self.player.onboard:
            self.search = False
            self.steps = constants.DEFAULT_STEPS
        if self.player.posx <= 0:
            self.dest *= -1
        if self.player.posx >= constants.SCREEN_LENGTH:
            self.dest *= -1
        if self.player.posx > self.players[mini].posx and not self.search and self.steps == 0:
            self.player.move(constants.LEFT)
        elif not self.search and self.steps == 0:
            self.player.move(constants.RIGHT)
        if self.player.posy > self.players[mini].posy:
            if self.player.onboard:
                self.player.move(constants.JUMP)
        if abs(self.player.posx - self.players[mini].posx) < constants.RABBIT_SIZE and \
            abs(self.player.posy - self.players[mini].posy) < constants.RABBIT_SIZE:
                self.player.move(constants.JUMP)

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
        except KeyError or AttributeError:
            pass

def create_level(objects, screen):
    """
    creating level
    :param: objects - game objects
    :param: screen - main view screen
    :return:
    """
    f = open(constants.LEVEL)
    for line in f:
        a = line.split()
        boardingleft = 0
        boardingright = 0
        killing = 0
        if len(a) == constants.LEFT_LEN or len(a) == constants.RIGHT_LEN:
            if int(a[constants.BOARDING_LEFT_POS]) == 0:
                boardingleft = False
            else:
                boardingleft = True
        if len(a) == constants.RIGHT_LEN:
            if int(a[constants.BOARDING_RIGHT_POS]) == 0:
                boardingright = False
            else:
                boardingright = True
        if len(a) == constants.KILL_LEN:
            killing = bool(a[constants.KILL_POS])
        var = globals()[a[0]]
        objects.append(sprites.Platform(screen, var, int(a[constants.PLATFORM_POSX_POS]), int(a[constants.PLATFORM_POSY_POS]), \
                                        int(a[constants.PLATFORM_LEN_POS]), int(a[constants.PLATFORM_HIG_POS]), \
                                        boardingleft, boardingright, killing))
