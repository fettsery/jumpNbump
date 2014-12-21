__author__ = 'User'
#!/usr/bin/env python
# coding=utf-8
# 2.7
#fettser.yury
import game
class Player:
    def __init__(self, num):
        pass

class Level:
    def __init__(self):
        pass

class Platform:
    def __init__(self, screen, image, posx, posy):
        self.screen = screen
        self.image = game.load_image(image)
        self.posx = posx
        self.posy = posy
    def draw(self):
        self.screen.blit(self.image, (self.posx, self.posy))