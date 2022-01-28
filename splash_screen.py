from tkinter import *
from PIL import Image,ImageTk
from _config import place_center

class SplashScreen(Tk):
    def __init__(self,master=None):
        Tk.__init__(self)
        self.overrideredirect(True)
        self.alpha = self.attributes("-alpha")
         
        splash_width = 427
        splash_height = 250

        x_cord, y_cord = place_center(self,splash_width,splash_height)

        self.geometry("%dx%d+%d+%d"%(splash_width,splash_height,x_cord,y_cord))
        self.after(2500, self.fade_out) 
 
        self.fm =Frame(self,width=splash_width,height=splash_height, bg="#ffffff",bd=0).place(x=0,y=0,anchor='nw')
        self.img = ImageTk.PhotoImage(Image.open("./assets/splash.png"))
        self.label = Label(self.fm, image = self.img)
        self.label.place(anchor='center', relx=0.5, rely=0.5)

    def fade_out(self):
        if self.alpha > 0:
            self.alpha -= .1
            self.wm_attributes("-alpha",self.alpha)
            self.after(30, self.fade_out)
        # if self.alpha <= 0:
        #     self.destroy()