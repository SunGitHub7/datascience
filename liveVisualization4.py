import matplotlib.pyplot as plt
import matplotlib.animation as anm
from matplotlib import style
import time
style.use("ggplot")  # to make grapgh little pretty we go for style

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):
    pullData = open("twitter-out.txt").read()
    lines = pullData.split('\n')

    xar = []
    yar = []

    x = 0  # line number, x- axis
    y = 0  # count +1 for positive and -0.5  for negative words

    for l in lines[-200:]:
        x += 1
        if "pos" in l:
            y += 1
        elif "neg" in l:
            y -= 0.1  # since negativity about anithing is high rate so we give 0.5  weight
        xar.append(x)
        yar.append(y)

    ax1.clear()
    ax1.plot(xar, yar)


while True:
        ani = anm.FuncAnimation(fig, animate, interval=10)
        plt.show()
