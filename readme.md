
MakingBot
Getting Started

This project utilizes a Raspberry Pi Zero W as the platform to run the code, connect to wifi, listen to the Twitch chat, and to control the LEDs.
You can get one here:
https://www.adafruit.com/product/3400

There is a version that comes with headers for $14, but they have a 2x20 header for $1 here:
https://www.adafruit.com/product/2822
I personally prefer the color-coded headers for a couple dollars more:
https://www.adafruit.com/product/3907

The Raspberry Pi Zero W does not come with the headers attached, so you'll have to bust out the soldering iron. Have fun, don't burn the house down.

There is no need for buying a case, because the regualar cases for the Pi Zero W won't fit when you put this board on anyway (or it'll cover the Pi, but not the LED board). So, you can 3D print your own, or get a plastic project box or something. I'd recommend getting some kind of case, just to keep the dust and things off it, but that's up to you.

You will also need a Micro SD card. This program is relatively small, and you can use the small installation of Raspian (more on that later). At last check, it all totalled to less than 2 GB. However, if you want to do more things with this bot, or you want to do other things with the Pi Zero W, I'd recommend getting at least a 16 GB.
Amazon is your best source for this. In this case, I got a SanDisk Extreme A2 for no particular reason. It's just what I bought. There really is no need for that in this applicaiton. You can use something like a class 10 with no ill effects.

Next you'll need Raspbian, the operating system for the Raspberry Pi. It is a Linux distribution, and I'm including my notes for installing and running all of this through the console cable so you don't even need a monitor. Therefore, we will get the version without GUI support.
https://downloads.raspberrypi.org/raspbian_lite_latest
If you're not using a monitor, you'll need a console cable. The LED board has a 4 pin header for the console connection, and you can plug into that. The console cable is something you'll need only once for getting all of this set up, but if you want to do more stuff with another Raspberry Pi, I would suggest having one on hand.

However, if you prefer to hook up a monitor to the Raspberry Pi Zero W (You know what, I'm just gonna call it the Pi from here on out), you certainly can. Download one of the larger versions (zip files) here:
https://www.raspberrypi.org/downloads/raspbian/
If you want to use a GUI, you'll need an HDMI monitor, a USB keyboard and mouse, as well as the Mini HDMI to regular HDMI adapter, a Micro USB to regular USB adapter (for your mouse and keyboard), a USB hub (there's only one USB for communication on the Pi, and a Micro USB power adapter.


One more piece of software is required to get started. balenaEtcher is a program to take the .img Raspbian file (inside the zip file you downloaded. Go ahead and unzip that) to the SD card.
Download and install the version for you computer (not for the Pi).
https://www.balena.io/etcher/

Now we can "burn" the SD card. You'll need a reader on your computer (you have one of those, right?). If you don't, they're on Amazon for cheap.
Depending on the type of SD card reader you're using, you may need to use the full size adapter that came with the Micro SD card.

After you've unzipped the Raspbian .img file, insert the Micro SD card into your reader. If prompted, you do not need to format the card or anything, so don't waste your time doing that. balenaEtcher will wipe the card for you before flashing the Micro SD card anyway.
















1 Main function

2 Threads
- listen to channel
- process command

LED Commands
 - fill
 - gradient
 - pattern
 - mirror
 - flash

Advanced LED Commands
 - animate
 - theater
 - scroll
 
LED Pre-defined colors
  * "red": (255, 0, 0),
  * "pink": (255, 128, 128),
  * "orange": (255, 128, 0),
  * "yellow": (255, 255, 0),
  * "light_green": (128, 255, 0),
  * "green": (0, 255, 0),
  * "cyan": (0, 255, 255),
  * "teal": (0, 255, 255),
  * "light_blue": (0, 128, 255),
  * "blue": (0, 0, 255),
  * "purple": (128, 0, 255),
  * "magenta": (255, 0, 255),
  * "fuschia": (255, 0, 128),
  * "gray": (127, 127, 127),
  * "grey": (127, 127, 127),
  * "white": (255, 255, 255),
  * "black": (0, 0, 0)
