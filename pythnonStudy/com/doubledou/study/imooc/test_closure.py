def func_150(val):
    passline = 90
    if val >= passline:
        print ('%d pass' % val)
    else:
        print ('failed')


def func_100(val):
    passline = 60
    if val >= passline:
        print ('%d pass' % val)
    else:
        print ('failed')


def set_passline(passline):
    def cmp(val):
        if val >= passline:
            print ('%d pass' % val)
        else :
            print ('failed')
    return cmp

if __name__ == '__main__':
    #func_100(60)
    #func_150(70)

    f_100 = set_passline(60)
    f_150 = set_passline(100)
    f_100(60)
    f_150(70)

