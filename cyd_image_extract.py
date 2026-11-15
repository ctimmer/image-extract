'''
MIT License

Copyright (c) 2026 Curt Timmerman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
################################################################################
#
# Cheap Yellow Display - ImageExtract demo
#
import time
#import random
import json

import os
from machine import SPI, Pin

from modules.ili9341 import Display, color565
#from modules.xglcd_font import XglcdFont

USE_SDCARD = True

from image_extract import ImageExtract

'''
class ImageExtract :
    def __init__ (self ,
                  image_file_name : str = None
                  ) :
        #print ("ImageExtract : __init__")
        self.image_file = None
        self.image_config = None
        self.image_count = 0
        self.initialize_image_file (image_file_name)
        gc.collect ()

    def initialize_image_file (self ,
                                image_file_name : str
                                ) :
        #print ("initialize_image_file")
        if image_file_name is None :
            return None
        self.image_file = None
        self.image_config = None
        self.image_count = 0
        try :
            self.image_file = open (image_file_name, "rb")
            offset = self.image_file.read (10)
            param_offset = int (offset)
            self.image_file.seek (param_offset)
            params = self.image_file.read (10000).decode ()
            self.image_config = json.loads (params)
            self.image_count = self.image_config ["count"]
        except Exception as e :
            print ("load_image_file:", e)
            return None
        return self.image_count

    def rename_name (self ,
                        old_name : str ,
                        new_name : str ,
                        remove_old = True) :
        if old_name not in self.image_config ["image_ids"] :
            return None
        self.image_config ["image_ids"][new_name] \
            = self.image_config ["image_ids"][old_name]
        return self.image_config ["image_ids"][new_name] # return index
    def rename_index (self ,
                        image_idx : int ,
                        new_name : str) :
        if image_idx < 0 \
        or image_idx >= self.image_count :
            return None
        #print (self.image_config ["image_ids"][new_name])
        self.image_config ["image_ids"][new_name] = image_idx
        return self.image_config ["image_ids"][new_name] # return index

    def get_image_data (self ,
                        image_idx : int) :
        #print ("get_image_data")
        if image_idx < 0 \
        or image_idx >= self.image_count :
            return None
        return self.image_config ["images"][image_idx]
    
    def get_image (self ,
                   image_idx : int) :
        #print ("get_image")
        image_data = self.get_image_data (image_idx)
        if image_data is None :
            return None
        self.image_file.seek (image_data ["pos"])
        return (self.image_file.read (image_data ["l"]) ,
                image_data ["w"] ,
                image_data ["h"])
    
    def get_image_by_name (self,
                           image_name : str) :
        if image_name not in self.image_config ["images"] :
            return None
        return self.get_image (self.image_config ["images"][image_name])

    def shut_down (self) :
        if self.image_file is not None :
            self.image_file.close ()

# end ImageExtract
'''
#

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

## SD card
SD_SPI_ID = 1
SD_MISO_PIN = 19
SD_MOSI_PIN = 23
SD_SCK_PIN = 18
SD_CS_PIN = 5

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

#----------------------------------------------------------------------------------
display = initialize_display ()
initialize_sdcard ()

image_extract_100 = ImageExtract ("images_100.bin")
image_extract_120 = ImageExtract ("images_120.bin")

def display_image_index_100 (image_idx : int, x = 0, y = 0) :
    img = image_extract_100.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_id_100 (image_name : str, x = 0, y = 0) :
    img = image_extract_100.get_image_id (image_name)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
def display_image_index_120 (image_idx : int, x = 0, y = 0) :
    img = image_extract_120.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])

def display_image_id_120 (image_name : str, x = 0, y = 0) :
    img = image_extract_120.get_image_id (image_name)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])

LARGE_PICS = True

for ids in [
    ["mccarthy_Slide242", "glacier"] ,
    ["mccarthy_Slide40", "cabin"] ,
    ["mccarthy_Slide68", "mountain"] ,
    ["mccarthy_Slide79", "bear"] ,
    ["mccarthy_Slide94", "river"]
    ] :
    image_extract_100.rename_id (ids [0], ids [1])
    image_extract_120.rename_id (ids [0], ids [1])

if LARGE_PICS :
    display_image_id_120 ("glacier", 0, 10)
    display_image_id_120 ("mountain", 125, 10)
    #display_image_id_120 ("bear", 0, 10)
    #display_image_id_120 ("river", 125, 10)
else :
    display_image_index_100 (0, 0, 0)
    display_image_index_100 (1, 105, 0)
    display_image_index_100 (2, 210, 0)
    display_image_index_100 (3, 0, 105)
    display_image_index_100 (4, 105, 105)

image_extract_100.shut_down ()
image_extract_120.shut_down ()
