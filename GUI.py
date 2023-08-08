import os
import sys
import SarcLib
import libyaz0
import struct
import math
import ast
from compress import pack 
from compress import pack_folder_to_blarc
import customtkinter
import tkinter
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter.filedialog import askdirectory
from customtkinter import *
from threading import Thread
import shutil
from download import download_extract_copy
from patch import create_patch_files
from functions import float2hex
from decompress import start_decompress
from script import patch_blarc

class PrintRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.buffer = ""
        self.text_widget.configure(state='disabled')  # Disable user input
        self.text_widget.tag_configure("custom_tag", background='lightgray', foreground='black')

    def write(self, text):
        self.buffer += text
        self.text_widget.configure(state='normal')  # Enable writing
        self.text_widget.insert("end", text, "custom_tag")  # Apply custom_tag to the inserted text
        self.text_widget.see("end")
        self.text_widget.configure(state='disabled')  # Disable user input again

    def flush(self):
        self.text_widget.configure(state='normal')  # Enable writing
        try:
            self.text_widget.insert("end", self.buffer, "custom_tag")  # Apply custom_tag to the buffered text
        except Exception as e:
            self.text_widget.insert("end", f"Error: {e}\n", "custom_tag")  # Display the exception message with custom_tag
        finally:
            self.text_widget.see("end")
            self.text_widget.configure(state='disabled')  # Disable user input again
            self.buffer = ""

scaling_factor = 0.762
HUD_pos = "corner"


    #repack the layour.lyarc folder into file
    #repack the folder into a szs file
    #move them to the correct place

def patch_blyt(filename, pane, operation, value):
    print(f"Scaling {pane} by {value}")
    offset_dict = {'shift_x': 0x40, 'shift_y': 0x48, 'scale_x': 0x70, 'scale_y': 0x78} 
    full_path = filename
    with open(full_path, 'rb') as f:
        content = f.read().hex()
    start_rootpane = content.index(b'RootPane'.hex())
    pane_hex = str(pane).encode('utf-8').hex()
    start_pane = content.index(pane_hex, start_rootpane)
    idx = start_pane + offset_dict[operation]
    content_new = content[:idx] + float2hex(value) + content[idx+8:]
    with open(full_path, 'wb') as f:
        f.write(bytes.fromhex(content_new))


def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(text_color=("#000000", "#FFFFFF"))

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(text_color='gray')

def select_mario_folder():
    global scaling_factor
    ratio_value = (int(numerator.get()) / int(denominator.get()))
    scaling_factor = (16/9) / (int(numerator.get()) / int(denominator.get()))
    input_folder = askdirectory()
    text_folder = os.path.join(input_folder, "SMO-AAR")
    patch_folder = os.path.join(input_folder, "SMO-AAR", "exefs")

    # Clean up the working directory
    if os.path.exists(text_folder):
        shutil.rmtree(text_folder)

    # Download the SMO Layout Files
    download_extract_copy(input_folder)

    # Create the PCHTXT Files
    create_patch_files(patch_folder, str(ratio_value), str(scaling_factor))
    romfs_folder = os.path.join(input_folder, "SMO-AAR", "romfs", "LayoutData")

    # Decomperss SZS and Lyarc Files
    start_decompress(romfs_folder)

    # Perform Pane Strecthing
    patch_blarc(str(ratio_value), HUD_pos, text_folder)

    # Compress layout folders and delete them
    for root, dirs, files in os.walk(input_folder):
        if "layout" in dirs:
            layout_folder_path = os.path.join(root, "layout")
            layout_lyarc_path = os.path.join(root, "layout.lyarc")
            pack_folder_to_blarc(layout_folder_path, layout_lyarc_path)
            shutil.rmtree(layout_folder_path)
    
    # Compress all remaining folders to SZS and delete them
    for dir_name in os.listdir(romfs_folder):
        dir_path = os.path.join(romfs_folder, dir_name)
        if os.path.isdir(os.path.join(romfs_folder, dir_name)):
            szs_output_path = os.path.join(romfs_folder, f"{dir_name}.szs")
            pack_folder_to_blarc(os.path.join(romfs_folder, dir_name), szs_output_path)
            shutil.rmtree(dir_path)

    print("We are done!")

def do_stuff():
    sys.stdout = PrintRedirector(scrolled_text)
    t = Thread(target=select_mario_folder)
    t.start()

root = customtkinter.CTk()
root.title(f"AAR for Super Mario Odyssey")
root.geometry("500x520")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")  

frame2 = customtkinter.CTkFrame(master=root)

scrolled_text = scrolledtext.ScrolledText(master=root, width=50, height=18, font=("Helvetica", 10))
scrolled_text.pack(pady=30)

bntx_folder_button = customtkinter.CTkButton(master=root, text="Select Mario Layout Folder", fg_color="red", hover_color="pink", command=do_stuff)
bntx_folder_button.pack(pady=15)

numerator_var = StringVar(value="21")
denominator_var = StringVar(value="9")

ratiolabel = customtkinter.CTkLabel(root, text="Enter Aspect Ratio:")
ratiolabel.pack()
numerator = customtkinter.CTkEntry(root, textvariable=numerator_var)
numerator.bind("<FocusIn>", lambda event: handle_focus_in(numerator, "21"))
numerator.bind("<FocusOut>", lambda event: handle_focus_out(numerator, "21"))
numerator.pack(side="left", padx=20)
numerator.configure(text_color='gray')
denominator = customtkinter.CTkEntry(root, textvariable=denominator_var)
denominator.bind("<FocusIn>", lambda event: handle_focus_in(denominator, "9"))
denominator.bind("<FocusOut>", lambda event: handle_focus_out(denominator, "9"))
denominator.configure(text_color='gray')
denominator.pack(side="right", padx=20)


root.mainloop()