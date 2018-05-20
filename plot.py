from random import randint
from scipy.interpolate import spline
import numpy as np
from PIL import Image, ImageDraw
import sys

SMOOTHING = 50

# Example call from terminal
# python3 plot.py 0 150 300 234,200,197,160,140


last_y = 0


def get_wpm_settings_outside(wpm_aim, lower, upper):
    total = upper
    segment_amount = total / 5.0

    settings = [lower]
    for i in range(1,6):
        settings.append(segment_amount * i)

    return settings


def save_plot(wpm, path, best_wpm, lower_limit, upper_limit):
    global last_y

    # img = Image.new('RGB', (495, 200), color = '#ffffff')
    img = Image.new('RGB', (495*3, 200*3), color = '#ffffff')
    draw = ImageDraw.Draw(img)

    def get_wpm_settings(wpm_aim, lower, upper):
        total = upper
        segment_amount = total / 5.0

        settings = [lower]
        for i in range(1,6):
            settings.append(segment_amount * i)

        return settings




    def scale(min, max, newmin, newmax,  value):
        global last_y
        if False:
            pass
            #print ('-'*5)
            #print ("Scaling: {}".format(value))
            #print ('In between {0} and {1}'.format(min, max))
            #print ('To between {0} and {1}'.format(newmin, newmax))
            #print ('Answer {}'.format(((float(value) - float(min)) / (float(max) - float(min))) * (float(newmax) - float(newmin)) + float(newmin)))
        return ((float(value) - float(min)) / (float(max) - float(min))) * (float(newmax) - float(newmin)) + float(newmin)

    def plot(x1, y1, x2, y2, minofgraphx, maxofgraphx, minofgraphy, maxofgraphy, color = "#000000"):
        global last_y
        # print(x1, y1, x2, y2)

        x1 = scale(minofgraphx, maxofgraphx, 0, img.width, x1)
        x2 = scale(minofgraphx, maxofgraphx, 0, img.width, x2)
        y1 = scale(minofgraphy, maxofgraphy, 0, img.height, y1)
        y2 = scale(minofgraphy, maxofgraphy, 0, img.height, y2)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=7)

        last_y = y2

        # print(x1, y1, x2, y2)
        # print('-'*4)





    wpm_settings = get_wpm_settings(best_wpm, lower_limit, upper_limit)

    # Get random wpm
    # wpm = [30]
    # for i in range(40):
    #     wpm.append(wpm[-1] + randint(-50,50))






    x = np.asarray(list(range(len(wpm))), dtype=np.float32)

    xnew = np.linspace(x.min(),x.max(),SMOOTHING)
    power = np.array([1.53E+03, 5.92E+02, 2.04E+02, 7.24E+01, 2.72E+01, 1.10E+01, 4.70E+00])

    power_smooth = spline(x,wpm,xnew)

    # print(power_smooth)
    #print ("SEttings: {}".format(wpm_settings))

    for x1, x2, y1,y2 in zip(xnew, xnew[1:], power_smooth, power_smooth[1:]):

        if (y1+y2) / 2.0 > wpm_settings [0]  and (y1+y2) / 2.0 <= wpm_settings [1]:
            plot(x1, y1, x2, y2, 0, max(xnew), upper_limit, lower_limit, '#ff0000')
            last_y = y2



        elif (y1+y2) / 2.0 >= wpm_settings [1] and (y1+y2) / 2.0 <= wpm_settings [2]:
            plot(x1, y1, x2, y2, 0, max(xnew), upper_limit, lower_limit, '#c9cf00')
            last_y = y2



        elif (y1+y2) / 2.0 >= wpm_settings [2] and (y1+y2) / 2.0 <= wpm_settings [3]:
            plot(x1, y1, x2, y2, 0,  max(xnew), upper_limit, lower_limit, '#009800')
            last_y = y2



        elif (y1+y2) / 2.0 >= wpm_settings [3] and (y1+y2) / 2.0 <= wpm_settings [4]:
            plot(x1, y1, x2, y2, 0, max(xnew), upper_limit, lower_limit, '#c9cf00')
            last_y = y2



        elif (y1+y2) / 2.0 >= wpm_settings [4] and (y1+y2) / 2.0 <= wpm_settings [5]:
            plot(x1, y1, x2, y2, 0, max(xnew), upper_limit, lower_limit, '#ff0000')
            last_y = y2

    total = img.height
    segment_amount = total / 5.0
    lower = 0

    settings = [lower]
    for i in range(1,6):
        settings.append(segment_amount * i)

    lineheight = wpm[-1]

    lineheight = float(lineheight) / float(upper_limit) * img.height

    draw.rectangle((0, 0, 20, settings[1]), fill='#ff0000')
    draw.rectangle((0, settings[1], 20, settings[2]), fill='#c9cf00')
    draw.rectangle((0, settings[2], 20, settings[3]), fill='#009800')
    draw.rectangle((0, settings[3], 20, settings[4]), fill='#c9cf00')
    draw.rectangle((0, settings[4], 20, settings[5]), fill='#ff0000')

    #print(last_y)

    #draw.line([(0,last_y),(img.width, last_y)], fill='#1a1a1a')
    # plot(0,xnew[-1], wpm[-1], wpm[-1], 0, max(xnew), 0, max(power_smooth), "#000000", )
    img = img.resize((495, 150), Image.ANTIALIAS)
    img.save(path)

    img.close()
