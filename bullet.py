import pygame
import abc
import flywight
import bullet_factory
class Bullet:
    __metaclass__= abc.ABCMeta #抽象类

    @abc.abstractmethod
    def moveUp(self):
        pass

    @abc.abstractmethod
    def reset(self, position):
        pass

    @staticmethod
    def fireBullet(clientPlane, bullets, index):
        flyWight = flywight.Bullet_FlyWight()
        flyWight.bullet_sound.play()
        
        if clientPlane.is_double_bullet:
            bullets[index].reset((clientPlane.rect.centerx-33, clientPlane.rect.centery))
            bullets[index+1].reset((clientPlane.rect.centerx+30, clientPlane.rect.centery))
            index = (index + 2) % (len(bullets))
            return index
        else:
            bullets[index].reset(clientPlane.rect.midtop)
            index = (index + 1) % len(bullets)
            return index

class Bullet1(Bullet, pygame.sprite.Sprite):
    def __init__(self, position, flyWight):
        Bullet.__init__(self)
        pygame.sprite.Sprite.__init__(self)

        self.image = flyWight.bullet1_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 10
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def moveUp(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True

class Bullet2(Bullet):
    def __init__(self, position, flyWight):
        Bullet.__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.image = flyWight.bullet2_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.speed = 15
        self.active = False
        self.mask = pygame.mask.from_surface(self.image)

    def moveUp(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.active = False

    def reset(self, position):
        self.rect.left, self.rect.top = position
        self.active = True


class BulletGroup:
    def __init__(self, clientPlane):
        #生成子弹
        self.bullets = None
        self.bullet1 = []
        self.bullet2 = []
        self.bullet1_index = 0
        self.bullet2_index = 0
        bullet_factory.Bullet1Factory.creatNumBullet(clientPlane.rect.midtop, self.bullet1)
        bullet_factory.Bullet2Factory.creatNumBullet((clientPlane.rect.centerx-33, clientPlane.rect.centery), self.bullet2)
        bullet_factory.Bullet2Factory.creatNumBullet((clientPlane.rect.centerx+30, clientPlane.rect.centery), self.bullet2)
        self.clientPlane = clientPlane

    def fireBullet(self):
        if self.clientPlane.is_double_bullet:
            self.bullet2_index = Bullet.fireBullet(self.clientPlane, self.bullet2, self.bullet2_index)
            self.bullets = self.bullet2
        else:
            self.bullet1_index = Bullet.fireBullet(self.clientPlane, self.bullet1, self.bullet1_index)
            self.bullets = self.bullet1

    def hitPlaneAndBarrier(self, screen, enemy_plane, barrier):
        for bullet in self.bullets:
            if bullet.active:
                bullet.moveUp()
                screen.blit(bullet.image, bullet.rect)
                enemy_hit = pygame.sprite.spritecollide(bullet, enemy_plane, False, pygame.sprite.collide_mask)
                barrier_hit = pygame.sprite.collide_rect(bullet, barrier)
                if enemy_hit:
                    bullet.active = False
                    for enemy in enemy_hit:#对于每个受到攻击的敌机
                        enemy.hit = True
                        enemy.energy -= 1
                        if enemy.energy == 0:
                            enemy.active = False
                if barrier_hit:
                    bullet.active = False
