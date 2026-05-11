import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_video():
    video = filedialog.askopenfilename(title="Select Video")
    video_path.set(video)

def select_audio():
    audio = filedialog.askopenfilename(title="Select Audio")
    audio_path.set(audio)

def select_logo1():
    logo = filedialog.askopenfilename(title="Select Logo 1")
    logo1_path.set(logo)

def select_logo2():
    logo = filedialog.askopenfilename(title="Select Logo 2")
    logo2_path.set(logo)

def generate():
    video = video_path.get()
    audio = audio_path.get()
    logo1 = logo1_path.get()
    logo2 = logo2_path.get()

    if not video or not audio or not logo1 or not logo2:
        messagebox.showerror("Error", "Please select all files")
        return

    output = filedialog.asksaveasfilename(defaultextension=".mp4")

    command = f'''
    ffmpeg -y -i "{video}" -i "{audio}" -i "{logo1}" -i "{logo2}" ^
    -filter_complex "[0:v][2:v]overlay=10:10[tmp1];[tmp1][3:v]overlay=W-w-10:H-h-10[v]" ^
    -map "[v]" -map 1:a -shortest ^
    -c:v libx264 -c:a aac ^
    "{output}"
    '''

    os.system(command)
    messagebox.showinfo("Done", "Video Generated!")

root = tk.Tk()
root.title("Video Overlay Tool")

video_path = tk.StringVar()
audio_path = tk.StringVar()
logo1_path = tk.StringVar()
logo2_path = tk.StringVar()

tk.Button(root, text="Select Video", command=select_video).pack()
tk.Button(root, text="Select Audio", command=select_audio).pack()
tk.Button(root, text="Select Logo 1", command=select_logo1).pack()
tk.Button(root, text="Select Logo 2", command=select_logo2).pack()
tk.Button(root, text="Generate Video", command=generate).pack()

root.mainloop()