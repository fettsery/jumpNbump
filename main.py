#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import pygame, menu
from constants import *

pygame.init()
pygame.mouse.set_visible(0)
pygame.display.set_caption("jumpNbump")
menu.Menu(pygame.display.set_mode((SCREEN_LENGTH, SCREEN_HIGHT)))