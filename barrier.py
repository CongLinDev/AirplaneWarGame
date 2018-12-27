import pygame
import abc
import random
import flywight
class Barrier:
    __metaclass__= abc.ABCMeta #抽象类
    @abc.abstractmethod
    def move(self):
        pass
    def reset(self):
        pass
    @abc.abstractmethod
    def drawBarrier(self, screen, clientPlane):
        pass

#陨石
class Aerolite_Barrier(Barrier, pygame.sprite.Sprite):
    def __init__(self, bg_size):
        Barrier.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.flyWight = flywight.Aerolite_Barrier_FlyWight()
        self.image = self.flyWight.aerolite_barrier_image
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), 0
        self.speed = 2
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)
        self.is_move_left = random.choice([True, False])

    def move(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
            if self.is_move_left:
                self.rect.left += (self.speed / 2)
            else:
                self.rect.left -= (self.speed / 2)
        else:
            self.active = False
            
    def reset(self):
        self.active = True
        self.is_move_left = random.choice([True, False])
        self.rect.left, self.rect.bottom = \
                        random.randint(0, self.width - self.rect.width), 0

    def drawBarrier(self, screen, clientPlane):
        if self.active:
            self.move()
            screen.blit(self.image, self.rect)
            if pygame.sprite.collide_mask(self, clientPlane):
                clientPlane.active = False
                pygame.time.set_timer(self.flyWight.BARRIER_TIME, 10 * 1000)
                self.active = False

