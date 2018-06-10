from functions import *
import matplotlib.pyplot as plt
import numpy as np


def f1(x1, x2):
    return 0.2*(x1-70)**2 + 0.8*(x2-20)**2


def f2(x1, x2):
    return 0.8*(x1-10)**2 + 0.2*(x2-70)**2


def original(fx, fy):

    x1, x2 = symbols("x1 x2")

    values = solve([0.2*(x1-70)**2 + 0.8*(x2-20)**2 - fx,
                    0.8*(x1-10)**2 + 0.2*(x2-70)**2 - fy], dict=True)

    return [values[0][x1], values[0][x2]]


# Настройки отображения
plt.gcf().canvas.set_window_title("Домашняя работа #4")
plt.xlabel("X1")
plt.ylabel("X2")

plt.axvline(0, 0, 1)
plt.axhline(0, 0, 1)

Q = []
Q80 = []
for w in range(1, 1024):
    a = lptau(w, 2)
    # Q.append(a)
    print(str(w) + " - " + str(a))
    ax = a[0]*80
    ay = a[1]*80
    Q80.append([ax, ay])
    # plt.scatter(a[0], a[1], color="black")

    tmp = a[0]
    a[0] = f1(a[0]*80, a[1]*80)
    a[1] = f2(tmp*80, a[1]*80)
    # plt.scatter(a[0], a[1], color="black")
    Q.append(a)

# for i in range(0, len(Q)):
#     plt.text(Q[i][0], Q[i][1], str(str(Q80[i][0]) + ", " + str(Q80[i][1])))

Q = pareto(Q)
print(Q)
print(len(Q))

for v in range(0, len(Q)):
    plt.scatter(Q[v][0], Q[v][1], color='blue')
    # orig = original(Q[v][0], Q[v][1])
    # plt.text(Q[v][0], Q[v][1], str(round(orig[0], 3)) + ", " + str(round(orig[1], 3)))
    # print("done " + str(v))

optimal = [f1(22.0, 30.0), f2(22.0, 30.0)]
plt.scatter(optimal[0], optimal[1], color="red")
plt.text(optimal[0], optimal[1], str(22.0) + ", " + str(30.0))

x = np.arange(0, 1500, 1)
plt.plot(x, x*1/1)

p = 0
tx = 0
ty = 0
found_flag = False
while True:
    print(p)
    for i in range(0, len(Q)):
        if (Q[i][1] + 1*Q[i][0]*1/1 - p) < 0.5:
            found_flag = True
            tx = Q[i][0]
            ty = Q[i][1]
            break
    if found_flag:
        break
    p += 1

plt.plot(x, -x*1/1+p)
plt.scatter(tx, ty, color="orange")

plt.show()
