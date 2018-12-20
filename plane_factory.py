import abc
import plane
import pygame
import flywight

class PlaneFactory:
    __metaclass__= abc.ABCMeta #抽象类

    #@abc.abstractmethod
    @staticmethod
    def createPlane(bg_size, flyWight):
        pass

    #创建num个飞机，加入group中
    #python不支持重载机制
    #@abc.abstractmethod
    @staticmethod
    def createNumPlane(bg_size, flyWight, group, num):
        pass

class ClientPlaneFactory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size, flyWight):
        return plane.ClientPlane(bg_size, flyWight)

    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, flyWight, group, num):
        for i in range(num):
            planes = plane.ClientPlane(bg_size, flyWight)
            group.add(planes)

class EnemyPlane1Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size, flyWight):
        return plane.EnemyPlane1(bg_size, flyWight)
    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, flyWight, group, num):
        for i in range(num):
            planes = plane.EnemyPlane1(bg_size, flyWight)
            group.add(planes)

class EnemyPlane2Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size, flyWight):
        return plane.EnemyPlane2(bg_size, flyWight)
    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, flyWight, group, num):
        for i in range(num):
            planes = plane.EnemyPlane2(bg_size, flyWight)
            group.add(planes)

class EnemyPlane3Factory(PlaneFactory):
    @staticmethod
    def createPlane(bg_size, flyWight):
        return plane.EnemyPlane3(bg_size, flyWight)

    #创建num个飞机，加入group中
    @staticmethod
    def createNumPlane(bg_size, flyWight, group, num):
        for i in range(num):
            planes = plane.EnemyPlane3(bg_size, flyWight)
            group.add(planes)