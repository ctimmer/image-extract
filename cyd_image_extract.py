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

USE_SDCARD = True

from image_extract import ImageExtract
#

#-------------------------------------------------------------------------------
# DISPLAY initialize
#-------------------------------------------------------------------------------
SPI_ID = 1
BAUDRATE = 60_000_000
SCK_PIN = 14
MOSI_PIN = 13
CS_PIN = 15
DC_PIN = 2
RST_PIN = 15
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
ROTATION = 90
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240



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
        spi = SPI(SPI_ID,
                    baudrate = BAUDRATE,
                    sck = Pin (SCK_PIN),
                    mosi = Pin (MOSI_PIN))
        disp = Display (spi = spi ,
                        cs = Pin (CS_PIN) ,
                        dc = Pin (DC_PIN) ,
                        rst = Pin (RST_PIN) ,
                        width = DISPLAY_WIDTH ,
                        height = DISPLAY_HEIGHT ,
                        rotation = ROTATION)
        # Turn on display backlight
        backlight = Pin(21, Pin.OUT)
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

SD_SPI_ID = 1
SD_MISO_PIN = 19
SD_MOSI_PIN = 23
SD_SCK_PIN = 18
SD_CS_PIN = 5

def initialize_sdcard (mount_dir = "/sd") :
    #print ("initialize_sdcard")
    if not USE_SDCARD :
        return
    from modules.sdcard import SDCard
    from machine import SoftSPI
    try :
        spi = SoftSPI (SD_SPI_ID ,
                        sck = Pin (SD_SCK_PIN) ,
                        mosi = Pin (SD_MOSI_PIN) ,
                        miso = Pin (SD_MISO_PIN))
        sd = SDCard (spi ,
                    cs = Pin (SD_CS_PIN))
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

image_extract_150 = ImageExtract ("images_150.bin")
image_extract_100 = ImageExtract ("images_100.bin")

def display_image_index_100 (image_idx : int, x = 0, y = 0) :
    img = image_extract_100.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_id_100 (image_name : str, x = 0, y = 0) :
    img = image_extract_100.get_image_id (image_name)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])

def display_image_index_150 (image_idx : int, x = 0, y = 0) :
    img = image_extract_150.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_id_150 (image_name : str, x = 0, y = 0) :
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
#image_extract_150.show ()



print ("Large images")
display.clear (WHITE)
#display_image_id_150 ("glacier", 5, 10)
#display_image_id_150 ("mountain", 160, 10)
display_image_id_150 ("bear", 5, 10)
display_image_id_150 ("river", 160, 10)
time.sleep (5)

print ("Small images")
display.clear (BLUE)
display_image_index_100 (0, 0, 10)
display_image_index_100 (1, 105, 10)
display_image_index_100 (2, 210, 10)
display_image_index_100 (3, 0, 115)
display_image_index_100 (4, 105, 115)
display_image_index_100 (5, 210, 115)
time.sleep (5)

print ("Mixed images")
display.clear (BROWN)
display_image_id_150 ("mountain", 20, 30)
display_image_id_100 ("kennecott", 180, 30)
display_image_id_100 ("iditarod", 180, 120)

image_extract_100.shut_down ()
image_extract_150.shut_down ()
