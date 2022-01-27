from tkinter import *
from PIL import Image,ImageTk

class SplashScreen(Tk):
    def __init__(self,master=None):
        Tk.__init__(self)
        # self.master.attributes("-alpha",0.0)
        self.overrideredirect(True)
        self.alpha = self.attributes("-alpha")
         
        splash_width = 427
        splash_height = 250
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cord = (screen_width/2)-(splash_width/2)
        y_cord = (screen_height/2)-(splash_height/2)
        self.geometry("%dx%d+%d+%d"%(splash_width,splash_height,x_cord,y_cord))
        self.after(2000, self.fade_out) 

        self.fm =Frame(self,width=splash_width,height=splash_height, bg="#51848E").place(x=splash_width/2,y=splash_height/2,anchor='center')
        # self.fm.pack()
        # self.fm.place(anchor='center', relx=0.5, rely=0.5)
        self.img = ImageTk.PhotoImage(Image.open("image_1.png"))
        self.label = Label(self.fm, image = self.img)
        self.label.place(anchor='center', relx=0.5, rely=0.5)

    def fade_out(self):
        if self.alpha > 0:
            self.alpha -= .1
            self.wm_attributes("-alpha",self.alpha)
            self.after(30, self.fade_out)
        if self.alpha <= 0:
            self.destroy()


s= SplashScreen()
s.mainloop()