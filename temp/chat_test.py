
import datetime
import os
import signal
import socket
import sys
import threading
import time
import traceback
import yaml

DEFAULT_CONFIG = "config.yaml"
PRIVATE_CONFIG = "private_config.yaml"

logfile = "temp/log3.txt"
def print_to_file(msg):
    with open(logfile, 'a') as f:
        f.write("{}\n".format(msg))

print_to_file("STARTING LOG - {}".format(datetime.datetime.now()))


config = {}
print_to_file("Reading in config files\n")
# Read in configuration values
if os.path.exists(DEFAULT_CONFIG):
    with open("config.yaml") as conf:
        config.update(yaml.safe_load(conf.read()))

if os.path.exists(PRIVATE_CONFIG):
    with open(PRIVATE_CONFIG) as conf:
        config.update(yaml.safe_load(conf.read()))

print_to_file(config)

# open socket
print_to_file("creating socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print_to_file("connecting socket")
s.connect((config["host"], config["port"]))
print_to_file("sending PASS")
s.send(("PASS {}\r\n".format(config["pass"])).encode())
print_to_file("sending NICK")
s.send(("NICK {}\r\n".format(config["nick"])).encode())
print_to_file("sending JOIN")
s.send(("JOIN #{}\r\n".format(config["channel"])).encode())
print_to_file("sending CAP REQ commands")
s.send("CAP REQ :twitch.tv/commands\r\n".encode())
print_to_file("sending CAP REQ tags")
s.send("CAP REQ :twitch.tv/tags\r\n".encode()) 
print_to_file("sending CAP REQ membership")
s.send("CAP REQ :twitch.tv/membership\r\n".encode()) 

print_to_file("joining room")
#join room
readbuffer = ""
loading = True
while loading:
    readbuffer = readbuffer + s.recv(1024).decode()
    temp = (readbuffer.split("\r\n"))
    readbuffer = temp.pop()

    for line in temp:
        print_to_file("+ {}".format(line))
        if "End of /NAMES list" in line:
            loading = False

# print_to_file time of day, once every couple seconds
# while True:
message_temp = "PRIVMSG #{} :{}".format(config["channel"], datetime.datetime.now())
s.send((message_temp + "\r\n").encode())
time.sleep(3)


while True:
    response = s.recv(1024).decode()

    if response == "PING :tmi.twitch.tv\r\n":
        s.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        print_to_file("Pinged by twitch, ponging.. ")

    else:
        print_to_file("{}".format(response))

