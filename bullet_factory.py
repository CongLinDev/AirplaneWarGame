import abc
import bullet

class BulletFactory:
    __metaclass__= abc.ABCMeta #抽象类

    #@abc.abstractmethod
    @staticmethod
    def createBullet(position, flyWight):
        pass

    #@abc.abstractmethod
    @staticmethod
    def creatNumBullet(position, flyWight, bullets):
        pass

class Bullet1Factory(BulletFactory):
    @staticmethod
    def createBullet(position, flyWight):
        return bullet.Bullet1(position, flyWight)
    @staticmethod
    def creatNumBullet(position, flyWight, bullets):
        for i in range(flyWight.BULLET_NUM):
            bullets.append(Bullet1Factory.createBullet(position, flyWight))

class Bullet2Factory(BulletFactory):
    @staticmethod
    def createBullet(position, flyWight):
        return bullet.Bullet2(position, flyWight)
    @staticmethod
    def creatNumBullet(position, flyWight, bullets):
        for i in range(flyWight.BULLET_NUM):
            bullets.append(Bullet2Factory.createBullet(position, flyWight))