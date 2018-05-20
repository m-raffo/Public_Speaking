from random import randint
from scipy.interpolate import spline
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from PIL import Image, ImageDraw
import sys

def save_plot(wpm_list, path):
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
    savefig(path)


def post_process_img(path):
    img = Image.open(path)

    img = img.crop((81, 59, 81+ 495, 59+ 368))

    draw = ImageDraw.Draw(img)


    total = img.height
    segment_amount = total / 5.0
    lower = 0

    settings = [lower]
    for i in range(1,6):
        settings.append(segment_amount * i)

    draw.rectangle((0, 0, 20, settings[1]), fill='#fc2222')
    draw.rectangle((0, settings[1], 20, settings[2]), fill='#defc22')
    draw.rectangle((0, settings[2], 20, settings[3]), fill='#26fc22')
    draw.rectangle((0, settings[3], 20, settings[4]), fill='#defc22')
    draw.rectangle((0, settings[4], 20, settings[5]), fill='#fc2222')

    img = img.resize((img.width, 200))


    img.save(path)


if __name__ == "__main__":
    save_plot([], "rect1.png")
    post_process_img("rect1.png")
