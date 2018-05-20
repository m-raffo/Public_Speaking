from random import randint
from scipy.interpolate import spline
import matplotlib.patches as patches
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from PIL import Image, ImageDraw
import sys


# Example call from terminal
# python3 plot.py 0 150 300 234,200,197,160,140






def save_plot(wpm_list, path):
    def get_wpm_settings(wpm_aim, lower, upper):
        total = upper
        segment_amount = total / 5.0

        settings = [lower]
        for i in range(1,6):
            settings.append(segment_amount * i)

        return settings

    best_wpm = int(sys.argv[2])
    lower_limit = int(sys.argv[1])
    upper_limit = int(sys.argv[3])

    wpm_settings = get_wpm_settings(best_wpm, lower_limit, upper_limit)

    # Get random wpm
    # wpm = [30]
    # for i in range(40):
    #     wpm.append(wpm[-1] + randint(-50,50))

    wpm = []
    wpm_raw = sys.argv[4].split(',')
    for i in wpm_raw:
        wpm.append(int(i))




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

    plt.plot([0,xnew[-1]], [wpm[-1], wpm[-1]], "#000000", linewidth = 2)
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

    lineheight = int(sys.argv[6])

    lineheight = float(lineheight) / float(sys.argv[3]) * img.height

    draw.rectangle((0, 0, 20, settings[1]), fill='#ff0000')
    draw.rectangle((0, settings[1], 20, settings[2]), fill='#c9cf00')
    draw.rectangle((0, settings[2], 20, settings[3]), fill='#009800')
    draw.rectangle((0, settings[3], 20, settings[4]), fill='#c9cf00')
    draw.rectangle((0, settings[4], 20, settings[5]), fill='#ff0000')
    # draw.line([0,lineheight, img.width, lineheight], fill='#000000', width=3)


    img = img.resize((img.width, 200))


    img.save(path)


if __name__ == "__main__":
    save_plot([], sys.argv[5])
    post_process_img(sys.argv[5])
