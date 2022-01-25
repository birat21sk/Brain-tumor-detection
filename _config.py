
class Window():
    def __init__(self,root):
        root.overrideredirect(True) #Hide windows title bar
        root.geometry("750x531+150+150")
        root.configure(bg = "#ffffff")
        root.resizable(False, False)
