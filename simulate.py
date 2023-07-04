import matplotlib.pyplot as plt
import breathingmodel.breathingmodel as b

x = []
for i in range(100):
    x.append(float(i) * 5.0 / 100.0)

y = list(map(b.twocomplinear, x))
plt.plot(x, y)
plt.show()
