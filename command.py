import abc

class Command:
    __metaclass__= abc.ABCMeta #抽象类
    @abc.abstractmethod
    def executeCommand(self):
        pass

class FireBulletCommand(Command):
    def __init__(self, aObject):
        Command.__init__(self)
        self.bulletGroup = aObject

    def executeCommand(self):
        return self.bulletGroup.fireBullet()
