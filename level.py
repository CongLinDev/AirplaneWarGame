import plane_factory
import abc

class Level:
    __metaclass__= abc.ABCMeta #抽象类

    @staticmethod
    def changeLevel(bg_size, enemy_plane, flyWight):
        pass

class Level_1(Level):
    @staticmethod
    def changeLevel(bg_size, enemy_plane, flyWight):
        enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(bg_size, flyWight, enemy_plane, 8)
        plane_factory.EnemyPlane2Factory.createNumPlane(bg_size, flyWight, enemy_plane, 2)
        plane_factory.EnemyPlane3Factory.createNumPlane(bg_size, flyWight, enemy_plane, 1)
        enemy_plane.update(1)#设置速度均为1

class Level_2(Level):
    @staticmethod
    def changeLevel(bg_size, enemy_plane, flyWight):
        enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(bg_size, flyWight, enemy_plane, 12)
        plane_factory.EnemyPlane2Factory.createNumPlane(bg_size, flyWight, enemy_plane, 4)
        plane_factory.EnemyPlane3Factory.createNumPlane(bg_size, flyWight, enemy_plane, 2)
        enemy_plane.update(2)#设置速度为2


class Level_3(Level):
    @staticmethod
    def changeLevel(bg_size, enemy_plane, flyWight):
        enemy_plane.empty()
        plane_factory.EnemyPlane1Factory.createNumPlane(bg_size, flyWight, enemy_plane, 16)
        plane_factory.EnemyPlane2Factory.createNumPlane(bg_size, flyWight, enemy_plane, 8)
        plane_factory.EnemyPlane3Factory.createNumPlane(bg_size, flyWight, enemy_plane, 4)
        enemy_plane.update(2)#设置速度为2
        