from cx_Freeze import setup,Executable
import sys
import os 

base = None

if sys.platform == 'win32':
    base = "Win32GUI"

os.environ['TCL_LIBRARY'] = r"C:\Users\Birud\AppData\Local\Programs\Python\Python39\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\Birud\AppData\Local\Programs\Python\Python39\tcl\tk8.6"

bdist_msi_option={
    "add_to_path" : False,
    "install_icon" : "icon.ico"
}

build_exe_option = {
    "packages":["tkinter","os"], 
    "include_files":["icon.ico",'tcl86t.dll','tk86t.dll', 'assets','model']
}

executables = [
    Executable(
        "Cilios.py",
        copyright='Copyright (C) 2022 Cilios',
        base=base,
        icon="icon.ico",
        shortcut_name="Cilios - Brain Tumor Detection",
        shortcut_dir="Cilios"
    ),
]

setup(
    name = "Cilios - Brain Tumor Detection",
    options = {
        "build_exe": build_exe_option,
        "bdist_msi": bdist_msi_option,
    },
    version = "1.5",
    description = "Cilios - Brain Tumor Detection System | Developed By Birat Siku, Sachin Pokharel and Sarila Ngakhusi",
    executables = executables
)