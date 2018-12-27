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


def readyForGame(clock, flyWight, enemy_plane):
    levelButtons = (\
        button.Button(flyWight.level_1_image),\
        button.Button(flyWight.level_2_image),\
        button.Button(flyWight.level_3_image),\
        )
    top = 300
    for each in levelButtons:
        each.layOut(((bg_size[0] - each.rect.width) // 2, top))
        top += 100
    levelButtons[0].setListener(level.Level_1(enemy_plane, bg_size))
    levelButtons[1].setListener(level.Level_2(enemy_plane, bg_size))
    levelButtons[2].setListener(level.Level_3(enemy_plane, bg_size))

    while True:
        clock.tick(60)
        pygame.display.update()
        screen.blit(flyWight.background, (0, 0))
        gamestart_text = flyWight.start_font.render("Welecome to Airplane War", True, flyWight.WHITE)
        gamestart_text_rect = gamestart_text.get_rect()
        gamestart_text_rect.left, gamestart_text_rect.top = (width - gamestart_text_rect.width) // 2, 100
        screen.blit(gamestart_text, gamestart_text_rect)

        for each in levelButtons:
            each.showImage(screen)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type ==  MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for each in levelButtons:
                    if each.isClicked(pos):
                        return each.done()
        pygame.display.flip()

def gameOver(clock, flyWight, score):
    pygame.mixer.music.stop()
    pygame.mixer.stop()
    gameAgainButton = button.Button(flyWight.again_image)
    gameOverButton = button.Button(flyWight.gameover_image)
    pos_again = (bg_size[0] - gameAgainButton.rect.width) // 2, 400
    gameAgainButton.layOut(pos_again)
    pos_gameOver = (bg_size[0] - gameOverButton.rect.width) // 2, 500
    gameOverButton.layOut(pos_gameOver)

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
                if gameAgainButton.isClicked(pos):
                    main()
                elif gameOverButton.isClicked(pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.flip()

def main():  
    clock = pygame.time.Clock()
    pygame.mixer.music.play(-1)
    flyWight = flywight.Common_FlyWight()
    #生成飞机
    me = plane_factory.ClientPlaneFactory.createPlane(bg_size)#生成我方飞机
    enemy_plane = pygame.sprite.Group()#敌方飞机集合
    #获取用户设置的关卡等级，以此用于敌军集合的生成，且生成敌军
    readyForGame(clock, flyWight, enemy_plane)
    #生成子弹
    bulletGroup = bullet.BulletGroup(me)
    #给飞机装配子弹
    me.fire_command = command.FireBulletCommand(bulletGroup)
    #生成补给
    bullet_supply = supply.Bullet_Supply(bg_size)
    bomb_supply = supply.Bomb_Supply(bg_size)
    supplyFlyWight = flywight.Supply_FlyWight()
    pygame.time.set_timer(supplyFlyWight.SUPPLY_TIME, 30 * 1000)
    #生成障碍物
    aerolite_barrier = barrier.Aerolite_Barrier(bg_size)
    barrierFlyWight = flywight.Aerolite_Barrier_FlyWight()
    pygame.time.set_timer(barrierFlyWight.BARRIER_TIME, 10 * 1000)

    score = 0#统计得分   
    delay = 100#延迟

    while me.life_num:
        #TODO：对事件进行分析
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:#键盘事件
                if event.key == K_SPACE:#空格键  使用炸弹
                    if me.bomb_num:#使用炸弹
                        me.bomb_num -= 1
                        supplyFlyWight.bomb_sound.play()
                        if aerolite_barrier.rect.bottom > 0:
                            aerolite_barrier.active = False#在界面中的障碍物
                        for each in enemy_plane:
                            if each.rect.bottom > 0:#在界面中的敌机
                                each.active = False
            elif event.type == supplyFlyWight.SUPPLY_TIME:#补给时间
                supplyFlyWight.supply_sound.play()
                #随机生成补给
                if random.choice([True, False]):
                    bullet_supply.reset()
                else:
                    bomb_supply.reset()
            elif event.type == supplyFlyWight.DOUBLE_BULLET_TIME:
                me.is_double_bullet = False
                pygame.time.set_timer(supplyFlyWight.DOUBLE_BULLET_TIME, 0)
            elif event.type == barrierFlyWight.BARRIER_TIME:
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
            me.fireBullet()
        #检测子弹是否击中物体
        bulletGroup.hitPlaneAndBarrier(screen, enemy_plane, aerolite_barrier)
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