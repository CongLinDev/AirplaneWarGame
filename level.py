import plane_factory
import flywight
import button
import abc

class Level:
    __metaclass__= abc.ABCMeta #抽象类
    def changeLevel():
        pass
    def done(self):
        pass

class Level_1(Level, button.ButtonListener):
    def __init__(self, enemy_plane, bg_size):
        Level.__init__(self)
        button.ButtonListener.__init__(self)
        self.enemy_plane = enemy_plane
        self.bg_size = bg_size
    def changeLevel(self):
        self.enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(self.bg_size, self.enemy_plane, 8)
        plane_factory.EnemyPlane2Factory.createNumPlane(self.bg_size, self.enemy_plane, 2)
        plane_factory.EnemyPlane3Factory.createNumPlane(self.bg_size, self.enemy_plane, 1)
        self.enemy_plane.update(1)#设置速度均为1
    def done(self):
        self.changeLevel()

class Level_2(Level, button.ButtonListener):
    def __init__(self, enemy_plane, bg_size):
        Level.__init__(self)
        button.ButtonListener.__init__(self)
        self.flyWight = flywight.Common_FlyWight()
        self.enemy_plane = enemy_plane
        self.bg_size = bg_size
    def changeLevel(self):
        self.enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(self.bg_size, self.enemy_plane, 12)
        plane_factory.EnemyPlane2Factory.createNumPlane(self.bg_size, self.enemy_plane, 4)
        plane_factory.EnemyPlane3Factory.createNumPlane(self.bg_size, self.enemy_plane, 2)
        self.enemy_plane.update(2)#设置速度为2
    def done(self):
        self.changeLevel()


class Level_3(Level, button.ButtonListener):
    def __init__(self, enemy_plane, bg_size):
        Level.__init__(self)
        button.ButtonListener.__init__(self)
        self.bg_size = bg_size
        self.enemy_plane = enemy_plane
    def changeLevel(self):
        self.enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(self.bg_size, self.enemy_plane, 16)
        plane_factory.EnemyPlane2Factory.createNumPlane(self.bg_size, self.enemy_plane, 8)
        plane_factory.EnemyPlane3Factory.createNumPlane(self.bg_size, self.enemy_plane, 4)
        self.enemy_plane.update(2)#设置速度为2
    def done(self):
        self.changeLevel()
        