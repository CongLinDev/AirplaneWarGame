import abc
import pygame
import level
 
class ButtonListener:
    __metaclass__= abc.ABCMeta

    @abc.abstractmethod 
    def done(self):
        pass

class Button:
    def __init__(self, image):
        self.image = image
        self.rect = image.get_rect()

    def layOut(self, pos):
        self.rect.left, self.rect.top = pos[0], pos[1]

    def setListener(self, listener):
        self.listener = listener
    
    def setImage(self, image):
        self.image = image

    def isClicked(self, pos):
        in_x = self.rect.left < pos[0] < self.rect.right
        in_y = self.rect.top < pos[1] < self.rect.bottom
        return in_x and in_y

    def showImage(self, screen):
        screen.blit(self.image, self.rect)

    def done(self):
        self.listener.done()