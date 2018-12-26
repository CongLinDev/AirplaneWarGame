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
    def fireBullet(flyWight, clientPlane, bullets, index):
        flyWight.bullet_sound.play()
        
        if clientPlane.is_double_bullet:
            bullets[index].reset((clientPlane.rect.centerx-33, clientPlane.rect.centery))
            bullets[index+1].reset((clientPlane.rect.centerx+30, clientPlane.rect.centery))
            index = (index + 2) % (flyWight.BULLET_NUM * 2)
            return index
        else:
            bullets[index].reset(clientPlane.rect.midtop)
            index = (index + 1) % flyWight.BULLET_NUM
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
    def __init__(self, clientPlane, flyWight):
        #生成子弹
        self.bullets = None
        self.bullet1 = []
        self.bullet2 = []
        self.bullet1_index = 0
        self.bullet2_index = 0
        bullet_factory.Bullet1Factory.creatNumBullet(clientPlane.rect.midtop, flyWight, self.bullet1)
        bullet_factory.Bullet2Factory.creatNumBullet((clientPlane.rect.centerx-33, clientPlane.rect.centery), flyWight, self.bullet2)
        bullet_factory.Bullet2Factory.creatNumBullet((clientPlane.rect.centerx+30, clientPlane.rect.centery), flyWight, self.bullet2)
        self.flyWight = flyWight
        self.clientPlane = clientPlane

    def fireBullet(self):
        if self.clientPlane.is_double_bullet:
            self.bullet2_index = Bullet.fireBullet(self.flyWight, self.clientPlane, self.bullet2, self.bullet2_index)
            self.bullets = self.bullet2
        else:
            self.bullet1_index = Bullet.fireBullet(self.flyWight, self.clientPlane, self.bullet1, self.bullet1_index)
            self.bullets = self.bullet1

    def hitPlane(self, screen, enemy_plane):
        for bullet in self.bullets:
            if bullet.active:
                bullet.moveUp()
                screen.blit(bullet.image, bullet.rect)
                enemy_hit = pygame.sprite.spritecollide(bullet, enemy_plane, False, pygame.sprite.collide_mask)
                if enemy_hit:
                    bullet.active = False
                    for enemy in enemy_hit:#对于每个受到攻击的敌机
                        enemy.hit = True
                        enemy.energy -= 1
                        if enemy.energy == 0:
                            enemy.active = False
