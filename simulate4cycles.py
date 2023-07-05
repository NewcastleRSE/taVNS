import matplotlib.pyplot as plt
import breathingmodel.breathingmodel as b

t = 0
x = []
new_y = []
while t < 20:
	x.append(t)
	y = b.twocomplinear(t)
	new_y.append(y)
	t += 0.1
	print(y)

plt.plot(x, new_y)
plt.show()


#
#	new_y.append(y)
#
#print(new_y)
#x = [t + v * 20 / 100 for v in range(100)]
#y = [b.twocomplinear(v) for v in x]
#plt.plot(x, y)
##plt.show()
