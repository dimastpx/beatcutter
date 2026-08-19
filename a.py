import sys
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

ffmpeg_path = resource_path("ffmpeg/ffmpeg.exe")
ffprobe_path = resource_path("ffmpeg/ffprobe.exe")
os.environ["PATH"] = os.path.dirname(ffmpeg_path) + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment

AudioSegment.converter = ffmpeg_path
AudioSegment.ffmpeg = ffmpeg_path
AudioSegment.ffprobe = ffprobe_path

file = ""
beg = 0
mod = 0

root = Tk()
root.title("beat cutter")
root.iconbitmap(default=resource_path("ico.ico"))
root.geometry("480x360")
root.resizable(False, False)

def filesel():
    global file
    file = filedialog.askopenfilename(filetypes=[("audiofiles", ".mp3 .wav")])
    update()

def filesave():
    global file, beg, mod
    tm = float(tempo.get())
    st = float(start.get())
    
    song = AudioSegment.from_file(file)
    part = song[st*1000:]

    arr = []
    
    length = part.duration_seconds*1000
    beat = 1000/tm*60*4

    now = 0
    
    while now < length:
        if mod == 0:
            arr.append(part[now:now+(beat/2)])
        if mod == 1:
            arr.append(part[now+(beat/2):now+beat])
        if mod == 2:
            arr.append(part[now+(beat/2):now+beat]+part[now:now+(beat/2)])
        now += beat
    
    result = sum(arr)

    path = filedialog.asksaveasfilename(filetypes=[("mp3 files", '*.mp3')])
    
    if path != "":
        if not "." in path:
            path = path + ".mp3"
        result.export(path, format="mp3")

def changeMode():
    global mod
    mod += 1
    if mod > 2:
        mod = 0
    if mod == 0:
        mode.config(text="mode: first beats")
    if mod == 1:
        mode.config(text="mode: second beats")
    if mod == 2:
        mode.config(text="mode: seperate beats")

selfile   = ttk.Button(text="select a file",command=filesel)
l1        = ttk.Label(text="tempo:")
tempo     = ttk.Entry(text="110")
tempo.insert(0, "110")
l2        = ttk.Label(text="start from(s):")
start     = ttk.Entry(text="0.784")
start.insert(0, "0.784")
l3        = ttk.Label(text="")
mode      = ttk.Button(text="mode: first beats",command=changeMode)
l4        = ttk.Label(text="")
save      = ttk.Button(text="save",command=filesave)

selfile  .pack(anchor="nw")
l1       .pack(anchor="nw")
tempo    .pack(anchor="nw")
l2       .pack(anchor="nw")
start    .pack(anchor="nw")
l3       .pack(anchor="nw")
mode     .pack(anchor="nw")
l4       .pack(anchor="nw")
save     .pack(anchor="nw")

logo = PhotoImage(file=resource_path("ico.png"))
img = ttk.Label(image=logo)
img.place(x=150,y=30)

def update():
    if file == "":
        save.config(state=["disabled"])
    else:
        save.config(state=["enabled"])

    root.mainloop()

update()
