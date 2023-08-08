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

def main(input_folder):
    global scaling_factor
    scaling_factor = (16/9) / (int(numerator.get()) / int(denominator.get()))

    # download the Layout folder
    # calculate the scaling factor based on entered aspect ratio
    # generate the pchtxt file

    if not os.path.exists(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist.")
        sys.exit(1)

    if not os.path.isdir(input_folder):
        print("Error: The input must be a folder path.")
        sys.exit(1)

    for file in os.listdir(input_folder):
        if file.lower().endswith(".szs"):
            file_path = os.path.join(input_folder, file)
            extract_blarc(file_path, input_folder)

    #repack the layour.lyarc folder into file
    #repack the folder into a szs file
    #move them to the correct place

def float2hex(f):
    return hex(struct.unpack('>I', struct.pack('<f', f))[0]).lstrip('0x').rjust(8,'0').upper()

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

def extract_blarc(file, output_folder):
    """
    Extract the given archive.
    """
    with open(file, "rb") as inf:
        inb = inf.read()

    while libyaz0.IsYazCompressed(inb):
        inb = libyaz0.decompress(inb)

    name = os.path.splitext(os.path.basename(file))[0]  # Extract the base name of the file without extension
    ext = SarcLib.guessFileExt(inb)

    if ext != ".sarc":
        with open(os.path.join(output_folder, ''.join([name, ext])), "wb") as out:
            out.write(inb)
    else:
        arc = SarcLib.SARC_Archive()
        arc.load(inb)

        root = os.path.join(output_folder, name)  # Output path will be in the specified output folder
        if not os.path.isdir(root):
            os.makedirs(root)

        files = []

        def getAbsPath(folder, path):
            nonlocal root
            nonlocal files

            for checkObj in folder.contents:
                if isinstance(checkObj, SarcLib.File):
                    files.append([os.path.join(path, checkObj.name), checkObj.data])
                else:
                    path_ = os.path.join(root, path, checkObj.name)
                    if not os.path.isdir(path_):
                        os.makedirs(path_)
                    getAbsPath(checkObj, os.path.join(path, checkObj.name))

        for checkObj in arc.contents:
            if isinstance(checkObj, SarcLib.File):
                files.append([checkObj.name, checkObj.data])
            else:
                path = os.path.join(root, checkObj.name)
                if not os.path.isdir(path):
                    os.makedirs(path)
                getAbsPath(checkObj, os.path.join(root, checkObj.name))

        for extracted_file, fileData in files:
            print(f"Unpacking {extracted_file}")
            extracted_file_path = os.path.join(root, extracted_file)
            with open(extracted_file_path, "wb") as out:
                out.write(fileData)

            if extracted_file.endswith("bflyt"):
                patch_blyt(extracted_file_path, "RootPane", "scale_x", scaling_factor)

        layout_lyarc = os.path.join(root, "layout.lyarc")
        if os.path.exists(layout_lyarc):
            extract_blarc(layout_lyarc, root)
            # os.remove(layout_lyarc)

    os.remove(file)

def handle_focus_in(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.configure(text_color=("#000000", "#FFFFFF"))

def handle_focus_out(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.configure(text_color='gray')

def select_mario_folder():
    input_folder = askdirectory()
    main(input_folder)

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