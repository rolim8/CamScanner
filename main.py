import os
import cv2
import sys
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime

fileName = os.environ['USERPROFILE'] + "\Imagens\Capturas de tela"
cancel = False


def prompt_ok():
    global button, save, cancel, repeat
    _cancel_ = True

    save = tk.Button(mainWindow, text="Salvar", command=saveAndExit)
    save.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    save.focus()

    repeat = tk.Button(mainWindow, text="Repetir", command=resume)
    repeat.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)


def saveAndExit():
    global prevImg

    date = datetime.now().strftime("%Y.%m.%d - %Ih %Mm %Ss %p")

    if (len(sys.argv) < 2):
        fp1 = "C:/Users/rolim/OneDrive/Imagens/Capturas de tela" and "C:/Users/rolim/OneDrive/Imagens/Imagens da Câmera"
        filepath = f"{fp1}/{date}.png"

    else:
        filepath = sys.argv[1]

    print("Output file to: " + filepath)
    prevImg.save(filepath)
    mainWindow.quit()


def resume():
    global button, save, repeat, lmain, cancel

    cancel = False

    save.place_forget()
    repeat.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)


try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex)
capWidth = cap.get(3)
capHeight = cap.get(4)

success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)

mainWindow = tk.Tk(screenName="Camera Capture")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)

mainWindow.bind('<Return>', lambda e : saveAndExit())

lmain.pack()


def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)


show_frame()
mainWindow.mainloop()