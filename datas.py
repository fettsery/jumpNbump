#!/usr/bin/env python
# coding=utf-8
# 2.7
# fettser.yury
import os, pygame

def load_image(filename):
    """
    loading image from file
    :param filename: -name of input file
    :return:
    """
    filename = os.path.realpath(filename)
    try:
        image = pygame.image.load(filename)
        image = pygame.transform.scale(image, \
                                       (image.get_width() * 2, image.get_height() * 2))
    except pygame.error:
        raise SystemExit("Unable to load: " + filename)
    return image.convert_alpha()