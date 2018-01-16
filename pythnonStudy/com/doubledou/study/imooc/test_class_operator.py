class Programmer(object):
    def __init__(self, name, age):
        self.name = name;
        if isinstance(age, int):
            self.age = age
        else:
            raise Exception('age must be int')

    def __eq__(self, other):
        if isinstance(other, Programmer):
            if self.age == other.age:
                return True
            else:
                return False
        else:
            raise Exception('The type of object must be Programmer')

    def __add__(self, other):
        if isinstance(other, Programmer):
            return self.age + other.age
        else:
            raise Exception('the type of object must be Programmer')

    def __str__(self):
        return '%s is %s years old' % (self.name, self.age)

    def __dir__(self):
        return self.__dict__.keys()


if __name__ == '__main__':
    p1 = Programmer('Alert', 25)
    p2 = Programmer('Bill', 30)
    print p1 == p2
    print p1 + p2

    print p1
    print p2
    print dir(p1)