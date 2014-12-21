#!/usr/bin/env python
# coding=utf-8
# 2.7
#fettser.yury
import pygame, os, sys
import menu, game
def RunGame(screen):
    game.Game(screen)
def Help():
    pass
def Fullscreen(screen):
    screen = pygame.display.set_mode((640, 480), pygame.FULLSCREEN)
def Normalscreen(screen):
    screen = pygame.display.set_mode((640, 480))
def Connect(screen):
    game.Game(screen, False)

class MenuO(object):
    def __init__(self, screen):
        self.screen = screen
        self.menuO = MainMenu(screen, ("FULLSCREEN", "WINDOWED MODE", "RETURN"))
        self.menuO.set_highlight_color((255, 0, 0))
        self.menuO.set_normal_color((255, 255, 255))
        self.menuO.center_at(300, 400)
        self.menuO.set_font(pygame.font.Font(os.path.realpath("fonts/font.ttf"), 16))
        image = pygame.image.load("menu.png")
        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
        self.bg = image.convert_alpha()
        self.font = pygame.font.Font(os.path.realpath("fonts/font.ttf"), 16)
        self.font2 = pygame.font.Font(os.path.realpath("fonts/super-mario-64.ttf"), 45)
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
            self.screen.blit(ren, (320-ren.get_width()/2, 180))

            ren = self.font2.render("Python", 1, (255, 255, 255))
            self.screen.blit(ren, (320-ren.get_width()/2, 235))

            self.menuO.draw(self.screen)
            pygame.display.flip()
class MainMenu:

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
        self.height = len(self.options)*self.font.get_height()
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 2, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o
            ren = self.font.render(text, 2, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, ((self.x+self.width/4) - ren.get_width()/2, self.y + i*(self.font.get_height()+4)))
            i+=1

    def update(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN:
                    if self.option == 0 and self.options[0] == "NEW_GAME":
                        RunGame(self.screen)
                    if self.option == 0 and self.options[0] == "FULLSCREEN":
                        Fullscreen(self.screen)
                    if self.option == 1 and self.options[1] == "CONNECT":
                        Connect(self.screen)
                    if self.option == 2 and self.options[2] == "OPTIONS":
                        MenuO(self.screen)
                    if self.option == 1 and self.options[1] == "WINDOWED MODE":
                        Normalscreen(self.screen)
                    if self.option == 3 and self.options[3] == "CONTROLS":
                        Help()
                    if self.option == 2 and self.options[2] == "RETURN":
                        menu.Menu(self.screen)
                    if self.option == 4 and self.options[4] == "QUIT_GAME":
                        sys.exit()

        if self.option > len(self.options)-1:
            self.option = 0
        if self.option < 0:
            self.option = len(self.options)-1

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
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
