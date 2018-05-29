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

# os.system("python3 plot.py 0 150 300 234,200,197,160,140 pace_graph.png 140")
# os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 volume_graph.png 120")

tag_ref = "0.0"
tag_ref_exists = False

WINDOW_BG = "#ffffff"
TEXTBOX_BG = "#e9e9e9"

#DEFAULT_FONT = "OpenDyslexic"
DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_SIZE = 22

# Colors for tips
COLOR_GOOD = "#15955f" # Green
COLOR_WARN = "#c9bb00" # Yellow
COLOR_BAD = "#ab0000" # Red

frame_count=0 #DELME
fps_on = False
enable_graphing= True

MINWPM = 0

MAXWPM = 300 #fast/minute


# Create and save new image to pace_graph.png to prevent errors if the file becomes corrupted

img = Image.new("RGB", (495, 150), '#ffffff')
img.save("pace_graph.png")

img = Image.new("RGB", (495, 150), '#ffffff')
img.save("volume_graph.png")

del img


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
    # Find tkinter index by word index in whole
    def get_index_by_word_number(self, word_count):
        line_no = 1 #this starts at one for some reason, gets booped later
        word_no = 0 #this is used to count
        char_no = 0 #this is used for the output thing

        for line in speech_by_paragraph:
            char_no = 0
            for word in line:
                word_no += 1
                char_no += len(word)+1
                if word_no >= word_count:
                    break
            if word_no >= word_count:
                break
            line_no += 2 #Lines per line

        return "{}.{}".format(line_no, char_no)



    # The frame window for the program
    def bold_by_word_number(self, word_count):
        global tag_ref, tag_ref_exists

        if not tag_ref_exists:
            tag_ref_exists = True
        else:
            self.text.tag_remove("0.0", tag_ref)

        tag_ref = self.get_index_by_word_number(word_count)
        self.text.tag_add("BOLD", "0.0", tag_ref)

    # The frame window for the program
    def highlight_by_word_number(self, word_count):
        tag_start = self.get_index_by_word_number(word_count)
        tag_end = self.get_index_by_word_number(word_count+1)
        self.text.tag_add("CORRECTION", tag_start, tag_end)


    def update(self, position, wpm, volume):
        if fps_on:
            global frame_count
            frame_count+=1

        optimal_wpm = (MAXWPM + MINWPM)/2
        wpm = realtime_interpreter.get_wpm() #grab wpm value

        wpm = clamp(MAXWPM - wpm, MINWPM, MAXWPM) #clamp it
        # print("Updating...")
        # print("Current wpm (clamped): {}".format(wpm))
        # print("Running average WPM: {}".format(float(sum(self.past_wpm[-6:-1]))/len(self.past_wpm[-6:-1])))

        if enable_graphing:
            self.past_wpm.append(wpm)
        # self.past_volume.append(volume)
        if fps_on:
            self.pace_value['text'] = frame_count#'{} WPM'.format(int(wpm))

        if enable_graphing:
            self.wpm_average_history.append(float(sum(self.past_wpm[-3:-1]))/len(self.past_wpm[-3:-1]))
            plot.save_plot(self.wpm_average_history[-10:-1], 'pace_graph.png', MAXWPM/  2.0, MINWPM, MAXWPM)

        # self.scrollb.set(.1, 0.8) #SET SCROLL

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
        # os.system("python3 plot.py 0 150 300 {} volume_graph.png 140".format(str.join(',',past_wpm_str)))
        # print("Done computing...")

        img2 = ImageTk.PhotoImage(Image.open("pace_graph.png"))
        self.Artwork.configure(image=img2)
        self.Artwork.image = img2


        num_words = realtime_interpreter.get_word_number()

        # Update by word number
        #print("hi____"+str(num_words))
        self.bold_by_word_number(num_words)
        variations = realtime_interpreter.get_variations()
        for variation in variations:
            self.highlight_by_word_number(variation.expected_index)
            #print (variation.expected_index)
        # self.text.yview_moveto(0.5)


        # img2 = ImageTk.PhotoImage(Image.open("volume_graph.png"))
        # self.Artwork1.configure(image=img2)
        # self.Artwork1.image = img2



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
        self.correction_font = Font(family=DEFAULT_FONT, size=DEFAULT_FONT_SIZE, weight="normal")






        self.text = Text(self.speechtext, wrap=WORD, bg= '#ffffff', font=(DEFAULT_FONT, DEFAULT_FONT_SIZE), fg = "#4f4f4f")

        self.scrollb = Scrollbar(self.speechtext, command=self.text.yview)
        self.scrollb.pack( fill=Y, side = RIGHT)
        self.text['yscrollcommand'] = self.scrollb.set


        self.text.config(state=DISABLED)



        self.text.pack(fill= BOTH)
        self.text.tag_configure("BOLD", font=self.bold_font, foreground='#000000')
        self.text.tag_configure("CORRECTION", font=self.correction_font, foreground='#FF0F0F')

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
        self.photo = ImageTk.PhotoImage(Image.open('pace_graph.png'))
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
        # self.photo1 = ImageTk.PhotoImage(Image.open('volume_graph.png'))
        # self.Artwork1 = Label(self.labelframe_volumechart, image=self.photo1)
        # self.Artwork1.photo = self.photo1
        # self.Artwork1.pack()
        #
        # self.labelframe_volumechart.pack(fill=tkinter.X, expand=False , padx = 0, pady = 0)



        self.past_wpm = [10, 10, 10, 10,10,10,10,10,10,10,10,10,10,10,10,10,10]
        self.wpm_average_history = [10, 10, 10, 10,10,10,10,10,10,10,10,10,10,10,10,10,10]

        self.past_volume = [150,150,150]
        self.volume_average_history = [150, 150, 150, 150]

        # self.update(0, 150, 150)




        # os.system("python3 plot.py 0 150 300 234,200,197,160,140 pace_graph.png 140")
        # os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 volume_graph.png 120")






root = Tk()

def start_threads():
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
        #app.update(0,1,1) debugbad
        sleep(0.05)


# root.after(2000, task)
start_threads()
#_thread.start_new_thread( task, () )
_thread.start_new_thread( nonstop_update, () )
root.mainloop()

print("Moving on..")
