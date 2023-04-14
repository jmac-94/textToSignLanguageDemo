import cv2
import os
import PIL
from PIL import ImageTk
import PIL.Image
from tkinter import *
import tkinter as tk

# Global variables
alpha_dir = "alphabet"

def output_image(input_text):
    frames = []
    gif = PIL.Image.new('RGB', (380, 260))
    words = input_text.split()
    print(words)

    for word in words:
        for char in word:
            img_pil = PIL.Image.open(alpha_dir + '/' + str(char).lower() + ".gif")
            img_pil.save("tmp.png")

            # im = im.resize((380,260))  # didn't do it with that resize because low quality
            img_cv2 = cv2.imread("tmp.png")
            img_cv2 = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
            img_cv2 = cv2.resize(img_cv2, (380,260))
            img_frame = PIL.Image.fromarray(img_cv2)
            
            # Repeat the same frame 15 times
            for _ in range(15):
                frames.append(img_frame)

    gif.save("out.gif", save_all=True, append_images=frames, duration=100, loop=0)
    return frames   

class Tk_App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        frame = TtoS(container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

class TtoS(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        cnt = 0
        gif_frames = []
        INPUT_text = None

        label = tk.Label(self, text="Text to Sign", font=("Verdana", 12))
        label.pack(pady=10,padx=10)
        gif_box = tk.Label(self)

        def gif_stream():
            global cnt
            global gif_frames

            # If there is no input text
            if cnt == len(gif_frames):
                return

            img = gif_frames[cnt]
            cnt += 1
            img_tk = ImageTk.PhotoImage(image=img)
            gif_box.imgtk = img_tk
            gif_box.configure(image=img_tk)
            gif_box.after(50, gif_stream)

        def generate_output():
            input_text = INPUT_text.get("1.0", "end-1c")
            print(input_text)
            global gif_frames
            gif_frames = output_image(input_text)
            global cnt
            cnt = 0
            gif_stream()
            gif_box.place(x=400,y=160)

        label_text = tk.Label(self, text="Enter text:")
        INPUT_text = tk.Text(self, height = 4, width = 25)
        display_button = tk.Button(self, height = 2, width = 20, text ="Convert", command = lambda:generate_output())

        label_text.place(x=50, y=160)
        INPUT_text.place(x=50, y=250)
        display_button.pack()


window = Tk_App()
window.iconbitmap('icon.ico')
window.title("Sign Language Recognition")
window.geometry("800x450")
window.mainloop()