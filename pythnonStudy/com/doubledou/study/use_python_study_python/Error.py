import random

num = random.randint(0, 100)
print num

while True:
    try:
        guess = int(raw_input("Enter 1-100"))
    except ValueError, e:
        print "Please enter 1 to 100"
    if guess > num:
        print "guess Bigger: ", guess
    elif guess < num:
        print "guess Smaller: ", guess
    else:
        print "guess OK, game over ", guess
        break
    print "\n"
