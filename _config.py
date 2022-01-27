from tkinter import Tk

class Iconified(Tk):    
    def __init__(self):
        Tk.__init__(self)
        self.attributes('-alpha', 0.0)

    

# iconifiedme = NewRoot()
# iconifiedme.lower()
# iconifiedme.iconify()
# iconifiedme.title('Spam 2.0')



class Window():
    def __init__(self,root):
        root.overrideredirect(True) #Hide windows title bar
        root.geometry("750x531+150+150")
        root.configure(bg = "#ffffff")
        root.resizable(False, False)
