
from random import randint
from scipy.interpolate import spline
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig


def get_wpm_settings(wpm_aim, lower, upper):
    total = upper
    segment_amount = total / 5.0

    settings = [lower]
    for i in range(1,6):
        settings.append(segment_amount * i)

    print(settings)
    return settings



best_wpm = 100
lower_limit = 0
upper_limit = 200




wpm_settings = get_wpm_settings(best_wpm, lower_limit, upper_limit)

wpm = [30]

for i in range(40):
    wpm.append(wpm[-1] + randint(-50,50))

x = np.asarray(list(range(len(wpm))), dtype=np.float32)

xnew = np.linspace(x.min(),x.max(),300)
power = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])

power_smooth = spline(x,wpm,xnew)




for x1, x2, y1,y2 in zip(xnew, xnew[1:], power_smooth, power_smooth[1:]):
    if (y1+y2) / 2.0 > wpm_settings [0]  and (y1+y2) / 2.0 <= wpm_settings [1]:
        plt.plot([x1, x2], [y1, y2], 'r', linewidth = 2)

    elif (y1+y2) / 2.0 >= wpm_settings [1] and (y1+y2) / 2.0 <= wpm_settings [2]:
        plt.plot([x1, x2], [y1, y2], 'y', linewidth = 2)

    elif (y1+y2) / 2.0 >= wpm_settings [2] and (y1+y2) / 2.0 <= wpm_settings [3]:
        plt.plot([x1, x2], [y1, y2], 'g', linewidth = 2)

    elif (y1+y2) / 2.0 >= wpm_settings [3] and (y1+y2) / 2.0 <= wpm_settings [4]:
        plt.plot([x1, x2], [y1, y2], 'y', linewidth = 2)

    elif (y1+y2) / 2.0 >= wpm_settings [4] and (y1+y2) / 2.0 <= wpm_settings [5]:
        plt.plot([x1, x2], [y1, y2], 'r', linewidth = 2)

plt.ylim((lower_limit, upper_limit))
# plt.plot(wpm)


plt.ylabel('some numbers')
savefig('rect1.png')
plt.show()
