import matplotlib.pyplot as plt

year = [1950, 1970, 1990, 2010]
pop = [2.135, 3.692, 5.263, 6.672]

value = [0, 0.6, 1.4, 1.6, 2.2, 2.5, 2.6, 3.2, 3.5, 3.9, 4.2, 6]
plt.hist(value, bins=10)

#plt.scatter(year, pop)
plt.show()
