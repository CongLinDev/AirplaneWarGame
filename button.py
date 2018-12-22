import abc
import pygame
import level

class Button:
    __metaclass__= abc.ABCMeta #抽象类

    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def isClickButton(self, pos):
        in_x = self.rect.left < pos[0] < self.rect.right
        in_y = self.rect.top < pos[1] < self.rect.bottom
        return in_x and in_y

    def showImage(self, screen):
        screen.blit(self.image, self.rect)

    @abc.abstractmethod
    def function(self):
        pass

class Level_1_Button(Button):
    def __init__(self, flyWight, bg_size):
        flyWight.level_1_rect.left = (bg_size[0] - flyWight.level_1_rect.width) // 2
        flyWight.level_1_rect.top = 300
        Button.__init__(self,flyWight.level_1_image, flyWight.level_1_rect)
    
    def function(self):
        return level.Level_1()

class Level_2_Button(Button):
    def __init__(self, flyWight, bg_size):
        flyWight.level_2_rect.left = (bg_size[0] - flyWight.level_2_rect.width) // 2
        flyWight.level_2_rect.top = 400
        Button.__init__(self,flyWight.level_2_image, flyWight.level_2_rect)
    
    def function(self):
        return level.Level_2()

class Level_3_Button(Button):
    def __init__(self, flyWight, bg_size):
        flyWight.level_3_rect.left = (bg_size[0] - flyWight.level_3_rect.width) // 2
        flyWight.level_3_rect.top = 500
        Button.__init__(self,flyWight.level_3_image, flyWight.level_3_rect)
    
    def function(self):
        return level.Level_3()

class GameAgainButton(Button):
    def __init__(self, flyWight, bg_size):
        flyWight.again_rect.left = (bg_size[0] - flyWight.again_rect.width) // 2
        flyWight.again_rect.top = 400
        Button.__init__(self,flyWight.again_image, flyWight.again_rect)
    def function(self):#重新开始
        return True

class GameOverButton(Button):
    def __init__(self, flyWight, bg_size):
        flyWight.gameover_rect.left = (bg_size[0] - flyWight.gameover_rect.width) // 2
        flyWight.gameover_rect.top = 500
        Button.__init__(self,flyWight.gameover_image, flyWight.gameover_rect)
    def function(self):#结束
        return True   
        