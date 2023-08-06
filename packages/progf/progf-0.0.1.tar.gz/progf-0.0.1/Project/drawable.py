import pygame


class Image:
    def __init__(self, image, size):
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.size = size

    def update(self):
        self.image = pygame.transform.scale(pygame.image.load(self.image), self.size)


class Color:
    def __init__(self, red, green, blue):
        self.color = (red, green, blue)
