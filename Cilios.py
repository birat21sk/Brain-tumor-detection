#!/usr/bin/env python
__author__ ="Birat Siku, Sachin Pokharel, and Sarila Ngakhusi"
__copyright__ = "Copyright 2022, Cilios"
__credits__ = ["Birat Siku","Sachin Pokharel","Sarila Ngakhusi"]
__version__ = "1.5.0"
__maintainer__ = "Birat Siku"
__email__ = "birat.siku@hotmail.com"
__status__ = "Production"

from ctypes import windll
from pathlib import Path
from tkinter import (
    Tk,  
    Canvas,
    Entry,
    Label,
    Button,
    PhotoImage, 
    filedialog,
    messagebox as mb
)
from PIL import Image, ImageTk

from pystray import MenuItem as item, Menu
import pystray as pys

from exception import FileTypeException
from prediction import predict_tumor
from preprocess import is_jpg, preprocess
from splash_screen import SplashScreen
from _global import * 
from _config import place_center

class TumorAppication(Tk):
    '''
        Derived class of tkinter.Tk()

        ...

        Attributes
        ----------
        No attributes 

        Methods
        -------
        .List of all methods and what they do

    '''
    def __init__(self):
        '''
        General description of method

        Parameters
        ----------
        list of parameters with type and desc

        Raise
        -----
        if any raise

        Return
        ------
        what is returned
        '''

        Tk.__init__(self)
        x_cord, y_cord = place_center(self,WIN_WIDTH,WIN_HEIGHT)
        self.geometry("%dx%d+%d+%d"%(WIN_WIDTH,WIN_HEIGHT,x_cord,y_cord)) 
        self.configure(bg = "#ffffff")
        self.title("Cilios")
        self.iconbitmap('./icon.ico')
        self.resizable(False, False)
        self.overrideredirect(True) #hides title bar
        self.bind("<Map>", self.canvas_mapped)
        self.after(10, lambda: self.set_taskbar(self)) 
        self.protocol('WM_DELETE_WINDOW', self.hide_window)
        self.min = 0

    def set_taskbar(self,master): 
        """
        Task bar icon
        ...
        Parameter
        ---------
        master: Tkinter object
        """

        hwnd = windll.user32.GetParent(master.winfo_id())  #Process ID (Handle Window)
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew) #Sets a new extended window style.
        # re-assert the new window style
        master.wm_withdraw()
        master.after(10, lambda: master.wm_deiconify())

    #System tray icon
    def set_tray(self):
        """
        System Tray icon on close
        
        """
        icon=Image.open("./icon.ico")
        SEPARATOR = item('- - - - - - - -', None)
        menu=(item('About Cilios', self.show_about),item(SEPARATOR, None),item('Show', self.show_window),item('Exit', self.quit_window))
        icon=pys.Icon("cilios", icon, "Cilios", menu)
        icon.run()
 
    def quit_window(self,icon):
        """
        Exit the application
        ...
        Parameters
        ----------
        icon: Tray icon
        """
        icon.stop()
        self.destroy()

    def show_window(self,icon):
        """
        Show the window again
        ...
        Parameters
        ----------
        icon: Tray icon
        """
        icon.stop()
        self.after(0,self.deiconify())

    def show_about(self): 
        """
        Show the again dialog
        """
        message="Cilios\n-------\nversion: 1.5.0 \n\nA Brain tuor is a growth of abnormal cells that have formed int the brain. Diagnosis of a suspected brain tumor is dependent on appropriate brain imaging. Enhanced Magnetic Resonance Imaging (MRI) is the prefered modality because of its resolution and enhancement with contrast agent. \nCilios is a dedicated software to detect brain tumor in MRI images.\n\nDeveloped by the team: \nBirat Siku\nSachin Pokharel\nSarila Ngakhusi\n\nCopyright (c) 2022 Cilios"
        mb.showinfo("About Cilios",message)

    def hide_window(self):
        """
        Hide the window again
        """
        self.withdraw()
        self.set_tray()
        
    def relative_to_assets(self,path: str) -> Path:
        """
        Map location of assets 
        ...
        Parameters
        ----------
        path: path to assets
        
        Return
        ------
        Return maped path
        """ 
        return ASSETS_PATH / Path(path)

    def canvas_mapped(self,e): 
        """
        Canvas
        ...
        Parameters
        ----------
        e: event
         
        """ 
        self.overrideredirect(True)
        if self.min == 1:
            self.set_taskbar(self)
            self.min = 0
                
    def minimize(self):
        """
        Minimize application 
        """ 
        self.state('withdrawn')
        self.overrideredirect(False)
        self.state('iconic')
        self.min = 1

    def move_app(self,e): 
        """
        Move application
        ...
        Parameters
        ----------
        e: event         
        """ 
        self.geometry(f'+{e.x_root - 672}+{e.y_root - 20}')

    def display_image(self,image_path):
        """
        Show image in result block
        ...
        Parameters
        ----------
        image_path: Path to MRI image
        """ 
        #========== Update UI ==========#
        image = Image.open(image_path)
        resized_img = image.resize((284,284))
        disp_image = ImageTk.PhotoImage(resized_img) 
        self.show_result_img=Label(self.canvas,image = disp_image,bd=0)
        self.show_result_img.image = disp_image
        self.show_result_img.place(x=60,y=101)
        #========== Update UI ==========#
    
    def clear_result(self, e): 
        """
        Clear result screen
        ...
        Parameters
        ----------
        e: event

        Raise
        -----
        AttributeError
        """ 
        try:
            self.show_result_img.place(x=-400,y=0)
            self.show_result_img.destroy()
            self.show_result_img = None
            self.canvas.itemconfig(self.pred_result, text="")
            self.canvas.itemconfig(self.pred_result_summary, text="")
        except AttributeError as ae:
            if DEBUG:
                print("Screen already cleared")
            pass

    def reset_screen(self, e):
        """
        Reset screen
        ...
        Parameters
        ----------
        e: event

        Raise
        -----
        AttributeError
        """ 
        try:
            self.show_img.destroy()
            self.show_result_img.destroy()
            self.show_result_img = None
            self.path_entry.delete(0, END)
            self.path_entry.insert(0, "Choose file (only jpg)...")
            self.canvas.itemconfig(self.pred_result, text="")
            self.canvas.itemconfig(self.pred_result_summary, text="")
            self.input_img_path=None
        except AttributeError as ae:
            if DEBUG:
                print("Reset done already")
            pass

    def detect_tumor(self, e):
        """
        Detect the tumor in MRI image
        ...
        Parameters
        ----------
        e: event

        Raise
        -----
        FileTypeException, NameError, AttributeError, Exception if any
        """ 
        try:
            self.img_is_jpg = is_jpg(self.input_img_path)            
            if self.img_is_jpg:
                self.img_to_pred = preprocess(self.input_img_path)
                self.result = predict_tumor(self.img_to_pred)
                self.result = self.result.flatten()                
                percentage = round(self.result[0]*100,2)
                if self.result[0] > 0.5:
                    self.canvas.itemconfig(self.pred_result, text="Tumor detected ")
                    self.canvas.itemconfig(self.pred_result_summary, text=f'Tumor was DETECTED in the MRI image with {percentage}% confidence.')
                elif self.result[0] < 0.5:
                    self.canvas.itemconfig(self.pred_result, text="Tumor not detected")
                    self.canvas.itemconfig(self.pred_result_summary, text=f'Tumor was NOT DETECTED in the MRI image with {100-percentage}% confidence.')
                
                self.display_image(self.input_img_path) 
            else:
                raise FileTypeException
        
        except FileTypeException as fe:
            if DEBUG:
                print(fe)
            mb.showerror("Unknown file type","Error: File Type Unknown, select jpg image")

        except NameError as ne:
            if DEBUG:
                print(ne)
            mb.showerror("Error","Unable to upload image")

        except AttributeError as ae:
            if DEBUG:
                print(ae)
            mb.showwarning("No image selected","Please select the MRI image first")
            
        except Exception as e:
            if DEBUG:
                print(e)
            mb.showerror("Error","Unexpected Error Occoured! Please try again")

    def get_image(self,e): 
        """
        Show the file dialog to select image from pc
        ...
        Parameters
        ----------
        e: event

        Raise
        -----
        FileTypeException, AttributeError, Exception if any
        """ 
        try:
            self.reset_screen(e)
            self.input_img_path = filedialog.askopenfilename()
            self.img_is_jpg = is_jpg(self.input_img_path)
            if self.img_is_jpg:
                self.path_entry.delete(0, END)
                self.path_entry.insert(0, self.input_img_path) 
                self.input_img = Image.open(self.input_img_path)
                self.resized_input_img = self.input_img.resize((208,208))
                self.input_image_tk = ImageTk.PhotoImage(self.resized_input_img)                 
                self.show_img=Label(self.canvas,image = self.input_image_tk,bd=0)
                self.show_img.image = self.input_image_tk
                self.show_img.place(x=440,y=123)
            else:
                raise FileTypeException

        except FileTypeException as fe: 
            if DEBUG:
                print(fe)
            mb.showerror("Unknown file type","Error: File Type Unknown, select jpg image")
        except AttributeError as ae:
            if DEBUG:
                print(ae)
            mb.showerror("No file selected","No file was selected")
        except Exception as e:
            if DEBUG:
                print(e)
            pass

    def custom_title_bar(self): 
        """
        Custom title bar
        """
        #===============Title===============#
        self.canvas.create_text(
            17.0,
            14.91,
            anchor="nw",
            text="Cilios - Brain Tumor Detection",
            fill="#FFFFFF",
            font=("Montserrat Regular",10)
        )
        #===============Title===============#

        #===============Drag Button===============#
        self.drag_button = PhotoImage(file= self.relative_to_assets("button_d.png"))
        self.button_5 = Button(
            image=self.drag_button,
            borderwidth=0,
            highlightthickness=0,
            bg="#4f9e9b",
            activebackground='#4d9996', 
            relief="flat",
            cursor="diamond_cross"
        )
        self.button_5.place(
            x=672.0,
            y=18.91,
            width=9.0,
            height=11.99
        )
        self.button_5.bind("<B1-Motion>", self.move_app)
        #===============Drag Button===============#

        #===============Minimize Button===============#
        self.min_button = PhotoImage(file=self.relative_to_assets("button_m.png"))
        self.button_4 = Button(
            image=self.min_button,
            borderwidth=0,
            bg="#4f9e9b",
            activebackground='#4d9996',
            highlightthickness=0,
            command=self.minimize,
            relief="flat",
            cursor="hand2"
        )
        self.button_4.place(
            x=695.0,
            y=15.91,
            width=8.31,
            height=20.26
        )
        #===============Minimize Button===============#

        #===============Close Button===============#
        self.close_button = PhotoImage(file=self.relative_to_assets("button_x.png"))
        self.button_3 = Button(
            image=self.close_button,
            borderwidth=0,
            highlightthickness=0,
            bg="#4f9e9b",
            activebackground='#4d9996',
            command=self.hide_window,
            relief="flat",
            cursor="hand2"
        )
        self.button_3.place(
            x=713.0,
            y=14.91,
            width=18.18,
            height=20.29
        )
        #===============Close Button===============#

    def input_block(self):
        """
        Setup Input block
        ... 
        """
        #====================Input Block====================#
        self.canvas.create_text(
            469.0,
            86.0,
            anchor="nw",
            text="Image Upload",
            fill="#FFFFFF",
            font=("Montserrat Regular", int(16.62))
        )
        self.img = PhotoImage(file=self.relative_to_assets('image_1.png'))
        self.canvas.create_image(440,123, anchor='nw', image=self.img)
        self.imgs = PhotoImage(file=self.relative_to_assets('entry_1.png'))
        self.canvas.create_image(440,345, anchor='nw', image=self.imgs)
        
        self.path_entry = Entry(
            bd = 0,
            bg = "#ffffff",
            foreground="#171717",
            highlightthickness = 0,
            font=("Montserrat Regular",int(10)))
        self.path_entry.insert(0,'Choose file (only jpg)...')
        self.path_entry.place(
            x=450.0,
            y=345.91,
            width=190.0,
            height=26.0
        )
        self.path_entry.bind("<1>", self.get_image)

        #===============Browse Button===============#
        self.browse_btn_img = PhotoImage(file=self.relative_to_assets("button_browse.png"))
        
        self.browse_btn = Label(
            self,
            image=self.browse_btn_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        ) 
        self.browse_btn.place(
            x=440.0,
            y=387.0,
            width=93.0,
            height=36.36
        )
        
        self.browse_btn.bind("<1>", self.get_image)
        #===============Browse Button===============#

        #===============Detect Button===============#
        self.detect_btn_img = PhotoImage(file=self.relative_to_assets("button_detect.png"))
        self.detect_btn = Label(
            self,
            image=self.detect_btn_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2",
        )
        self.detect_btn.place(
            x=555.0,
            y=387.0,
            width=93.0,
            height=36.36
        ) 
        self.detect_btn.bind("<1>", self.detect_tumor)
        #===============Detect Button===============#
        #===============Clear Button===============#
        self.clear_btn_img = PhotoImage(file=self.relative_to_assets("button_clear.png"))
        self.clear_btn = Label(
            self,
            image=self.clear_btn_img,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            cursor="hand2"
        )
        self.clear_btn.place(
            x=440.0,
            y=437.0,
            width=93.0,
            height=36.36
        ) 
        self.clear_btn.bind("<1>", self.clear_result)
        #===============Clear Button===============#

        #===============Reset Button===============#
        self.reset_btn_img = PhotoImage(file=self.relative_to_assets("button_reset.png"))
        self.reset_btn = Label(
            self,
            image=self.reset_btn_img,
            borderwidth=0,
            highlightthickness=0, 
            relief="flat",
            cursor="hand2"
        )
        self.reset_btn.place(
            x=555.0,
            y=437.0,
            width=93.0,
            height=36.36
        ) 
        self.reset_btn.bind("<1>", self.reset_screen)        
        #===============Reset Button===============#
        #====================Input Block====================#

    def result_block(self):
        """
        Setup result block
        """
        #===============Result Block===============#
        self.pred_result = self.canvas.create_text(
            60.0,
            399.0,
            width=290,
            anchor="nw", 
            fill="#FFFFFF",
            font=("Montserrat Medium",int(16.62))
        )
        self.pred_result_summary = self.canvas.create_text(
            60.0,
            435.91,
            width=290,
            anchor="nw", 
            fill="#FFFFFF",
            font=("Montserrat Regular",10)
        )
        #===============Result Block===============#

    def create_canvas(self,background_image):
        """
        Create the canvas in application
        ...
        Parameters
        ----------
        background_image: Background image path

        Return
        ------
        return the generated canvas
        """      
        canvas = Canvas(self,bg = "#000000",height = 531,width = 750,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas_background_img = PhotoImage(file = background_image)
        canvas.create_image(0, 0,image=self.canvas_background_img,anchor='nw')
        canvas.place(x = 0, y = 0) 
        return canvas
        
    def create_ui(self):
        """
        Create the application UI 
        """    
        self.canvas = self.create_canvas(self.relative_to_assets('background.png'))
        
        self.custom_title_bar()
        self.input_block()
        self.result_block()        

def main():
    """
    Startup sequence
    """
    splash.destroy()
    app = TumorAppication()
    app.create_ui()
    app.mainloop()

if __name__ == '__main__': 
    splash = SplashScreen()
    splash.after(3000, main)
    splash.mainloop()