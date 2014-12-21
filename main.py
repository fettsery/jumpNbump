#!/usr/bin/env python
# coding=utf-8
# 2.7
#fettser.yury
import pygame, menu

pygame.init()
pygame.mouse.set_visible(0)
pygame.display.set_caption("jumpNbump")
screen = pygame.display.set_mode((640, 480))
menu.Menu(screen)