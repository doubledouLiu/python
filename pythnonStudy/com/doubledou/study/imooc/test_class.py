class Programmer(object):
    hobby = 'Play Computer'

    def __init__(self, name, age, weight):
        self.name = name
        self._age = age
        self.__weight = weight

    @classmethod
    def get_hooby(cls):
        return cls.hobby

    @property
    def get_weight(self):
        return self.__weight

    def self_introduction(self):
        print 'My Nme is %s \n I am %s years old \n' % (self.name, self._age)


class BackendProgrammer(Programmer):
    def __init__(self, name, age, weight, language):
        super(BackendProgrammer, self).__init__(name, age, weight)
        self.language = language

    def self_introduction(self):
        print 'My name is %s \n My favorite language is %s' % (self.name, self.language)


def introduce(programmer):
    if isinstance(programmer, Programmer):
        programmer.self_introduction()


if __name__ == '__main__':
    programmer = Programmer('Albert', 25, 80)
    print dir(programmer)
    print Programmer.get_hooby()
    print programmer.get_weight
    programmer.self_introduction()

    backend_programmer = BackendProgrammer('Albert', 25, 80, 'Python')
    print dir(backend_programmer)
    print backend_programmer.__dict__
    print type(programmer)
    print isinstance(backend_programmer, Programmer)

    introduce(programmer)
    introduce(backend_programmer)

