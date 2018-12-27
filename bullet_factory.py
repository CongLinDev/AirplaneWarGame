import abc
import bullet
import flywight

class BulletFactory:
    __metaclass__= abc.ABCMeta #???
    @staticmethod
    def createBullet(position):
        pass
    @staticmethod
    def creatNumBullet(position, bullets):
        pass

class Bullet1Factory(BulletFactory):
    @staticmethod
    def createBullet(position):
        flyWight = flywight.Bullet_FlyWight()
        return bullet.Bullet1(position, flyWight)
    @staticmethod
    def creatNumBullet(position, bullets):
        flyWight = flywight.Bullet_FlyWight()
        for i in range(flyWight.BULLET_NUM):
            bullets.append(Bullet1Factory.createBullet(position))

class Bullet2Factory(BulletFactory):
    @staticmethod
    def createBullet(position):
        flyWight = flywight.Bullet_FlyWight()
        return bullet.Bullet2(position, flyWight)
    @staticmethod
    def creatNumBullet(position, bullets):
        flyWight = flywight.Bullet_FlyWight()
        for i in range(flyWight.BULLET_NUM):
            bullets.append(Bullet2Factory.createBullet(position))