from tkinter import *
import tkinter
from PIL import ImageTk, Image


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
# icon = ImageTk.PhotoImage(Image.open(imagepath))


class Window(Frame):


    def __init__(self, master=None):
        # Frame.__init__(self, master)
        # self.master = master
        # self.init_window()
        #
        # self.config(bg=WINDOW_BG)
        #
        # self.root.update()
        # self.box1Text = tkinter.Text(self.root, width=1, height=1)
        # self.box1Text.pack(fill=tkinter.BOTH,side=tkinter.LEFT, expand=True)
        # self.box2Text = tkinter.Text(self.root, width=1, height=1)
        # self.box2Text.pack(fill=tkinter.BOTH,side=tkinter.RIGHT, expand=True)

        self.root = master
        self.root.title("App")
        self.root.geometry("1000x500")
        self.root.config(bg = '#ffffff')
        self.root.update()
        self.labelframe = LabelFrame(self.root, text="", width=700, height= 1, bg= TEXTBOX_BG)
        # self.box2Text = tkinter.Text(self.root, width=1, height=1)
        # self.labelframe.pack(fill=tkinter.BOTH,side=tkinter.RIGHT, expand=True)
        self.labelframe.pack(fill=tkinter.Y, side=tkinter.RIGHT, expand=False)


        self.text = tkinter.Text(self.root, wrap=WORD, bg= '#ffffff', font=(DEFAULT_FONT, DEFAULT_FONT_SIZE), fg = "#777777")
        # self.text.pack(fill=BOTH, side=tkinter.LEFT)
        self.text.pack(fill=BOTH)
        # self.text.pack(fill=tkinter.BOTH,side=tkinter.LEFT, expand=True)
        # self.labelframe = LabelFrame(self.root, text="", width=1, height= 1, bg= TEXTBOX_BG)




        self.text.insert(END, '''Lorem ipsum de arbitrantur. Enim id ad quem offendit, ea quid quid quis excepteur eu cupidatat fugiat arbitror, qui nostrud distinguantur, nescius si labore ad id export dolore est nescius, hic ita quae doctrina est possumus id nostrud. Te appellat qui mentitum, eu velit constias.Quis consequat ab summis anim e veniam e excepteur. Anim ut nostrud ea summis, duis laborum eu vidisse. Admodum graviterque te ingeniis.
        #
        # Consequat eram quid se quae, aut se tamen elit quem. Illum excepteur aut aliqua dolore, quorum doctrina nam coniunctione ad a malis cernantur, a quorum vidisseconiunctione a fugiat ut probant ex sunt ad se magna hic ipsum, nulla admodum anvoluptate ad amet quo incurreret. Do aute a dolor ne tempor quamquam nonsempiternum ubi ullamco efflorescere id commodo, ea quid irure et consequat, iisdo malis eram enim, cillum nescius voluptate, qui quem arbitror mandaremus nam osunt sint hic incurreret. Summis eiusmod coniunctione.Iis sunt offendit hic nenoster multos summis laborum do vidisse duis elit si quis in oe instituendarum.Quorum cohaerescant quibusdam nisi deserunt, anim admodum occaecat. Illumofficia ita amet cillum, ut quis praesentibus, iudicem summis ita proidentrelinqueret ea constias exercitation ut mentitum, ne fore officia quo voluptatene commodo est tamen iudicem qui distinguantur se te magna deserunt praetermissum.''')

        self.text.config(state=DISABLED)


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


        self.photo = ImageTk.PhotoImage(Image.open('sample chart.png'))
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


        self.photo1 = ImageTk.PhotoImage(Image.open('sample chart.png'))
        self.Artwork1 = Label(self.labelframe_volumechart, image=self.photo1)
        self.Artwork1.photo = self.photo1
        self.Artwork1.pack()

        self.labelframe_volumechart.pack(fill=tkinter.X, expand=False , padx = 0, pady = 0)


        # self.bind("<Configure>", self.on_resize)

    def on_resize(self,event):
        print(event.width())






    # #Creation of init_window
    # def init_window(self):
    #
    #
    #
    #     # changing the title of our master widget
    #     self.master.title("GUI")
    #
    #     # allowing the widget to take the full space of the root window
    #     self.pack(fill=BOTH, expand=1)
    #
    #     # creating a button instance
    #
    #     # text = Text(self, wrap=WORD, bg= TEXTBOX_BG, width=1, height= 1)
    #     # text = Text(self, wrap=WORD, bg= TEXTBOX_BG)
    #     #
    #     # # text = tkinter.Text(self.root, width=1, height=1)
    #     # text.pack(fill=BOTH,side=tkinter.RIGHT, expand=1)
    #     # # self.box2Text = tkinter.Text(self.root, width=1, height=1)
    #     # # self.box2Text.pack(fill=tkinter.BOTH,side=tkinter.RIGHT, expand=True)
    #     #
    #     # text.place(x=0, y=0)
    #     #
    #     # text.insert(END, '''Lorem ipsum de arbitrantur. Enim id ad quem offendit, ea quid quid quis excepteur eu cupidatat fugiat arbitror, qui nostrud distinguantur, nescius si labore ad id export dolore est nescius, hic ita quae doctrina est possumus id nostrud. Te appellat qui mentitum, eu velit constias.Quis consequat ab summis anim e veniam e excepteur. Anim ut nostrud ea summis, duis laborum eu vidisse. Admodum graviterque te ingeniis.
    #     #
    #     # Consequat eram quid se quae, aut se tamen elit quem. Illum excepteur aut aliqua dolore, quorum doctrina nam coniunctione ad a malis cernantur, a quorum vidisseconiunctione a fugiat ut probant ex sunt ad se magna hic ipsum, nulla admodum anvoluptate ad amet quo incurreret. Do aute a dolor ne tempor quamquam nonsempiternum ubi ullamco efflorescere id commodo, ea quid irure et consequat, iisdo malis eram enim, cillum nescius voluptate, qui quem arbitror mandaremus nam osunt sint hic incurreret. Summis eiusmod coniunctione.Iis sunt offendit hic nenoster multos summis laborum do vidisse duis elit si quis in oe instituendarum.Quorum cohaerescant quibusdam nisi deserunt, anim admodum occaecat. Illumofficia ita amet cillum, ut quis praesentibus, iudicem summis ita proidentrelinqueret ea constias exercitation ut mentitum, ne fore officia quo voluptatene commodo est tamen iudicem qui distinguantur se te magna deserunt praetermissum.''')
    #     #
    #     #
    #     #
    #     # # text.delete(0, END)
    #     # # text.insert(0, "a default value")
    #     #
    #     # text.config(state=DISABLED)
    #
    #     # placing the button on my window
    #
    # def client_exit(self):
    #     exit()

root = Tk()
# root = Toplevel()

#
# #size of the window
#
# width = root.winfo_screenwidth()
# height = root.winfo_screenheight()
# root.geometry('8000x600')


app = Window(root)
root.mainloop()
