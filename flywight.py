import pygame
#纯函数式使用元类
#type(类名, 父类的元组（针对继承的情况，可以为空），包含属性的字典（名称和值）)
metaflyweight = lambda name, parents, attrs: type(
        name,
        parents,
        dict(attrs.items() + [
            ('__instances', dict()),
            ('__new__', classmethod(
                lambda cls, *args, **kargs: cls.__instances.setdefault(#setdefault() 键如果不在字典中，会更新字典
                                tuple(args),
                                super(type(cls), cls).__new__(*args, **kargs))
                )
            )
        ])
    )

class Common_FlyWight:
    __metaclass__ = metaflyweight
    def __init__(self):
        #颜色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        #背景图
        self.bg_size = self.width, self.height = 480, 700
        self.background = pygame.image.load("images/background.png").convert()
        pygame.mixer.init()
        #升级声音
        self.upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
        self.upgrade_sound.set_volume(0.2)
        #开始界面
        self.start_font = pygame.font.Font("font/font.TTF", 42)
        self.level_1_image = pygame.image.load("images/level_1.png").convert_alpha()
        self.level_2_image = pygame.image.load("images/level_2.png").convert_alpha()
        self.level_3_image = pygame.image.load("images/level_3.png").convert_alpha()
        self.level_1_rect = self.level_1_image.get_rect()
        self.level_2_rect = self.level_2_image.get_rect()
        self.level_3_rect = self.level_3_image.get_rect()
        #结束界面
        self.again_image = pygame.image.load("images/again.png").convert_alpha()
        self.again_rect = self.again_image.get_rect()
        self.gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
        self.gameover_rect = self.gameover_image.get_rect()
        self.gameover_font = pygame.font.Font("font/font.TTF", 48)
        #分数的字体
        self.score_font = pygame.font.Font("font/font.ttf", 36)

class ClientPlane_FlyWight:
    __metaclass__ = metaflyweight

    def __init__(self):
        #客户端飞机图片
        self.client_plane_image1 = pygame.image.load("images/me1.png").convert_alpha()
        self.client_plane_image2 = pygame.image.load("images/me2.png").convert_alpha()
        self.client_plane_destroy_images = []
        self.client_plane_destroy_images.extend([\
            pygame.image.load("images/me_destroy_1.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_2.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_3.png").convert_alpha(), \
            pygame.image.load("images/me_destroy_4.png").convert_alpha() \
            ])
        #客户端飞机击落声音
        self.client_plane_down_sound = pygame.mixer.Sound("sound/me_down.wav")
        self.client_plane_down_sound.set_volume(0.2)
        #客户端生命图片
        self.client_plane_life_image = pygame.image.load("images/life.png").convert_alpha()
        #颜色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        #事件
        self.INVINCIBLE_TIME = pygame.USEREVENT + 2

class EnemyPlane1_FlyWight:
    __metaclass__ = metaflyweight
    def __init__(self):
        #敌机1图片
        self.enemy_plane_1_image = pygame.image.load("images/enemy1.png").convert_alpha()
        self.enemy_plane_1_destroy_images = []
        self.enemy_plane_1_destroy_images.extend([\
            pygame.image.load("images/enemy1_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy1_down4.png").convert_alpha() \
            ])
        self.enemy_plane_1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
        self.enemy_plane_1_down_sound.set_volume(0.2)
        self.enemy_plane_1_energy = 1


class EnemyPlane2_FlyWight:
    __metaclass__ = metaflyweight
    def __init__(self):
        #敌机2图片
        self.enemy_plane_2_image = pygame.image.load("images/enemy2.png").convert_alpha()
        self.enemy_plane_2_hit_image = pygame.image.load("images/enemy2_hit.png").convert_alpha()
        self.enemy_plane_2_destroy_images = []
        self.enemy_plane_2_destroy_images.extend([\
            pygame.image.load("images/enemy2_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy2_down4.png").convert_alpha() \
            ])
        self.enemy_plane_2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
        self.enemy_plane_2_down_sound.set_volume(0.2)
        self.enemy_plane_2_energy = 5
        #颜色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

class EnemyPlane3_FlyWight:
    __metaclass__ = metaflyweight

    def __init__(self):
        #敌机3图片
        self.enemy_plane_3_image1 = pygame.image.load("images/enemy3_n1.png").convert_alpha()
        self.enemy_plane_3_image2 = pygame.image.load("images/enemy3_n2.png").convert_alpha()
        self.enemy_plane_3_hit_image = pygame.image.load("images/enemy3_hit.png").convert_alpha()
        self.enemy_plane_3_destroy_images = []
        self.enemy_plane_3_destroy_images.extend([\
            pygame.image.load("images/enemy3_down1.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down2.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down3.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down4.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down5.png").convert_alpha(), \
            pygame.image.load("images/enemy3_down6.png").convert_alpha() \
            ])
        self.enemy_plane_3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
        self.enemy_plane_3_down_sound.set_volume(0.5)
        self.enemy_plane_3_energy = 20
        self.enemy_plane_3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
        self.enemy_plane_3_fly_sound.set_volume(0.2)
        #颜色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

class Aerolite_Barrier_FlyWight:
    __metaclass__ = metaflyweight
    def __init__(self):
        #障碍物图片
        self.aerolite_barrier_image = pygame.image.load("images/aerolite.png").convert_alpha()
        # BARRIER_TIME
        self.BARRIER_TIME = pygame.USEREVENT + 3

class Supply_FlyWight:
    __metaclass__ = metaflyweight

    def __init__(self):
        self.SUPPLY_TIME = pygame.USEREVENT
        #子弹补给图片
        self.bullet_supply_image = pygame.image.load("images/bullet_supply.png").convert_alpha()
        #炸弹补给图片
        self.bomb_supply_image = pygame.image.load("images/bomb_supply.png").convert_alpha()
        #补给声音
        self.supply_sound = pygame.mixer.Sound("sound/supply.wav")
        self.supply_sound.set_volume(0.2)
        #获得炸弹 声音
        self.get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
        self.get_bomb_sound.set_volume(0.2)
        #获得子弹 声音
        self.get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
        self.get_bullet_sound.set_volume(0.2)
        #炸弹声音
        self.bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
        self.bomb_sound.set_volume(0.2)
        #事件
        self.DOUBLE_BULLET_TIME = pygame.USEREVENT + 1
        #颜色
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

class Bullet_FlyWight:
    __metaclass__ = metaflyweight
    def __init__(self):
        #一次性创建的子弹数量
        self.BULLET_NUM = 4
        #子弹图片
        self.bullet1_image = pygame.image.load("images/bullet1.png").convert_alpha()
        self.bullet2_image = pygame.image.load("images/bullet2.png").convert_alpha()
        #子弹声音
        self.bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
        self.bullet_sound.set_volume(0.2)

    
