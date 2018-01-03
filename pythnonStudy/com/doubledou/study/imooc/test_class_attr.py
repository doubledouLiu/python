class Programmer(object):
    def __init__(self, name, age):
        self.name = name;
        if isinstance(age, int):
            self.age = age
        else:
            raise Exception('age must be int')

    def __str__(self):
        return '%s is %s years old' % (self.name, self.age)

    def __dir__(self):
        return self.__dict__.keys()

    def __getattribute__(self, name):
        #return getattr(self, name)
        #return self.__dict__[name]
        return super(Programmer, self).__getattribute__(name)

    def __setattr__(self, name, value):
        #setattr(self, name, value)
        self.__dict__[name] = value


if __name__ == '__main__':
    p1 = Programmer('Alert', 25)

    print p1
    print dir(p1)

    print p1.name
    p1.__setattr__('name', 'Bill')
    print p1.name

