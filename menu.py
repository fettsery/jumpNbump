#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import os, pygame, sys, time
from pygame.locals import *
import game


def runGame(screen):
    game.Game(screen)


def help(screen):
    pass


def quit(screen):
    sys.exit()


def fullscreen(screen):
    screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)


def normalscreen(screen):
    screen = pygame.display.set_mode((640, 480))


def Return(screen):
    Menu(screen)


def connect(screen):
    game.Game(screen, False)


def options(screen):
    MenuOptions(screen)


class Menu(object):
    def __init__(self, screen):
        self.screen = screen
        self.menu = SubMenu(screen, (("NEW_GAME", runGame), ("CONNECT", connect), \
                                     ("OPTIONS", options), ("CONTROLS", help), ("QUIT_GAME", quit)))
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.menu.set_font(pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16))
        image = pygame.image.load("data/menu.png")
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.bg = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("data/fonts/super-mario-64.ttf"), 45)
        self.clock = pygame.time.Clock()
        events = pygame.event.get()
        self.menu.update(events)
        self.menu.draw(self.screen)
        self.main_loop()

    def main_loop(self):
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menu.update(events)
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.bg, (0, 0))

            ren = self.font2.render("JumpNbump", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 235))

            self.menu.draw(self.screen)
            pygame.display.flip()


class MenuOptions(object):
    def __init__(self, screen):
        self.screen = screen
        self.menuO = SubMenu(screen, (("FULLSCREEN", fullscreen), ("WINDOWED MODE", normalscreen), ("RETURN", Return)))
        self.menuO.set_highlight_color((255, 0, 0))
        self.menuO.set_normal_color((255, 255, 255))
        self.menuO.center_at(300, 400)
        self.menuO.set_font(pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16))
        image = pygame.image.load("data/menu.png")
        image = pygame.transform.scale(image, (image.get_width() * 2, image.get_height() * 2))
        self.bg = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("data/fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("data/fonts/super-mario-64.ttf"), 45)
        events = pygame.event.get()
        self.clock = pygame.time.Clock()
        self.menuO.update(events)
        self.main_loop()

    def main_loop(self):
        while 1:
            self.clock.tick(30)
            events = pygame.event.get()
            self.menuO.update(events)
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

            self.screen.blit(self.bg, (0, 0))

            ren = self.font2.render("JumpNbump", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320 - ren.get_width() / 2, 235))

            self.menuO.draw(self.screen)
            pygame.display.flip()


class SubMenu(object):
    def __init__(self, screen, options):
        self.screen = screen
        self.options = options
        self.x = 0
        self.y = 0
        self.font = pygame.font.Font(None, 32)
        self.option = 0
        self.width = 1
        self.color = [0, 0, 0]
        self.hcolor = [255, 0, 0]
        self.height = len(self.options) * self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 2, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        i = 0
        for o in self.options:
            if i == self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 2, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren,
                         ((self.x + self.width / 3 * 2) - ren.get_width() / 2,
                          self.y + i * (self.font.get_height() + 4)))
            i += 1

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:
                    self.options[self.option][1](self.screen)
        if self.option > len(self.options) - 1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options) - 1

    def set_pos(self, x, y):
        self.x = x
        self.y = y

    def set_font(self, font):
        self.font = font

    def set_highlight_color(self, color):
        self.hcolor = color

    def set_normal_color(self, color):
        self.color = color

    def center_at(self, x, y):
        self.x = x - (self.width / 2)
        self.y = y - (self.height / 2)
