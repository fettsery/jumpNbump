#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import os, pygame, sys, time
from pygame.locals import *
from mainMenu import *

class Menu(object):
    def __init__(self, screen):
        self.screen = screen
#        self.menu = MainMenu(["NEW GAME", lambda: RunGame(screen)], ["OPTIONS", lambda: MenuO(screen)],
#                             ["CONTROLS", lambda: Help(screen)], ["QUIT_GAME", sys.exit()])
        self.menu = MainMenu(screen, ("NEW_GAME", "CONNECT", "OPTIONS", "CONTROLS", "QUIT_GAME"))
        self.menu.set_highlight_color((255, 0, 0))
        self.menu.set_normal_color((255, 255, 255))
        self.menu.center_at(300, 400)
        self.menu.set_font(pygame.font.Font(os.path.realpath("fonts/font.ttf"), 16))
        image = pygame.image.load("menu.png")
        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
        self.bg = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("fonts/super-mario-64.ttf"), 45)
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