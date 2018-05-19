from tkinter import *
import tkinter


WINDOW_BG = "#ffffff"
TEXTBOX_BG = "#e9e9e9"

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

        self.root = tkinter.Tk()
        self.root.title("App")
        self.root.geometry("400x400")
        self.root.update()
        self.text = tkinter.Text(self.root, width=1, height=1, wrap=WORD, bg= TEXTBOX_BG)
        self.text.pack(fill=tkinter.BOTH,side=tkinter.LEFT, expand=True)
        self.labelframe = LabelFrame(self.root, text="Info", width=1, height= 1)
        # self.box2Text = tkinter.Text(self.root, width=1, height=1)
        self.labelframe.pack(fill=tkinter.BOTH,side=tkinter.RIGHT, expand=True)

        self.text.insert(END, '''Lorem ipsum de arbitrantur. Enim id ad quem offendit, ea quid quid quis excepteur eu cupidatat fugiat arbitror, qui nostrud distinguantur, nescius si labore ad id export dolore est nescius, hic ita quae doctrina est possumus id nostrud. Te appellat qui mentitum, eu velit constias.Quis consequat ab summis anim e veniam e excepteur. Anim ut nostrud ea summis, duis laborum eu vidisse. Admodum graviterque te ingeniis.
        #
        # Consequat eram quid se quae, aut se tamen elit quem. Illum excepteur aut aliqua dolore, quorum doctrina nam coniunctione ad a malis cernantur, a quorum vidisseconiunctione a fugiat ut probant ex sunt ad se magna hic ipsum, nulla admodum anvoluptate ad amet quo incurreret. Do aute a dolor ne tempor quamquam nonsempiternum ubi ullamco efflorescere id commodo, ea quid irure et consequat, iisdo malis eram enim, cillum nescius voluptate, qui quem arbitror mandaremus nam osunt sint hic incurreret. Summis eiusmod coniunctione.Iis sunt offendit hic nenoster multos summis laborum do vidisse duis elit si quis in oe instituendarum.Quorum cohaerescant quibusdam nisi deserunt, anim admodum occaecat. Illumofficia ita amet cillum, ut quis praesentibus, iudicem summis ita proidentrelinqueret ea constias exercitation ut mentitum, ne fore officia quo voluptatene commodo est tamen iudicem qui distinguantur se te magna deserunt praetermissum.''')

        self.text.config(state=DISABLED)


        self.tips = Label(self.labelframe, text="Tips:")

        self.tips.pack(anchor="w")

        self.tipstext = tkinter.Text(self.labelframe, width=1, height = 2, wrap=WORD, bg= TEXTBOX_BG)
        self.tipstext.pack(fill=tkinter.X, expand=False)

        self.tipstext.insert(END, "Slow down\nGood Volume")






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
#
# #size of the window
#
# width = root.winfo_screenwidth()
# height = root.winfo_screenheight()
# root.geometry('8000x600')


app = Window(root)
root.mainloop()
