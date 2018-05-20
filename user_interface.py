from tkinter import *
import tkinter
from PIL import ImageTk, Image
from tkinter.font import Font
import os
from random import randint
import plot
import _thread
from time import sleep

from backend import realtime_interpreter

# os.system("python3 plot.py 0 150 300 234,200,197,160,140 rect1.png 140")
# os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 rect2.png 120")


WINDOW_BG = "#ffffff"
TEXTBOX_BG = "#e9e9e9"

DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_SIZE = 22

# Colors for tips
COLOR_GOOD = "#15955f" # Green
COLOR_WARN = "#c9bb00" # Yellow
COLOR_BAD = "#ab0000" # Red



MINWPM = 0

MAXWPM = 200



speech = '''In ullamco praesentibus.

Quorum voluptate appellat hic de tamen quamquam laboris, litteris labore illum  aut tamen o a enim mandaremus singulis. Quo eiusmod non cupidatat, an aliqua  domesticarum o probant te vidisse si nescius cillum fugiat laborum ipsum et eu iis firmissimum, quid consequat an distinguantur, quis te e legam aliquip et pariatur in offendit. Sint est si veniam quamquam.

Do illum proident concursionibus ad fore fabulas iis appellat. Est dolore appellat distinguantur, se ne arbitrantur, fabulas irure ullamco arbitror, mandaremus ne arbitror non nostrud si quorum, est dolore deserunt expetendis, veniam ad consequat si summis et export senserit si litteris.

Veniam sed probant iis noster in fabulas duis magna nostrud anim non singulis elit malis est multos aut id malis cernantur tractavissent, dolore comprehenderit laborum elit offendit, qui sint nescius proident, quamquam quo dolore admodum, officia illum te probant fidelissimae.

''' * 6


speech_by_paragraph_raw = speech.split('\n')
speech_by_paragraph = []
for i in speech_by_paragraph_raw:
    if i != '\n' and i != '':
        speech_by_paragraph.append(i.split(' '))







def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)



# Image
imagepath = 'sample chart.png'


class Window(Frame):
    def bold_by_word_number(self, word_count):
        line_count, word_count = self.get_index_by_word_number(speech, word_count)
        # print(line_count, word_count)
        line_count = line_count * 2 -1
        self.text.tag_add("BOLD", '{0}.{1}'.format(line_count, word_count), '{0}.{1}'.format(line_count, word_count+3))


    def update(self, position, wpm, volume):
        # return None
        # print("Current wpm: {}".format(wpm))
        wpm = clamp(MAXWPM - realtime_interpreter.get_wpm(), MINWPM, MAXWPM)
        # print("Updating...")
        # print("Current wpm (clamped): {}".format(wpm))
        # print("Running average WPM: {}".format(float(sum(self.past_wpm[-6:-1]))/len(self.past_wpm[-6:-1])))
        self.past_wpm.append(wpm)
        # self.past_volume.append(volume)
        self.pace_value['text'] = '{} WPM'.format(int(wpm))

        self.wpm_average_history.append(float(sum(self.past_wpm[-3:-1]))/len(self.past_wpm[-3:-1]))
        plot.save_plot(self.wpm_average_history[-10:-1], 'rect1.png', MAXWPM/  2.0, MINWPM, MAXWPM)
        # plot.save_plot(self.past_wpm, 'rect2.png', 5, 0, 10)

        # self.scrollb.set(.1, 0.8)



        # self.text.see(1)
        # print(self.scrollb.get())


        # os.system("python3 plot.py 0 150 300 {} rect2.png 140".format(str.join(',',past_wpm_str)))

#
        # print("Done computing...")

        img2 = ImageTk.PhotoImage(Image.open("rect1.png"))
        self.Artwork.configure(image=img2)
        self.Artwork.image = img2




        # Update by word number
        self.bold_by_word_number(realtime_interpreter.get_word_number())
        # self.text.yview_moveto(0.5)


        # img2 = ImageTk.PhotoImage(Image.open("rect2.png"))
        # self.Artwork1.configure(image=img2)
        # self.Artwork1.image = img2

    def get_index_by_word_number(self,speech, word_count):
        current_found = 0
        count = 0
        for i in speech_by_paragraph:
            count += 1
            if len(i) + current_found  > word_count:
                return count, word_count - current_found
            else:
                current_found += len(i)





    def __init__(self, master=None):
        self.root = master
        self.root.title("App")
        self.root.geometry("1000x500")
        self.root.config(bg = '#ffffff')
        self.root.update()


        self.speechtext = Frame(self.root)


        self.labelframe = LabelFrame(self.root, text="", width=700, height= 1, bg= TEXTBOX_BG)
        self.labelframe.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=False)

        # self.dostuff = Button(self.labelframe, text="update!", command=lambda: self.update(0,realtime_interpreter.get_wpm(),randint(1,5)))
        # self.dostuff.pack()

        # Bold font
        self.bold_font = Font(family=DEFAULT_FONT, size=DEFAULT_FONT_SIZE, weight="bold")





        self.text = Text(self.speechtext, wrap=WORD, bg= '#ffffff', font=(DEFAULT_FONT, DEFAULT_FONT_SIZE), fg = "#4f4f4f")

        self.scrollb = Scrollbar(self.speechtext, command=self.text.yview)
        self.scrollb.pack( fill=Y, side = RIGHT)
        self.text['yscrollcommand'] = self.scrollb.set


        self.text.config(state=DISABLED)



        self.text.pack(fill= BOTH)
        self.text.tag_configure("BOLD", font=self.bold_font, foreground='#000000')
        self.text.configure(state='normal')
        self.text.insert(END, speech)
        self.text.config(state=DISABLED)
        self.text.tag_add("BOLD", '1.2', '1.5')
        # self.text.tag_add("BOLD", '2.3', '2.8')

        self.speechtext.pack(fill=BOTH)





        # self.text.insert(END, '''Text here''')

        # self.text.config(state=DISABLED)


        self.tips = Label(self.labelframe, text="Tips:", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE-2), bg=TEXTBOX_BG)

        self.tips.pack(anchor="w")

        # Tips in a textbox

        # self.tipstext = tkinter.Text(self.labelframe, width=1, height = 2, wrap=WORD, bg= TEXTBOX_BG)
        # self.tipstext.pack(fill=tkinter.X, expand=False)
        #
        # self.tipstext.insert(END, "Slow down\nGood Volume")

        # ------------------------------------------------------

        # Tips as a label

        self.labelframe_tips = Frame(self.labelframe, width=1, height= 1, bg = WINDOW_BG)
        self.labelframe_tips.pack(fill=tkinter.X, expand=False , padx = 10)

        self.volume_tip = Label(self.labelframe_tips, text= "Good Volume", fg=COLOR_GOOD, font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = WINDOW_BG)


        self.speed_tip = Label(self.labelframe_tips, text= "Slow down a bit", fg=COLOR_WARN, font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = WINDOW_BG)


        self.volume_tip.pack(fill=tkinter.X, expand=False)
        self.speed_tip.pack(fill=tkinter.X, expand=False)

        self.spaceholder1 = Frame(self.labelframe, bg = TEXTBOX_BG)
        self.spaceholder1.pack(fill = X, pady= 50/2)


        # Frame for the pace chart!
        self.labelframe_pacechart_numbers = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)
        self.labelframe_pacechart_numbers.pack(fill=tkinter.X, expand=False , padx = 0)




        self.pace_value_label = Label(self.labelframe_pacechart_numbers, text= "Pace:", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)
        self.pace_value = Label(self.labelframe_pacechart_numbers, text= "25 wpm", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)




        self.pace_value.pack(fill=tkinter.X, expand=True, side = RIGHT)
        self.pace_value_label.pack(fill=tkinter.X, expand=True, side = LEFT)

        self.labelframe_pacechart = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)


        # self.photo = ImageTk.PhotoImage(Image.open('sample chart.png'))
        self.photo = ImageTk.PhotoImage(Image.open('rect1.png'))
        self.Artwork = Label(self.labelframe_pacechart, image=self.photo)
        self.Artwork.photo = self.photo
        self.Artwork.pack()

        self.labelframe_pacechart.pack(fill=tkinter.X, expand=False , padx = 0, pady = 0)


        self.spaceholder2 = Frame(self.labelframe, bg = TEXTBOX_BG)
        self.spaceholder2.pack(fill = X, pady= 50/2)

        # self.labelframe_volumechart_numbers = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)
        # self.labelframe_volumechart_numbers.pack(fill=tkinter.X, expand=False , padx = 0)




        # self.volume_value_label = Label(self.labelframe_volumechart_numbers, text= "Volume:", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)
        # self.volume_value = Label(self.labelframe_volumechart_numbers, text= "1.5x ambient", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)




        # self.volume_value.pack(fill=tkinter.X, expand=True, side = RIGHT)
        # self.volume_value_label.pack(fill=tkinter.X, expand=True, side = LEFT)
        #
        # self.labelframe_volumechart = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)
        #
        #
        # self.photo1 = ImageTk.PhotoImage(Image.open('rect2.png'))
        # self.Artwork1 = Label(self.labelframe_volumechart, image=self.photo1)
        # self.Artwork1.photo = self.photo1
        # self.Artwork1.pack()
        #
        # self.labelframe_volumechart.pack(fill=tkinter.X, expand=False , padx = 0, pady = 0)



        self.past_wpm = [10, 10, 10, 10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        self.wpm_average_history = [10, 10, 10, 10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        self.past_volume = [150,150,150]

        # self.update(0, 150, 150)




        # os.system("python3 plot.py 0 150 300 234,200,197,160,140 rect1.png 140")
        # os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 rect2.png 120")






root = Tk()

def task():
    # Run the backend code
    print("Running main now...")
    _thread.start_new_thread(realtime_interpreter.main, ())
app = Window(root)


def nonstop_update():
    print("RNNNINGININGINGIN")
    while True:
        # print("Updating.........")
        app.update(0,realtime_interpreter.get_wpm(),randint(1,5))
        sleep(0.2)


# root.after(2000, task)
_thread.start_new_thread( task, () )
_thread.start_new_thread( nonstop_update, () )
root.mainloop()

print("Moving on..")
