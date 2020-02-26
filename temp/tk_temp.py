
import threading
import time
from tkinter import *
from tkinter import ttk

num_leds = 60

def set_up_window(root):
    root.grid()
    leds = []
    for i in range(num_leds):
        f = Frame(master=root, bd=2, relief=RAISED)
        f.grid(row=0, column=i, sticky="NESW", pady=1, padx=2)  # , padx=1, pady=10, ipadx=3, ipady=12, sticky="NESW")
        leds.append(f)
    
    
    return leds

def run(root, pixels):
    while True:
        for j in range(255):
            for i in range(num_leds):
                pixel_index = (i * 256 // num_leds) + j
                color = wheel(pixel_index & 255)
                color = "#{:02x}{:02x}{:02x}".format(color[0], color[1], color[2])
                pixels[i].configure(background=color)
            time.sleep(0.0166)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos*3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos*3)
        g = 0
        b = int(pos*3)
    else:
        pos -= 170
        r = 0
        g = int(pos*3)
        b = int(255 - pos*3)
    return r, g, b  # if ORDER == neopixel.RGB or ORDER == neopixel.GRB else (r, g, b, 0)


if __name__ == "__main__":

    window_h = 25
    window_w = 1200

    root = Tk()
    root.height=window_h
    root.width=window_w

    # root.geometry("1000x25")
    root.configure(background="black")
    for c in range(num_leds):
        root.grid_columnconfigure(c, minsize=(window_w / int(num_leds)))
    root.grid_rowconfigure(0, minsize=window_h)
    # print(root.grid_size())
    # print(root.grid_slaves())

    # root.geometry("500x50")
    leds = set_up_window(root)
    # print(root.grid_slaves())
    threading._start_new_thread(run, (root, leds))
    root.mainloop()
