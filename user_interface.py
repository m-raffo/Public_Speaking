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

badglob = "0.0"
bagblobooler = False

WINDOW_BG = "#ffffff"
TEXTBOX_BG = "#e9e9e9"

#DEFAULT_FONT = "OpenDyslexic"
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_SIZE = 22

# Colors for tips
COLOR_GOOD = "#15955f" # Green
COLOR_WARN = "#c9bb00" # Yellow
COLOR_BAD = "#ab0000" # Red



MINWPM = 0

MAXWPM = 300 #fast/minute



with open("./script.txt", "r") as text_file:
    speech = str.join('\n',text_file.readlines())

# * 6


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
    # The frame window for the program
    def bold_by_word_number(self, word_count):
        global badglob, bagblobooler
        '''line_count, word_count = self.get_index_by_word_number(speech, word_count)
        # print(line_count, word_count)
        line_count = line_count * 2 -1'''
        ts = speech
        ts = ts.split(' ')
        tl = speech
        tl = tl.split('\n')
        ts[word_count]
        j = 0
        k = 1
        for i in range(0,word_count):
            j+=len(ts[i])+1
            if '\n' in ts[i]:
                #
                k+=2
                j=2
                #print("NEWLINE")
        if not bagblobooler:
            bagblobooler = True
        else:
            self.text.tag_remove("0.0", badglob)
        badglob = str(k)+"."+str(j+10)
        #print (badglob)
        self.text.tag_add("BOLD", "0.0", str(k)+"."+str(j+10))
        #self.text.tag_remove("BOLD", str(k)+"."+str(j+5))


    def update(self, position, wpm, volume):
        # return None
        # print("Current wpm: {}".format(wpm))
        optimal_wpm = (MAXWPM + MINWPM)/2
        wpm = realtime_interpreter.get_wpm() #grab wpm value
        #process wpm value
        wpm -= optimal_wpm
        wpm *= 0.2
        if wpm > 0:
            wpm = abs(wpm ** 1.5)
        else:
            wpm = -abs(wpm ** 1.5)

        wpm += optimal_wpm
        wpm = clamp(MAXWPM - wpm, MINWPM, MAXWPM) #clamp it
        # print("Updating...")
        # print("Current wpm (clamped): {}".format(wpm))
        # print("Running average WPM: {}".format(float(sum(self.past_wpm[-6:-1]))/len(self.past_wpm[-6:-1])))
        self.past_wpm.append(wpm)
        # self.past_volume.append(volume)
        self.pace_value['text'] = ""#'{} WPM'.format(int(wpm))

        self.wpm_average_history.append(float(sum(self.past_wpm[-3:-1]))/len(self.past_wpm[-3:-1]))
        plot.save_plot(self.wpm_average_history[-10:-1], 'rect1.png', MAXWPM/  2.0, MINWPM, MAXWPM)
        # plot.save_plot(self.past_wpm, 'rect2.png', 5, 0, 10)

        # self.scrollb.set(.1, 0.8)

        wpm_settings = plot.get_wpm_settings_outside(MAXWPM / 2.0, MINWPM, MAXWPM)
        #print(wpm_settings)

        if wpm > wpm_settings [0]  and wpm / 2.0 <= wpm_settings [1]:
            self.speed_tip['text'] = "Speak faster"
            self.speed_tip.config(fg='#ff0000')



        elif wpm >= wpm_settings [1] and wpm / 2.0 <= wpm_settings [2]:
            self.speed_tip['text'] = "Speak a little slower"
            self.speed_tip.config(fg='#c9cf00')



        elif wpm >= wpm_settings [2] and wpm / 2.0 <= wpm_settings [3]:
            self.speed_tip['text'] = "Good speed"
            self.speed_tip.config(fg='#009800')



        elif wpm >= wpm_settings [3] and wpm / 2.0 <= wpm_settings [4]:
            self.speed_tip['text'] = "Speak a little faster"
            self.speed_tip.config(fg='#c9cf00')



        elif wpm >= wpm_settings [4] and wpm / 2.0 <= wpm_settings [5]:
            self.speed_tip['text'] = "Speak a lot faster"
            self.speed_tip.config(fg='#ff0000')

        else:
            self.speed_tip['text'] = "Please speak at a consistent pace"
            self.speed_tip.config(fg='black')
        # self.text.see(1)
        # print(self.scrollb.get())


        # os.system("python3 plot.py 0 150 300 {} rect2.png 140".format(str.join(',',past_wpm_str)))

#
        # print("Done computing...")

        img2 = ImageTk.PhotoImage(Image.open("rect1.png"))
        self.Artwork.configure(image=img2)
        self.Artwork.image = img2


        num_words = realtime_interpreter.get_word_number()

        # Update by word number
        #print("hi____"+str(num_words))
        # self.bold_by_word_number(num_words)
        # self.text.yview_moveto(0.5)


        # img2 = ImageTk.PhotoImage(Image.open("rect2.png"))
        # self.Artwork1.configure(image=img2)
        # self.Artwork1.image = img2

    def get_index_by_word_number(self,speech, word_count):
        current_found = 0
        count = 0
        speechtemp = speech;
        speechtemp.replace('\n',' ')
        for i in speechtemp:
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
        #self.text.tag_add("BOLD", '1.2', '1.5')
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


        # self.volumetip.pack(fill=tkinter.X, expand=False)
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
    #print("Running main now...")
    _thread.start_new_thread(realtime_interpreter.main, ())
app = Window(root)


def nonstop_update():
    print("initUI")
    i = 0
    while True:
        i+=1
        # print("Updating.........")
        app.update(0,realtime_interpreter.get_wpm(),randint(1,5))
        sleep(0.25)


# root.after(2000, task)
_thread.start_new_thread( task, () )
_thread.start_new_thread( nonstop_update, () )
root.mainloop()

print("Moving on..")
