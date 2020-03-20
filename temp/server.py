#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
import threading
import time
from tkinter import *
from tkinter import ttk

# from common.utils import get_config
# config = get_config()

# num_leds = config["num_leds"]
num_leds = 60
pixel_order = "GRB"

# LEDS / Tk stuff

def set_up_window(root):

    window_h = 25
    window_w = 1200

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
    # leds = set_up_window(root)
    # print(root.grid_slaves())

    leds = []
    for i in range(num_leds):
        f = Frame(master=root, bd=2, relief=RAISED)
        f.grid(row=0, column=i, sticky="NESW", pady=1, padx=2)  # , padx=1, pady=10, ipadx=3, ipady=12, sticky="NESW")
        f.configure(background="black")
        leds.append(f)
    return leds

def update_pixels(leds, msg):
    # print("Message length: {}".format(len(msg) / 3))
    for i in range(int(len(msg) / 3)):
        color = "#{:02x}{:02x}{:02x}".format(msg[i*3], msg[i*3 + 1], msg[i*3 + 2])
        leds[i].configure(background=color)


# Client connection stuff

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("{},{}".format(num_leds, pixel_order), "utf8"))
        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument, and the leds

    while True:
        msg = client.recv(BUFSIZ)
        if len(msg) == 0:
            print("Received no bytes...")
            root.quit()
            break
        # print("Received {} bytes".format(len(msg)))
        if msg != bytes("quit", "utf8"):
            # print(msg)
            update_pixels(leds, msg[1:])
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            print(bytes("Client has left.", "utf8"))
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


RGB = (0, 1, 2)
GRB = (1, 0, 2)
RGBW = (0, 1, 2, 3)
GRBW = (1, 0, 2, 3)

        
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

SHUTDOWN = threading.Event()

if __name__ == "__main__":

    # Setup Tk window, and LEDs
    root = Tk()
    leds = set_up_window(root)
    
    # Setup Socket Server Thread
    
    # Start Tk Thread
    # Start LED Thread



    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    root.quit()

    ACCEPT_THREAD.join()
    
    SERVER.close()