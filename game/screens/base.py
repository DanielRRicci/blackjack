import pygame

class BaseScreen:
    def __init__(self, screen, assets):
        self.screen = screen
        self.assets = assets

    def run(self):
        raise NotImplementedError("The run method must be implemented by subclasses.")