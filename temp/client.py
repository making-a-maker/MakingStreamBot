#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import tkinter

num_leds = 60


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


def run_led_sim():
    while not SHUTDOWN:
        for j in range(255):
            pixel_array = []
            pixel_array.append(255)

            for i in range(num_leds):
                pixel_index = (i * 256 // num_leds) + j
                color = wheel(pixel_index & 255)
                pixel_array.append(color[0])
                pixel_array.append(color[1])
                pixel_array.append(color[2])
            
            # print("Sending: {}".format(pixel_array))
            send_bytes(bytes(pixel_array))
            time.sleep(0.05)



def receive():
    received = 0
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # msg_list.insert(tkinter.END, msg)
            print("RECEIVED ({}): {}".format(received, msg))
            received += 1
        except OSError:  # Possibly client has left the chat.
            break

def send_bytes(msg):  # event is passed by binders.
    """Handles sending of messages."""
    client_socket.send(msg)

def send(msg, event=None):  # event is passed by binders.
    """Handles sending of messages."""
    # msg = my_msg.get()
    # my_msg.set("")  # Clears input field.

    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        #  top.quit()


# def on_closing(event=None):
#     """This function is to be called when the window is closed."""
#     my_msg.set("{quit}")
#     send()

# top = tkinter.Tk()
# top.title("Chatter")

# messages_frame = tkinter.Frame(top)
# my_msg = tkinter.StringVar()  # For the messages to be sent.
# my_msg.set("Type your messages here.")
# scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# # Following will contain the messages.
# msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
# scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
# msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
# msg_list.pack()
# messages_frame.pack()

# entry_field = tkinter.Entry(top, textvariable=my_msg)
# entry_field.bind("<Return>", send)
# entry_field.pack()
# send_button = tkinter.Button(top, text="Send", command=send)
# send_button.pack()

# top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

SHUTDOWN = False
led_thread = Thread(target=run_led_sim)
led_thread.start()

receive_thread = Thread(target=receive)
receive_thread.start()
# tkinter.mainloop()  # Starts GUI execution.

try:
    while True:
        msg = input(":> ")
        if msg != "quit":
            send(msg)
        else:
            raise KeyboardInterrupt
except KeyboardInterrupt:
    SHUTDOWN = True
    send("quit")

led_thread.join()
receive_thread.join()
