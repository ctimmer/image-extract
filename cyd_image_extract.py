#
################################################################################
#
# MIT License
#
# Copyright (c) 2026 Curt Timmerman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
################################################################################
#
# Cheap Yellow Display - ImageExtract demo
#

import os
from machine import SPI, Pin

import time
import json

from modules.ili9341 import Display, color565
#from modules.xglcd_font import XglcdFont

USE_SDCARD = False

from image_extract import ImageExtract

#-------------------------------------------------------------------------------
# DISPLAY initialize
#-------------------------------------------------------------------------------
DISPLAY_SPI_ID = 1
DISPLAY_BAUDRATE = 60_000_000
DISPLAY_SCK_PIN = 14
DISPLAY_MOSI_PIN = 13
DISPLAY_CS_PIN = 15
DISPLAY_DC_PIN = 2
DISPLAY_RST_PIN = 15
DISPLAY_BACKLIGHT_PIN = 21
#
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_ROTATION = 90
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
#
WHITE = color565 (255,255,255)
BLACK = color565 (0,0,0)
RED = color565 (255,0,0)
GREEN = color565 (0,255,0)
BLUE = color565 (0,0,255)
BROWN = color565 (165,42,42)
YELLOW_ORANGE = color565 (255,179,67)

def initialize_display () :
    #print ("initialize_display")
    disp = None
    try :
        spi = SPI(DISPLAY_SPI_ID ,
                    baudrate = DISPLAY_BAUDRATE ,
                    sck = Pin (DISPLAY_SCK_PIN) ,
                    mosi = Pin (DISPLAY_MOSI_PIN))
        disp = Display (spi = spi ,
                        cs = Pin (DISPLAY_CS_PIN) ,
                        dc = Pin (DISPLAY_DC_PIN) ,
                        rst = Pin (DISPLAY_RST_PIN) ,
                        width = DISPLAY_WIDTH ,
                        height = DISPLAY_HEIGHT ,
                        rotation = DISPLAY_ROTATION)
        # Turn on display backlight
        backlight = Pin(DISPLAY_BACKLIGHT_PIN, Pin.OUT)
        backlight.on()
    except Exception as e :
        print ("init display:", e)
        pass
    gc.collect ()
    return disp

# end initialize_display #

#-------------------------------------------------------------------------------
## SD card initialize
#-------------------------------------------------------------------------------

SD_SPI_SLOT = 2
SD_MISO_PIN = 19
SD_MOSI_PIN = 23
SD_SCK_PIN = 18
SD_CS_PIN = 5

def initialize_sdcard (mount_dir = "/sd") :
    #print ("initialize_sdcard")
    if not USE_SDCARD :
        return
    from machine import SDCard
    try :
        sd = SDCard(slot = SD_SPI_SLOT ,
                    sck = Pin (SD_SCK_PIN) ,
                    miso = Pin (SD_MISO_PIN) ,
                    mosi = Pin (SD_MOSI_PIN) ,
                    cs = Pin (SD_CS_PIN))
        # Print SD card info (seems to be card size and sector size?)
        #print(sd.info())
        # Mount the SD card
        os.mount(sd, mount_dir)
    except Exception as e :
        print (e)
        return None
    gc.collect ()
    return mount_dir

# end initialize_sdcard

################################################################################
# MAIN
################################################################################

display = initialize_display ()
initialize_sdcard ()

# Regular
image_extract_150 = ImageExtract ("/images_150.bin")
# Alternate
image_extract_100 = ImageExtract ()
image_extract_100.initialize_image_file ("/images_100.bin")

# SD Card:
#image_extract_150 = ImageExtract ("/sd/images_150.bin")
#image_extract_100 = ImageExtract ("/sd/images_100.bin")

def display_image_index_100 (image_idx : int, x : int = 0, y : int = 0) :
    img = image_extract_100.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_id_100 (image_name : str, x : int = 0, y : int = 0) :
    img = image_extract_100.get_image_id (image_name)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])

def display_image_index_150 (image_idx : int, x : int = 0, y : int = 0) :
    img = image_extract_150.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_id_150 (image_name : str, x : int = 0, y : int = 0) :
    img = image_extract_150.get_image_id (image_name)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])

#image_extract_150.show ()
for ids in [
    ["IMG_0209", "kennecott"] ,
    ["IMG_4851", "iditarod"] ,
    ["mccarthy_Slide242", "glacier"] ,
    ["mccarthy_Slide40", "cabin"] ,
    ["mccarthy_Slide68", "mountain"] ,
    ["mccarthy_Slide79", "bear"] ,
    ["mccarthy_Slide94", "river"]
    ] :
    image_extract_100.rename_id (ids [0], ids [1])
    image_extract_150.rename_id (ids [0], ids [1])
image_extract_150.show ()

image_extract_100.set_default_image_id ("imagenotfound")
image_extract_150.set_default_image_id ("imagenotfound")

print ("Large images")
display.clear (WHITE)
#display_image_id_150 ("glacier", 5, 10) # only room for 2 images
#display_image_id_150 ("mountain", 160, 10)
display_image_id_150 ("bear", 5, 10)
display_image_id_150 ("river", 160, 10)
time.sleep (5)

print ("Small images")
display.clear (BLUE)
display_image_index_100 (1, 0, 10)
display_image_index_100 (2, 105, 10)
display_image_index_100 (3, 210, 10)
display_image_index_100 (4, 0, 115)
display_image_index_100 (5, 105, 115)
display_image_index_100 (6, 210, 115)
time.sleep (5)

print ("Mixed images")
display.clear (BROWN)
display_image_id_150 ("mountain", 20, 30)
display_image_id_100 ("kennecott", 180, 30)
display_image_id_100 ("iditarod", 180, 120)
time.sleep (5)

print ("Error images")
display.clear (YELLOW_ORANGE)
display_image_id_150 ("bad", 20, 30)
display_image_index_100 (999, 180, 30)

image_extract_100.shut_down ()
image_extract_150.shut_down ()
