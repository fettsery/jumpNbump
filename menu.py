#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import os, pygame, sys
import game


def rungame(screen):
    """
    running new game
    :param screen:
    :return:
    """
    game.Server(screen)
    game.Client(screen)

def helpfun(screen):
    """
    printing controls
    :param screen:
    :return:
    """
    if screen:
        pass


def quitfun(screen):
    """
    exit from game
    :param screen:
    :return:
    """
    if screen:
        pass
    sys.exit()


def fullscreen(screen):
    """
    make fullscreen
    :param screen:
    :return:
    """
    if screen:
        pass
    screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)


def normalscreen(screen):
    """
    make normalscreen
    :param screen:
    :return:
    """
    if screen:
        pass
    screen = pygame.display.set_mode((640, 480))


def returntomain(screen):
    """
    return to main menu
    :param screen:
    :return:
    """
    Menu(screen)


def connect(screen):
    """
    connect to server
    :param screen:
    :return:
    """
    game.Client(screen)


def options(screen):
    """
    options menu
    :param screen:
    :return:
    """
    MenuOptions(screen)


class Menu(object):
    """
    Menu class
    """
    def __init__(self, screen):
        """
        initialising
        :param screen:
        :return:
        """
        self.screen = screen
        self.menu = SubMenu(screen, (("NEW_GAME", rungame), ("CONNECT", connect), \
                                     ("OPTIONS", options), ("CONTROLS", helpfun), ("QUIT_GAME", quitfun)))
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.menu.set_font(pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16))
        image = pygame.image.load("data/menu.png")
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.background = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("data/fonts/super-mario-64.ttf"), 45)
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.main_loop()

    def main_loop(self):
        """
        main menu loop
        :return:
        """
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menu.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.background, (0, 0))

            ren = self.font2.render("JumpNbump", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 235))

            self.menu.draw(self.screen)
            pygame.display.flip()


class MenuOptions(object):
    """
    Options class
    """
    def __init__(self, screen):
        """
        initialising
        :param screen:
        :return:
        """
        self.screen = screen
        self.menuoptions = SubMenu(screen, (("FULLSCREEN", fullscreen), ("WINDOWED MODE", normalscreen), ("RETURN", returntomain)))
        self.menuoptions.set_highlight_color((255, 0, 0))
        self.menuoptions.set_normal_color((255, 255, 255))
        self.menuoptions.center_at(300, 400)
        self.menuoptions.set_font(pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16))
        image = pygame.image.load("data/menu.png")
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.background = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("data/fonts/super-mario-64.ttf"), 45)
        events = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.menuoptions.update(events)
        self.main_loop()

    def main_loop(self):
        """
        main options loop
        :return:
        """
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menuoptions.update(events)
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.background, (0, 0))

            ren = self.font2.render("JumpNbump", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 235))

            self.menuoptions.draw(self.screen)
            pygame.display.flip()


class SubMenu(object):
    """
    Submenu class
    """
    def __init__(self, screen, options):
        """
        initialising
        :param screen:
        :param options:
        :return:
        """
        self.screen = screen
        self.options = options
        self.xcoord = 0
        self.ycoord = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options) * self.font.get_height()
        for option in self.options:
            text = option[0]
            ren = self.font.render(text, 2, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        """
        draw menu
        :param surface:
        :return:
        """
        i = 0
        for option in self.options:
            if i == self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = option[0]
            ren = self.font.render(text, 2, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren,
                         ((self.xcoord + self.width / 3 * 2) - ren.get_width() / 2,
                          self.ycoord + i * (self.font.get_height() + 4)))
            i += 1

    def update(self, events):
        """
        update menu
        :param events:
        :return:
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.option += 1
                if event.key == pygame.K_UP:
                    self.option -= 1
                if event.key == pygame.K_RETURN:
                    self.options[self.option][1](self.screen)
        if self.option > len(self.options) - 1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options) - 1

    def set_pos(self, xcoord, ycoord):
        """
        set position
        :param xcoord:
        :param ycoord:
        :return:
        """
        self.xcoord = xcoord
        self.ycoord = ycoord

    def set_font(self, font):
        """
        setting font
        :param font:
        :return:
        """
        self.font = font

    def set_highlight_color(self, color):
        """
        seting hihlight color
        :param color:
        :return:
        """
        self.hcolor = color

    def set_normal_color(self, color):
        """
        setting normal color
        :param color:
        :return:
        """
        self.color = color

    def center_at(self, xcoord, ycoord):
        """
        center at x, y
        :param xcoord:
        :param ycoord:
        :return:
        """
        self.xcoord = xcoord - (self.width / 2)
        self.ycoord = ycoord - (self.height / 2)
