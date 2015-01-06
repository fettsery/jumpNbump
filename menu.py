#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import os, pygame, sys, socket
import game, constants

def rungame(screen):
    """
    running new game
    :param screen: main view screen
    :return:
    """
    try:
        game.Server(screen, 0)
    except socket.error:
        pass
    game.PlayerClient(screen)

def quitfun(screen):
    """
    exit from game
    :param screen: main view screen
    :return:
    """
    if screen:
        pass
    sys.exit()


def fullscreen(screen):
    """
    make fullscreen
    :param screen: main view screen
    :return:
    """
    if screen:
        pass
    screen = pygame.display.set_mode((constants.SCREEN_LENGTH, constants.SCREEN_HIGHT), pygame.FULLSCREEN)


def normalscreen(screen):
    """
    make normalscreen
    :param screen: main view screen
    :return:
    """
    if screen:
        pass
    screen = pygame.display.set_mode((constants.SCREEN_LENGTH, constants.SCREEN_HIGHT))


def returntomain(screen):
    """
    return to main menu
    :param screen: main view screen
    :return:
    """
    Menu(screen)


def connect(screen):
    """
    connect to server
    :param screen:
    :return:
    """
    game.PlayerClient(screen)


def options(screen):
    """
    options menu
    :param screen: main view screen
    :return:
    """
    MenuOptions(screen)

def playbots(screen):
    game.BotClient(screen)

class Menu(object):
    """
    Menu class(buttons and actions)
    """

    def __init__(self, screen):
        """
        initialising
        :param screen: main view screen
        :return:
        """
        self.screen = screen
        self.menu = SubMenu(screen, (("NEW_GAME", rungame), ("CONNECT_AS_BOT", playbots), ("CONNECT", connect), \
                                     ("OPTIONS", options), ("QUIT_GAME", quitfun)))
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(constants.MENU_CENTX, constants.MENU_CENTY)
        self.menu.set_font(pygame.font.Font(os.path.realpath(constants.FONT), constants.FONT1_SIZE))
        image = pygame.image.load(constants.MENU_PICTURE)
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.background = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath(constants.FONT), constants.FONT1_SIZE)
        self.font2 = pygame.font.Font(os.path.realpath(constants.SMFONT), constants.FONT2_SIZE)
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
            self.clock.tick(constants.TICKS)
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
            self.screen.blit(ren, (constants.MMAGIC - ren.get_width() / 2, constants.JNBM_MAGIC))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (constants.MMAGIC - ren.get_width() / 2, constants.PY_MAGIC))

            self.menu.draw(self.screen)
            pygame.display.flip()


class MenuOptions(object):
    """
    Options Menu class
    """

    def __init__(self, screen):
        """
        initialising
        :param screen: main view screen
        :return:
        """
        self.screen = screen
        self.menuoptions = SubMenu(screen, (
        ("FULLSCREEN", fullscreen), ("WINDOWED MODE", normalscreen), ("RETURN", returntomain)))
        self.menuoptions.set_highlight_color((255, 0, 0))
        self.menuoptions.set_normal_color((255, 255, 255))
        self.menuoptions.center_at(constants.MENU_CENTX, constants.MENU_CENTY)
        self.menuoptions.set_font(pygame.font.Font(os.path.realpath(constants.FONT), constants.FONT1_SIZE))
        image = pygame.image.load(constants.MENU_PICTURE)
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.background = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath(constants.FONT), constants.FONT1_SIZE)
        self.font2 = pygame.font.Font(os.path.realpath(constants.SMFONT), constants.FONT2_SIZE)
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
            self.clock.tick(constants.TICKS)
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
            self.screen.blit(ren, (constants.MMAGIC - ren.get_width() / 2, constants.JNBM_MAGIC))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (constants.MMAGIC - ren.get_width() / 2, constants.PY_MAGIC))

            self.menuoptions.draw(self.screen)
            pygame.display.flip()


class SubMenu(object):
    """
    Submenu class
    """

    def __init__(self, screen, optionsa):
        """
        initialising
        :param screen: main view screen
        :param optionsa: options(color)
        :return:
        """
        self.screen = screen
        self.optionsa = optionsa
        self.xcoord = 0
        self.ycoord = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.optionsa) * self.font.get_height()
        for option in self.optionsa:
            text = option[0]
            ren = self.font.render(text, 2, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        """
        draw menu
        :param surface: main view screen
        :return:
        """
        i = 0
        for option in self.optionsa:
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
        :param events: button presses
        :return:
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.option += 1
                if event.key == pygame.K_UP:
                    self.option -= 1
                if event.key == pygame.K_RETURN:
                    self.optionsa[self.option][1](self.screen)
        if self.option > len(self.optionsa) - 1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.optionsa) - 1

    def set_pos(self, xcoord, ycoord):
        """
        set position
        :param xcoord: x coordinate
        :param ycoord: y coordinate
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
