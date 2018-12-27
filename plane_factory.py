import abc
import plane
import pygame
import flywight

class PlaneFactory:
    __metaclass__= abc.ABCMeta #抽象类
    @staticmethod
    def createPlane(bg_size):
        pass
    #创建num个飞机，加入group中
    #python不支持重载机制
    @staticmethod
    def createNumPlane(bg_size, group, num):
        pass

class ClientPlaneFactory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size):
        flyWight = flywight.ClientPlane_FlyWight()
        return plane.ClientPlane(bg_size, flyWight)

    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, group, num):
        flyWight = flywight.ClientPlane_FlyWight()
        for i in range(num):
            planes = plane.ClientPlane(bg_size, flyWight)
            group.add(planes)

class EnemyPlane1Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size):
        flyWight = flywight.EnemyPlane1_FlyWight()
        return plane.EnemyPlane1(bg_size, flyWight)
    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, group, num):
        flyWight = flywight.EnemyPlane1_FlyWight()
        for i in range(num):
            planes = plane.EnemyPlane1(bg_size, flyWight)
            group.add(planes)

class EnemyPlane2Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size):
        flyWight = flywight.EnemyPlane2_FlyWight()
        return plane.EnemyPlane2(bg_size, flyWight)
    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, group, num):
        flyWight = flywight.EnemyPlane2_FlyWight()
        for i in range(num):
            planes = plane.EnemyPlane2(bg_size, flyWight)
            group.add(planes)

class EnemyPlane3Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size):
        flyWight = flywight.EnemyPlane3_FlyWight()
        return plane.EnemyPlane3(bg_size, flyWight)

    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, group, num):
        flyWight = flywight.EnemyPlane3_FlyWight()
        for i in range(num):
            planes = plane.EnemyPlane3(bg_size, flyWight)
            group.add(planes)