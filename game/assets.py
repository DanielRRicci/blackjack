import pygame
import os
import sys

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)




def load_assets():
    assets = {}

    ################# LOAD FONTS #################
    font_path = resource_path("assets/font/BJ_Font.ttf")

    assets["font_20"] = pygame.font.Font(font_path, 20)
    assets["font_30"] = pygame.font.Font(font_path, 30)
    assets["font_50"] = pygame.font.Font(font_path, 50)
    assets["font_70"] = pygame.font.Font(font_path, 70)
    assets["font_100"] = pygame.font.Font(font_path, 100)
    assets["font_150"] = pygame.font.Font(font_path, 150)

    ################# LOAD BACKGROUND IMAGE #################

    assets["board"] = pygame.image.load(resource_path("graphics/BJB.png")).convert()

    ################# LOAD CARD IMAGES #################
    ############## CARD BACK
    assets["card_back"] = pygame.image.load(resource_path("graphics/blueback.png")).convert()

    ############## NUMBERED/FACE CARDS
    assets["cards"] = {}
    suits = ['c', 'd', 'h', 's']
    for i in range(1, 14):
        for suit in suits:
            name = f"{i}{suit}"
            path = resource_path(f"graphics/{name}.png")
            assets["cards"][name] = pygame.image.load(path).convert()

    return assets