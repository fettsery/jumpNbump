#!/usr/bin/env python
# coding=utf-8
# 2.7
#fettser.yury
import pygame, os
from sprites import *

def load_image(filename):
    filename = os.path.realpath(filename)
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, (image.get_width()*2, image.get_height()*2))
    except pygame.error:
        raise SystemExit, "Unable to load: " + filename
    return image.convert_alpha()

class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.create_level()
        self.Player = Player(0)
        self.clock = pygame.time.Clock()
        self.bg = load_image("background.png")
        self.level = Level()
        self.font = pygame.font.Font(os.path.realpath("fonts/font.ttf"), 16)
        self.running = True
        self.main_loop()
    def main_loop(self):
        while self.running:
            self.clock.tick(30)
            self.draw()
            pygame.display.flip()
    def create_level(self):
        self.objects = list()
        self.objects.append(Platform(self.screen, "bush-2.png", 0, 450))
        self.objects.append(Platform(self.screen, "bush-3.png", 50, 450))
        self.objects.append(Platform(self.screen, "bush-3.png", 100, 450))
        self.objects.append(Platform(self.screen, "lava.png", 160, 460))
        self.objects.append(Platform(self.screen, "lava.png", 200, 460))
        self.objects.append(Platform(self.screen, "lava.png", 240, 460))
        self.objects.append(Platform(self.screen, "bush-2.png", 270, 450))
        self.objects.append(Platform(self.screen, "bush-2.png", 340, 450))
        self.objects.append(Platform(self.screen, "bush-3.png", 400, 450))
        self.objects.append(Platform(self.screen, "lava.png", 460, 460))
        self.objects.append(Platform(self.screen, "lava.png", 500, 460))
        self.objects.append(Platform(self.screen, "bush-2.png", 560, 450))
        self.objects.append(Platform(self.screen, "brick1.png", 160, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 190, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 220, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 430, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 460, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 490, 360))
        self.objects.append(Platform(self.screen, "brick1.png", 520, 360))
        self.objects.append(Platform(self.screen, "brickblue1.png", 260, 280))
        self.objects.append(Platform(self.screen, "brickblue1.png", 290, 280))
        self.objects.append(Platform(self.screen, "brickblue1.png", 320, 280))
        self.objects.append(Platform(self.screen, "brickblue1.png", 520, 280))
        self.objects.append(Platform(self.screen, "brickblue1.png", 550, 280))
        self.objects.append(Platform(self.screen, "brickblue1.png", 580, 280))
        self.objects.append(Platform(self.screen, "brick1.png", 0, 280))
        self.objects.append(Platform(self.screen, "brick1.png", 30, 280))
        self.objects.append(Platform(self.screen, "brick1.png", 60, 280))
        self.objects.append(Platform(self.screen, "brick1.png", 90, 280))
        self.objects.append(Platform(self.screen, "brick1.png", 60, 180))
        self.objects.append(Platform(self.screen, "brick1.png", 90, 180))
        self.objects.append(Platform(self.screen, "brick1.png", 120, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 320, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 350, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 380, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 410, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 440, 180))
        self.objects.append(Platform(self.screen, "brickblue1.png", 470, 180))
        self.objects.append(Platform(self.screen, "cloud.png", 50, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 90, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 120, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 160, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 200, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 240, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 400, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 440, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 480, 50))
        self.objects.append(Platform(self.screen, "cloud.png", 520, 50))
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for i in self.objects:
            i.draw()

