import pygame
import abc
import flywight
import random
import bullet

class Plane:
    __metaclass__= abc.ABCMeta #抽象类

    @abc.abstractmethod
    def moveUp(self):
        pass

    @abc.abstractmethod
    def moveDown(self):
        pass

    @abc.abstractmethod
    def moveLeft(self):
        pass

    @abc.abstractmethod
    def moveRight(self):
        pass

    @abc.abstractmethod
    def reset(self):
        pass

    @abc.abstractmethod
    def drawPlane(self, screen, delay):
        pass
    
    #@abc.abstractmethod
    def update(self, newSpeed):#用于更新飞机速度
        self.speed = newSpeed


class ClientPlane(pygame.sprite.Sprite, Plane):
    #发射子弹的方式

    def __init__(self, bg_size, flyWight):
        pygame.sprite.Sprite.__init__(self)
        Plane.__init__(self)
        self.flyWight = flyWight
        self.life_num = 3
        self.life_image = flyWight.client_plane_life_image
        self.life_rect = self.life_image.get_rect()

        self.image1 = flyWight.client_plane_image1
        self.image2 = flyWight.client_plane_image2
        self.destroy_images = flyWight.client_plane_destroy_images
        self.destroy_index = 0
        self.client_down_sound = flyWight.client_plane_down_sound

        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        self.speed = 3
        self.active = True
        self.invincible = False
        self.mask = pygame.mask.from_surface(self.image1)

        self.is_double_bullet = False#子弹发射方式
        self.bomb_num = 1#炸弹数
        #生成子弹
        self.bulletGroup = bullet.BulletGroup(self, flyWight)

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.bottom < self.height - 60:
            self.rect.top += self.speed
        else:
            self.rect.bottom = self.height - 60

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.rect.left, self.rect.top = \
                        (self.width - self.rect.width) // 2, \
                        self.height - self.rect.height - 60
        self.active = True
        self.invincible = True

    def drawPlane(self, screen, delay):
        if self.active:
            screen.blit(self.image1, self.rect)
        else:#毁灭
            if not(delay % 3):
                if self.destroy_index == 0:
                    self.client_down_sound.play()
                screen.blit(self.destroy_images[self.destroy_index], self.rect)
                self.destroy_index = (self.destroy_index + 1) % 4
                if self.destroy_index == 0:
                    self.life_num -= 1
                    self.reset()
                    pygame.time.set_timer(self.flyWight.INVINCIBLE_TIME, 3 * 1000)
                    return -10#返回的是得到的分数
        return 0#返回的是得到的分数

    #检测飞机是否被撞，或是被子弹打中
    def checkPlane(self, enemy):
        enemies_down = pygame.sprite.spritecollide(self, enemy, False, pygame.sprite.collide_mask)
        if enemies_down:
            self.active = False
            for e in enemies_down:
                e.active = False

    #绘制剩余生命数量和分数  
    def drawLifeNumAndScore(self, screen, score_font, score):
        if self.life_num:
            for i in range(self.life_num):
                screen.blit(self.life_image, \
                    (self.width-10-(i+1)*self.life_rect.width, \
                    self.height-10-self.life_rect.height))

        score_text = score_font.render("Score : %s" % str(score), True, self.flyWight.WHITE)
        screen.blit(score_text, (10, 5))
    
    def increaseBombNum(self):#炸弹数不得超过三个
        if self.bomb_num < 3:
            self.bomb_num += 1
    def fireBullet(self):
        return self.bulletGroup.fireBullet()


class EnemyPlane1(pygame.sprite.Sprite, Plane):  
    def __init__(self, bg_size, flyWight):
        pygame.sprite.Sprite.__init__(self)
        Plane.__init__(self)
        self.image = flyWight.enemy_plane_1_image
        self.destroy_images = flyWight.enemy_plane_1_destroy_images
        self.e_destroy_index = 0#毁灭时的图片索引，用于播放毁灭图像
        self.enemy1_down_sound = flyWight.enemy_plane_1_down_sound
        self.energy = flyWight.enemy_plane_1_energy#能量
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-5 * self.height, 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.hit = False

    def moveUp(self):#向上移动
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.energy = 1       
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-5 * self.height, 0)

    def drawPlane(self, screen, delay):
        if self.active:
            self.moveDown()
            screen.blit(self.image, self.rect)
        else: #毁灭
            if not(delay % 3):
                if self.e_destroy_index == 0:
                    self.enemy1_down_sound.play()
                screen.blit(self.destroy_images[self.e_destroy_index], self.rect)
                self.e_destroy_index = (self.e_destroy_index + 1) % 4
                if self.e_destroy_index == 0:
                    return 1#返回的是得到的分数
        return 0#返回的是得到的分数

class EnemyPlane2(pygame.sprite.Sprite, Plane): 
    def __init__(self, bg_size, flyWight):
        pygame.sprite.Sprite.__init__(self)
        Plane.__init__(self)
        self.flyWight = flyWight
        self.image = flyWight.enemy_plane_2_image
        self.image_hit = flyWight.enemy_plane_2_hit_image
        self.destroy_images = flyWight.enemy_plane_2_destroy_images
        self.e_destroy_index = 0#毁灭时的图片索引，用于播放毁灭图像
        self.enemy2_down_sound = flyWight.enemy_plane_2_down_sound
        self.energy = flyWight.enemy_plane_2_energy#能量
        self.rect = self.image.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-10 * self.height, -self.height)
        self.mask = pygame.mask.from_surface(self.image)
        self.hit = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.energy = self.flyWight.enemy_plane_2_energy
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-10 * self.height, -self.height)

    def drawPlane(self, screen, delay):
        if self.active:
            self.moveDown()
            if self.hit:
                screen.blit(self.image_hit, self.rect)              
                self.hit = False
            else:
                screen.blit(self.image, self.rect)
            #绘制血槽
            pygame.draw.line(screen, self.flyWight.BLACK, \
                    (self.rect.left, self.rect.top - 5), \
                    (self.rect.right, self.rect.top - 5), 2)          
            #当生命大于20%显示绿色，否则显示红色
            energy_remain = self.energy / self.flyWight.enemy_plane_2_energy
            if energy_remain > 0.2:
                energy_color = self.flyWight.GREEN
            else:
                energy_color = self.flyWight.RED
            pygame.draw.line(screen, energy_color, \
                (self.rect.left, self.rect.top - 5), \
                (self.rect.left + self.rect.width * energy_remain, \
                self.rect.top - 5), 2)
        else: #毁灭
            if not(delay % 3):
                if self.e_destroy_index == 0:
                    self.enemy2_down_sound.play()
                screen.blit(self.destroy_images[self.e_destroy_index], self.rect)
                self.e_destroy_index = (self.e_destroy_index + 1) % 4
                if self.e_destroy_index == 0:
                    return 3#返回的是得到的分数
        return 0#返回的是得到的分数

class EnemyPlane3(pygame.sprite.Sprite, Plane):
    
    def __init__(self, bg_size, flyWight):
        pygame.sprite.Sprite.__init__(self)
        Plane.__init__(self)
        self.flyWight = flyWight
        self.image1 = flyWight.enemy_plane_3_image1
        self.image2 = flyWight.enemy_plane_3_image2
        self.enemy3_fly_sound = flyWight.enemy_plane_3_fly_sound
        self.image_hit = flyWight.enemy_plane_3_hit_image
        self.destroy_images = flyWight.enemy_plane_3_destroy_images
        self.e_destroy_index = 0#毁灭时的图片索引，用于播放毁灭图像
        self.enemy3_down_sound = flyWight.enemy_plane_3_down_sound
        self.enemy3_down_sound.set_volume(0.5)
        self.energy = flyWight.enemy_plane_3_energy#能量
        self.rect = self.image1.get_rect()
        self.width, self.height = bg_size[0], bg_size[1]
        self.speed = 1
        self.active = True
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-15 * self.height, -5 * self.height)
        self.mask = pygame.mask.from_surface(self.image1)
        self.hit = False

    def moveUp(self):
        if self.rect.top > 0:
            self.rect.top -= self.speed
        else:
            self.rect.top = 0

    def moveDown(self):
        if self.rect.top < self.height:
            self.rect.top += self.speed
        else:
            self.reset()

    def moveLeft(self):
        if self.rect.left > 0:
            self.rect.left -= self.speed
        else:
            self.rect.left = 0

    def moveRight(self):
        if self.rect.right < self.width:
            self.rect.left += self.speed
        else:
            self.rect.right = self.width

    def reset(self):
        self.active = True
        self.energy = self.flyWight.enemy_plane_3_energy
        self.rect.left, self.rect.top = \
                        random.randint(0, self.width - self.rect.width), \
                        random.randint(-15 * self.height, -5 * self.height)

    def drawPlane(self, screen, delay):
        if self.active:
            self.moveDown()
            if self.hit:
                screen.blit(self.image_hit, self.rect)              
                self.hit = False
            else:
                screen.blit(self.image1, self.rect)
            #绘制血槽
            pygame.draw.line(screen, self.flyWight.BLACK, \
                    (self.rect.left, self.rect.top - 5), \
                    (self.rect.right, self.rect.top - 5), 2)          
            #当生命大于20%显示绿色，否则显示红色
            energy_remain = self.energy / self.flyWight.enemy_plane_3_energy
            if energy_remain > 0.2:
                energy_color = self.flyWight.GREEN
            else:
                energy_color = self.flyWight.RED
            pygame.draw.line(screen, energy_color, \
                (self.rect.left, self.rect.top - 5), \
                (self.rect.left + self.rect.width * energy_remain, \
                self.rect.top - 5), 2)
            if self.rect.bottom == -50:#即将出现时，播放出场音乐
                self.enemy3_fly_sound.play(-1)
        else: #毁灭
            if not(delay % 3):
                if self.e_destroy_index == 0:
                    self.enemy3_down_sound.play()
                screen.blit(self.destroy_images[self.e_destroy_index], self.rect)
                self.e_destroy_index = (self.e_destroy_index + 1) % 6
                if self.e_destroy_index == 0:
                    self.enemy3_fly_sound.stop()
                    return 10#返回的是得到的分数
        return 0#返回的是得到的分数
  