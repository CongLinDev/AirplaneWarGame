import pygame
import abc
import flywight
import random

class Supply:
    __metaclass__= abc.ABCMeta #抽象类
    @abc.abstractmethod
    def move(self):
        pass
    @abc.abstractmethod
    def reset(self):
        pass
    @abc.abstractmethod
    def drawSupply(self, screen, clientPlane):
        pass

class Bullet_Supply(Supply, pygame.sprite.Sprite):
    def __init__(self, bg_size, flyWight):
        Supply.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.flyWight = flyWight
        self.image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100
        self.speed = 2
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
            
    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100

    def drawSupply(self, screen, clientPlane):
        if self.active:
            self.move()
            screen.blit(self.image, self.rect)
            if pygame.sprite.collide_mask(self, clientPlane):
                self.flyWight.get_bullet_sound.play()
                clientPlane.is_double_bullet = True
                pygame.time.set_timer(self.flyWight.DOUBLE_BULLET_TIME, 18 * 1000)
                self.active = False

class Bomb_Supply(Supply, pygame.sprite.Sprite):
    def __init__(self, bg_size, flyWight):
        Supply.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100
        self.flyWight = flyWight
        self.speed = 2
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.active = False
    def reset(self):
        self.active = True
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), -100

    def drawSupply(self, screen, clientPlane):
        if self.active:
            self.move()
            screen.blit(self.image, self.rect)
            if pygame.sprite.collide_mask(self, clientPlane):
                self.flyWight.get_bomb_sound.play()
                clientPlane.increaseBombNum()#增加炸弹
                self.active = False
        bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.Font("font/font.ttf", 48)
        bomb_text = bomb_font.render(" X %d" % clientPlane.bomb_num, True, self.flyWight.WHITE)
        text_rect = bomb_text.get_rect()
        screen.blit(bomb_image, (10, self.height - 10 - bomb_rect.height))
        screen.blit(bomb_text, (20 + bomb_rect.width, self.height - 5 - text_rect.height))