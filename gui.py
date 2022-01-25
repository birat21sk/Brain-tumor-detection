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

from _global import ASSETS_PATH
from _config import Window

def canvas_mapped(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')

def detect():
    try:
        result_resized_img = input_img.resize((284,284))
        result_img_tk = ImageTk.PhotoImage(result_resized_img) 
        
        show_img=Label(canvas,image = result_img_tk,bd=0)
        show_img.image = result_img_tk
        show_img.place(x=68,y=101)
        canvas.itemconfig(pred_result, text="text has changed!")
        print("Detect clicked")

    except Exception as e:
        print("\nSelect the MRI image first")
        mb.showinfo("No image selected","Please select the MRI image first")

def get_image(e):
    global input_img_path
    global input_img
    try:
        input_img_path = filedialog.askopenfilename()
        path_entry.delete(0, 'end')
        path_entry.insert(0, input_img_path)
        
        input_img = Image.open(input_img_path)
        resized_input_img = input_img.resize((208,208))

        input_image_tk = ImageTk.PhotoImage(resized_input_img) 
        
        show_img=Label(canvas,image = input_image_tk,bd=0)
        show_img.image = input_image_tk
        show_img.place(x=463,y=136)

    except AttributeError as e:
        print("Please select the file")
        mb.showerror("No file selected","No file was selected")

def get_pos(e):
    global xwin
    global ywin

    xwin = e.x
    ywin = e.y

def minimize():
    root.update_idletasks()
    root.overrideredirect(False)
    root.state('iconic') 

def move_app(e): 
    root.geometry(f'+{e.x_root - 672}+{e.y_root - 20}')

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

#====================================== UI ======================================#

root = Tk()

#===================Canvas===================#
global canvas
canvas = Canvas(
    root,
    bg = "#000000",
    height = 531,
    width = 750,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)
canvas.bind("<Map>", canvas_mapped)
canvas.place(x = 0, y = 0)

canvas_background_img = PhotoImage(file = relative_to_assets("background.png"))
canvas_background = canvas.create_image(375, 265,image=canvas_background_img)

#===================Canvas===================#

#====================Custom Title Bar====================#
#===============Title===============#
canvas.create_text(
    17.0,
    14.91,
    anchor="nw",
    text="Brain Tumor Detection",
    fill="#FFFFFF",
    font=("OpenSansRoman-Regular",int(12.62))
)
#===============Title===============#

#===============Drag Button===============#
drag_button = PhotoImage(file=relative_to_assets("button_d.png"))
button_5 = Button(
    image=drag_button,
    borderwidth=0,
    highlightthickness=0,
    bg="#51848F",
    activebackground='#51848E', 
    relief="flat",
    cursor="diamond_cross"
)
button_5.place(
    x=672.0,
    y=18.91,
    width=9.0,
    height=11.99
)
button_5.bind("<B1-Motion>",move_app)
button_5.bind("<Button-1>", get_pos)
#===============Drag Button===============#

#===============Minimize Button===============#
min_button = PhotoImage(file=relative_to_assets("button_m.png"))
button_4 = Button(
    image=min_button,
    borderwidth=0,
    bg="#51848F",
    activebackground='#51848E',
    highlightthickness=0,
    command=minimize,
    relief="flat",
    cursor="hand2"
)
button_4.place(
    x=695.0,
    y=15.91,
    width=8.31,
    height=20.26
)
#===============Minimize Button===============#

#===============Close Button===============#
close_button = PhotoImage(file=relative_to_assets("button_x.png"))
button_3 = Button(
    image=close_button,
    borderwidth=0,
    highlightthickness=0,
    bg="#51848F",
    activebackground='#51848E',
    command=canvas.quit,
    relief="flat",
    cursor="hand2"
)
button_3.place(
    x=713.0,
    y=14.91,
    width=18.18,
    height=20.29
)
#===============Close Button===============#

#====================Custom Title Bar====================#


#====================Input Block====================#

canvas.create_text(
    511.89,
    95.91,
    anchor="nw",
    text="Image Upload",
    fill="#FFFFFF",
    font=("OpenSansRoman-Regular",int(16.622))
) 

#Input Image 
dummy_input_img = PhotoImage(file=relative_to_assets("image_1.png"))
dummy_input_img_show = canvas.create_image(
    567.0,
    239.91,
    image=dummy_input_img
)

#===============Get Image Path===============#

path_entry_img = PhotoImage(file=relative_to_assets("entry_1.png"))
path_entry_bg = canvas.create_image(
    567.0,
    378.91,
    image=path_entry_img)

path_entry = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font=("OpenSansRoman-Regular",int(10)))
path_entry.insert(0,'Choose file...')
path_entry.place(
    x=467.0,
    y=364.91,
    width=200.0,
    height=26.0
)
path_entry.bind("<1>", get_image)

#===============Get Image Path===============#

#===============Browse Button===============#
browse_btn_img = PhotoImage(file=relative_to_assets("button_1b.png"))
browse_btn = Button(
    image=browse_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("Browse clicked"),
    relief="flat",
    cursor="hand2"
)
browse_btn.place(
    x=467.0,
    y=417.91,
    width=92.5,
    height=36.36
) 
browse_btn.bind("<1>", get_image)
#===============Browse Button===============#

 
#===============Detect Button===============#
detect_btn_img = PhotoImage(file=relative_to_assets("button_2d.png"))
detect_btn = Button(
    image=detect_btn_img,
    borderwidth=0,
    highlightthickness=0,
    command = detect,
    relief="flat",
    cursor="hand2"
)
detect_btn.place(
    x=573.0,
    y=417.91,
    width=92.5,
    height=36.36
) 
#===============Detect Button===============#

#====================Input Block====================#


#===============Result Block===============#

pred_result = canvas.create_text(
70.0,
418.91,
anchor="nw",
text="Result Summary",
fill="#FFFFFF",
font=("OpenSansRoman-Regular",int(16.62)))
#===============Result Block===============#

#====================================== UI ======================================#

win = Window(root)
root.mainloop()