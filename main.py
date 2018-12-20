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
from pygame.locals import *

pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("飞机大战")

pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)

def main():
    pygame.mixer.music.play(-1)

    flyWight = flywight.FlyWight()
    #生成飞机
    me = plane_factory.ClientPlaneFactory.createPlane(bg_size, flyWight)    #生成我方飞机
    enemy_plane = pygame.sprite.Group()#敌方飞机集合

    level.Level_3.changeLevel(bg_size, enemy_plane, flyWight)

    # level_1_rect.left, level_1_rect.top = (width - level_1_rect.width) // 2, height // 3
    # screen.blit(level_1_image, level_1_rect)
    # level_2_rect.left, level_2_rect.top = (width - level_2_rect.width) // 2, level_1_rect.top + level_1_rect.height
    # screen.blit(level_2_image, level_2_rect)
    # level_3_rect.left, level_3_rect.top = (width - level_3_rect.width) // 2, level_2_rect.top + level_3_rect.height
    # screen.blit(level_3_image, level_3_rect)
    # if pygame.mouse.get_pressed()[0]:
    #     pos = pygame.mouse.get_pos()
         
    #     if level_1_rect.left < pos[0] < level_1_rect.right and \ 
    #         level_1_rect.top < pos[1] < level_1_rect.bottom:# 如果用户点击“Level 1”
    #         level.Level_1.changeLevel(bg_size, enemy_plane, enemy_plane_1,\
    #             enemy_plane_2, enemy_plane_3)
    #     elif level_2_rect.left < pos[0] < level_2_rect.right and \
    #         level_2_rect.top < pos[1] < level_2_rect.bottom:# 如果用户点击“Level 2”
    #         level.Level_2.changeLevel(bg_size, enemy_plane, enemy_plane_1,\
    #             enemy_plane_2, enemy_plane_3)
    #     elif level_3_rect.left < pos[0] < level_3_rect.right and \
    #         level_3_rect.top < pos[1] < level_3_rect.bottom:# 如果用户点击“Level 3”
    #         level.Level_3.changeLevel(bg_size, enemy_plane, enemy_plane_1,\
    #             enemy_plane_2, enemy_plane_3)

    #生成补给
    bullet_supply = supply.Bullet_Supply(bg_size, flyWight)
    bomb_supply = supply.Bomb_Supply(bg_size, flyWight)
    pygame.time.set_timer(flyWight.SUPPLY_TIME, 30 * 1000)

    #生成障碍物
    aerolite_barrier = barrier.Aerolite_Barrier(bg_size, flyWight)
    pygame.time.set_timer(flyWight.BARRIER_TIME, 10 * 1000)

    clock = pygame.time.Clock()

    score = 0#统计得分
    score_font = pygame.font.Font("font/font.ttf", 36)

    delay = 100#延迟

    running = True
    while running:
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
        #TODO：具体操作
        if me.life_num:
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
            me.drawLifeNumAndScore(screen, score_font, score)

        elif me.life_num == 0:#游戏结束
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            gameover_rect = flyWight.gameover_image.get_rect()
            again_rect = flyWight.again_image.get_rect()

            gameover_text1 = flyWight.gameover_font.render("Your Score", True, flyWight.WHITE)
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (width - gameover_text1_rect.width) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)
            
            gameover_text2 = flyWight.gameover_font.render(str(score), True, flyWight.WHITE)
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (width - gameover_text2_rect.width) // 2, \
                                    gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (width - again_rect.width) // 2, \
                                gameover_text2_rect.bottom + 50
            screen.blit(flyWight.again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (width - again_rect.width) // 2, \
                                again_rect.bottom + 10
            screen.blit(flyWight.gameover_image, gameover_rect)
            #检测用户的鼠标操作
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                # 如果用户点击“重新开始”
                if again_rect.left < pos[0] < again_rect.right and \
                    again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                    gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()   

        delay -= 1
        if not delay:
            delay = 100
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()