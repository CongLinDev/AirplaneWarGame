#coding=utf-8
import pygame
import sys
import traceback
import plane_factory
import bullet_factory
import bullet
import level
import supply
import random
import barrier
import flywight
import command
import button
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)

def readyForGame(clock, flyWight):
    level1Button = button.Level_1_Button(flyWight, bg_size)
    level2Button = button.Level_2_Button(flyWight, bg_size)
    level3Button = button.Level_3_Button(flyWight, bg_size)
    while True:
        clock.tick(60)
        pygame.display.update()
        screen.blit(flyWight.background, (0, 0))
        gamestart_text = flyWight.start_font.render("Welecome to Airplane War", True, flyWight.WHITE)
        gamestart_text_rect = gamestart_text.get_rect()
        gamestart_text_rect.left, gamestart_text_rect.top = (width - gamestart_text_rect.width) // 2, 100
        screen.blit(gamestart_text, gamestart_text_rect)
        level1Button.showImage(screen)
        level2Button.showImage(screen)
        level3Button.showImage(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type ==  MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if level1Button.isClickButton(pos):
                    return level1Button.function()
                elif level2Button.isClickButton(pos):
                    return level2Button.function()
                elif level3Button.isClickButton(pos):
                    return level3Button.function()
        pygame.display.flip()

def gameOver(clock, flyWight, score):
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    gameAgainButton = button.GameAgainButton(flyWight, bg_size)
    gameOverButton = button.GameOverButton(flyWight, bg_size)
    while True:
        clock.tick(60)
        pygame.display.update()

        screen.blit(flyWight.background, (0, 0))
        gameover_text1 = flyWight.gameover_font.render("Your Score", True, flyWight.WHITE)
        gameover_text1_rect = gameover_text1.get_rect()
        gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, 200
        screen.blit(gameover_text1, gameover_text1_rect)
        gameover_text2 = flyWight.gameover_font.render(str(score), True, flyWight.WHITE)
        gameover_text2_rect = gameover_text2.get_rect()
        gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, 300
        screen.blit(gameover_text2, gameover_text2_rect)

        gameAgainButton.showImage(screen)
        gameOverButton.showImage(screen)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type ==  MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if gameAgainButton.isClickButton(pos):
                    main()
                elif gameOverButton.isClickButton(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    flyWight = flywight.FlyWight()#享元
    #获取用户设置的等级
    currentLevel = readyForGame(clock, flyWight)
    #生成飞机
    me = plane_factory.ClientPlaneFactory.createPlane(bg_size, flyWight)#生成我方飞机
    enemy_plane = pygame.sprite.Group()#敌方飞机集合
    #生成子弹
    bulletGroup = bullet.BulletGroup(me, flyWight)
    #给飞机装配子弹
    me.fire_command = command.FireBulletCommand(bulletGroup)
    #调整等级
    currentLevel.changeLevel(bg_size, enemy_plane, flyWight)
    #生成补给
    bullet_supply = supply.Bullet_Supply(bg_size, flyWight)
    bomb_supply = supply.Bomb_Supply(bg_size, flyWight)
    pygame.time.set_timer(flyWight.SUPPLY_TIME, 30 * 1000)
    #生成障碍物
    aerolite_barrier = barrier.Aerolite_Barrier(bg_size, flyWight)
    pygame.time.set_timer(flyWight.BARRIER_TIME, 10 * 1000)

    score = 0#统计得分   
    delay = 100#延迟

    while me.life_num:
        #TODO：对事件进行分析
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:#键盘事件
                if event.key == K_SPACE:#空格键
                    if me.bomb_num:#使用炸弹
                        me.bomb_num -= 1
                        flyWight.bomb_sound.play()
                        aerolite_barrier.active = False
                        for each in enemy_plane:
                            if each.rect.bottom > 0:#在界面中的敌机
                                each.active = False
            elif event.type == flyWight.SUPPLY_TIME:#补给时间
                flyWight.supply_sound.play()
                #随机生成补给
                if random.choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
            elif event.type == flyWight.DOUBLE_BULLET_TIME:
                me.is_double_bullet = False
                pygame.time.set_timer(flyWight.DOUBLE_BULLET_TIME, 0)
            elif event.type == flyWight.BARRIER_TIME:
                aerolite_barrier.reset()
        
        screen.blit(flyWight.background, (0, 0))
        #检测键盘操作
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            me.moveUp()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            me.moveDown()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            me.moveLeft()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            me.moveRight()
        #绘制补给
        bullet_supply.drawSupply(screen, me)
        bomb_supply.drawSupply(screen, me)
        #绘制障碍物
        aerolite_barrier.drawBarrier(screen, me)
        #发射子弹
        if not (delay % 10):
            bullets = me.fireBullet()
        #检测子弹是否击中敌机
        bullet.Bullet.hit_enemy_plane(bullets, screen, enemy_plane)
        #绘制敌机
        for each in enemy_plane:
            getScore = each.drawPlane(screen, delay)
            if getScore != 0:
                score += getScore
                each.reset()
        #检测客户机是否被撞
        me.checkPlane(enemy_plane)           
        #绘制客户机
        getScore = me.drawPlane(screen, delay)
        score += getScore
        #画出生命值和分数
        me.drawLifeNumAndScore(screen, flyWight.score_font, score)

        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)

    gameOver(clock, flyWight, score)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()