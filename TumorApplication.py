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

from exception import FileTypeException
from prediction import predict_tumor
from preprocess import is_jpg, preprocess
from _global import * 

#for taskbar integration
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

class TumorAppication(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("750x531+150+150") 
        self.configure(bg = "#ffffff")
        self.title("Brain Tumor Detection")
        self.resizable(False, False)
        self.overrideredirect(True) #hides title bar
        self.bind("<Map>", self.canvas_mapped)
        self.after(500, lambda: self.set_taskbar(self))
        self.z=0


    def set_taskbar(self,master): 
        hwnd = windll.user32.GetParent(master.winfo_id())
        stylew = windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
        stylew = stylew & ~WS_EX_TOOLWINDOW
        stylew = stylew | WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, stylew)
        # re-assert the new window style
        master.wm_withdraw()
        master.after(10, lambda: master.wm_deiconify())

    def minimize(self):
        self.state('withdrawn')
        self.overrideredirect(False)
        self.state('iconic')
        self.z = 1

    def canvas_mapped(self,e): 
        self.overrideredirect(True)   

        if self.z == 1:
            self.set_taskbar(self)
            self.z = 0
    
    def move_app(self,e): 
        self.geometry(f'+{e.x_root - 672}+{e.y_root - 20}')

    def display_image(self,input_img):
        #========== Update UI ==========#
        input_img = input_img.resize((284,284))
        img_tk = ImageTk.PhotoImage(input_img) 
        self.show_img=Label(self.canvas,image = img_tk,bd=0)
        self.show_img.image = img_tk
        self.show_img.place(x=70,y=101)
        #========== Update UI ==========#

    def detect_tumor(self):
        try:        
            self.img_is_jpg = is_jpg(self.input_img_path)
            
            if self.img_is_jpg:
                self.img_to_pred = preprocess(self.input_img_path)
                
                self.result = predict_tumor(self.img_to_pred)
                self.result = self.result.flatten()
                self.result = round(self.result[0],4)

                if self.result > 0.5:
                    self.canvas.itemconfig(self.pred_result, text="Tumor detected ")
                    self.canvas.itemconfig(self.pred_result_summary, text="Tumor was detected in the MRI image with with "+str((self.result*100))+"% confidence")
                elif self.result < 0.5:
                    self.canvas.itemconfig(self.pred_result, text="Tumor not detected")
                    self.canvas.itemconfig(self.pred_result_summary, text="Tumor was Not detected in the MRI image with with "+str((self.result*100))+"% confidence")
                
            self.display_image(self.input_img)           

            print("hey")
            # else:
            #     raise FileTypeException
        
        except FileTypeException as fe:
            print("Error: File type unknown")
            mb.showerror("Unknown file type","Error: File Type Unknown, select jpg image")

        except Exception as e:
            # print("\nSelect the MRI image first")
            print(e)
            mb.showinfo("No image selected","Please select the MRI image first")

    def get_image(self,e):
        # global input_img_path
        # global input_img
        try:
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
                self.show_img.place(x=463,y=136)
            else:
                raise FileTypeException

        except FileTypeException:
            print("Error: File type unknown")
            mb.showerror("Unknown file type","Error: File Type Unknown, select jpg image")

        except AttributeError:
            print("Please select the file")
            mb.showerror("No file selected","No file was selected")

    def custom_title_bar(self): 
        #===============Title===============#
        self.canvas.create_text(
            17.0,
            14.91,
            anchor="nw",
            text="Brain Tumor Detection",
            fill="#FFFFFF",
            font=("OpenSansRoman-Regular",10)
        )
        #===============Title===============#

        #===============Drag Button===============#
        self.drag_button = PhotoImage(file= self.relative_to_assets("button_d.png"))
        self.button_5 = Button(
            image=self.drag_button,
            borderwidth=0,
            highlightthickness=0,
            bg="#51848F",
            activebackground='#51848E', 
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
            bg="#51848F",
            activebackground='#51848E',
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
            bg="#51848F",
            activebackground='#51848E',
            command=self.canvas.quit,
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
        #====================Input Block====================#
        self.canvas.create_text(
            511.89,
            95.91,
            anchor="nw",
            text="Image Upload",
            fill="#FFFFFF",
            font=("OpenSansRoman-Regular",int(16.62))
        ) 
        self.img = PhotoImage(file=self.relative_to_assets('image_1.png'))
        self.canvas.create_image(463,136, anchor='nw', image=self.img)
        self.imgs = PhotoImage(file=self.relative_to_assets('entry_1.png'))
        self.canvas.create_image(463,365, anchor='nw', image=self.imgs)
        
        self.path_entry = Entry(
            bd = 0,
            bg = "#ffffff",
            highlightthickness = 0,
            font=("OpenSansRoman-Regular",int(10)))
        self.path_entry.insert(0,'Choose file (only jpg)...')
        self.path_entry.place(
            x=467.0,
            y=364.91,
            width=200.0,
            height=26.0
        )
        self.path_entry.bind("<1>", self.get_image)

        #===============Browse Button===============#
        self.browse_btn_img = PhotoImage(file=self.relative_to_assets("button_1b.png"))
        self.browse_btn = Button(
            image=self.browse_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("Browse clicked"),
            relief="flat",
            cursor="hand2"
        )
        self.browse_btn.place(
            x=463.0,
            y=415.0,
            width=92.5,
            height=36.36
        ) 
        self.browse_btn.bind("<1>", self.get_image)
        #===============Browse Button===============#


        #===============Detect Button===============#
        self.detect_btn_img = PhotoImage(file=self.relative_to_assets("button_2d.png"))
        self.detect_btn = Button(
            image=self.detect_btn_img,
            borderwidth=0,
            highlightthickness=0,
            command = self.detect_tumor,
            relief="flat",
            cursor="hand2"
        )
        self.detect_btn.place(
            x=577.0,
            y=415.0,
            width=92.5,
            height=36.36
        ) 
        #===============Detect Button===============#
        #====================Input Block====================#

    def result_block(self):
        #===============Result Block===============#
        self.pred_result = self.canvas.create_text(
            70.0,
            400.0,
            width=290,
            anchor="nw", 
            fill="#FFFFFF",
            font=("OpenSansRoman-Regular",int(16.62))
        )
        self.pred_result_summary = self.canvas.create_text(
            70.0,
            435.91,
            width=290,
            anchor="nw", 
            fill="#FFFFFF",
            font=("OpenSansRoman-Regular",10)
        )
        #===============Result Block===============#

    def create_canvas(self,background_image):        
        canvas = Canvas(self,bg = "#000000",height = 531,width = 750,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas_background_img = PhotoImage(file = background_image)
        canvas.create_image(0, 0,image=self.canvas_background_img,anchor='nw')
        canvas.place(x = 0, y = 0) 
        return canvas
        
    def create_ui(self):
        self.canvas = self.create_canvas(self.relative_to_assets('background.png'))
        
        self.custom_title_bar()
        self.input_block()
        self.result_block()        


    def relative_to_assets(self,path: str) -> Path:
        return ASSETS_PATH / Path(path)
 
def main(): 
    # destroy splash window
    splash_root.destroy()
    
    app = TumorAppication()
    app.create_ui()
    app.mainloop()


if __name__ == '__main__':
    splash_root = Tk()
    
    # Adjust size
    splash_root.geometry("200x200")
    
    # Set Label
    splash_label = Label(splash_root,text="Splash Screen",font=18)
    splash_label.pack()
    
    splash_root.after(3000,main)
    splash_root.mainloop()

    