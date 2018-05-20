import matplotlib as mpl
from tkinter import *
import tkinter
from PIL import ImageTk, Image
from tkinter.font import Font
import os


os.system("python3 plot.py 0 150 300 234,200,197,160,140 rect1.png 140")
os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 rect2.png 120")


WINDOW_BG = "#ffffff"
TEXTBOX_BG = "#e9e9e9"

DEFAULT_FONT = "Helvetica"
DEFAULT_FONT_SIZE = 22

# Colors for tips
COLOR_GOOD = "#15955f" # Green
COLOR_WARN = "#c9bb00" # Yellow
COLOR_BAD = "#ab0000" # Red



# Image
imagepath = 'sample chart.png'


class Window(Frame):
    def update(self, position, wpm, volume):
        print("Updating...")
        self.past_wpm.append(wpm)
        self.past_volume.append(volume)

        img2 = ImageTk.PhotoImage(Image.open("rect1.png"))
        self.Artwork.configure(image=img2)
        self.Artwork.image = img2

        img2 = ImageTk.PhotoImage(Image.open("rect2.png"))
        self.Artwork1.configure(image=img2)
        self.Artwork1.image = img2

    def __init__(self, master=None):
        self.root = master
        self.root.title("App")
        self.root.geometry("1000x500")
        self.root.config(bg = '#ffffff')
        self.root.update()


        self.speechtext = Frame(self.root)


        self.labelframe = LabelFrame(self.root, text="", width=700, height= 1, bg= TEXTBOX_BG)
        self.labelframe.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=False)

        self.dostuff = Button(self.labelframe, text="update!", command=lambda: self.update(0,140,40))
        self.dostuff.pack()

        # Bold font
        self.bold_font = Font(family=DEFAULT_FONT, size=DEFAULT_FONT_SIZE, weight="bold")




        text = Text(self.speechtext, wrap=WORD, bg= '#ffffff', font=(DEFAULT_FONT, DEFAULT_FONT_SIZE), fg = "#4f4f4f")


        text.pack(fill= BOTH)
        text.tag_configure("BOLD", font=self.bold_font, foreground='#000000')
        text.insert(END, '''HI WORLD''')
        text.tag_add("BOLD", '1.2', '1.5')

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

        self.labelframe_volumechart_numbers = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)
        self.labelframe_volumechart_numbers.pack(fill=tkinter.X, expand=False , padx = 0)




        self.volume_value_label = Label(self.labelframe_volumechart_numbers, text= "Volume:", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)
        self.volume_value = Label(self.labelframe_volumechart_numbers, text= "1.5x ambient", fg="black", font=(DEFAULT_FONT, DEFAULT_FONT_SIZE),  bg = TEXTBOX_BG)




        self.volume_value.pack(fill=tkinter.X, expand=True, side = RIGHT)
        self.volume_value_label.pack(fill=tkinter.X, expand=True, side = LEFT)

        self.labelframe_volumechart = Frame(self.labelframe, width=1, height= 1, bg = TEXTBOX_BG)


        self.photo1 = ImageTk.PhotoImage(Image.open('rect2.png'))
        self.Artwork1 = Label(self.labelframe_volumechart, image=self.photo1)
        self.Artwork1.photo = self.photo1
        self.Artwork1.pack()

        self.labelframe_volumechart.pack(fill=tkinter.X, expand=False , padx = 0, pady = 0)



        self.past_wpm = []
        self.past_volume = []

        self.update(0, 150, 150)




        os.system("python3 plot.py 0 150 300 234,200,197,160,140 rect1.png 140")
        os.system("python3 plot.py 0 150 300 20,40,100,250,100,140,120 rect2.png 120")







root = Tk()



app = Window(root)
root.mainloop()
