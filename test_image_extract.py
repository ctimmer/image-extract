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
# ImageExtract demo
# Display is not used, ImageExtract calls are printed with arguments
#
import time
import json

from image_extract import ImageExtract

USE_SDCARD = True
SD_SPI_SLOT = 2
SD_MISO_PIN = 19
SD_MOSI_PIN = 23
SD_SCK_PIN = 18
SD_CS_PIN = 5

WHITE = "WHITE"
BLACK = "BLACK"
RED = "RED"
GREEN = "GREEN"
BLUE = "BLUE"
BROWN = "BROWN"
YELLOW_ORANGE = "YELLOW_ORANGE"

class Display () :
    def __init__ (self, *args, **kwargs) :
        self.width = kwargs ["width"]
        self.height = kwargs ["height"]

    def clear (self, color = WHITE) :
        print (f"*Display.clear: color={color}")
    def draw_sprite (self, buf, x, y, w, h) :
        print (f"*Display.draw_sprite: buf_len={len(buf)},w={w},h={h} at pos({x},{y})")
        if (x + w) >= self.width :
            print ("  *Display.draw_sprite: Image exceeds display width")
        if (y + h) >= self.height :
            print ("  *Display.draw_sprite: Image exceeds display height")

DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240
DISPLAY_ROTATION = 90

def initialize_display () :
    #print ("initialize_display")
    disp = None
    try :
        spi = "SPI"
        disp = Display (spi = spi ,
                        cs = "CS_PIN" ,
                        dc = "DC_PIN" ,
                        rst = "RST_PIN" ,
                        width = DISPLAY_WIDTH ,
                        height = DISPLAY_HEIGHT ,
                        rotation = DISPLAY_ROTATION)
        # Turn on display backlight
    except Exception as e :
        print ("init display:", e)
        pass
    return disp
# end initialize_display #

def initialize_sdcard (mount_dir = "/sd") :
    #print ("initialize_sdcard")
    if not USE_SDCARD :
        return
    
    from machine import SDCard, Pin
    import os
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
    return mount_dir

# end initialize_sdcard

#----------------------------------------------------------------------------------
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
    print (f"display_index_100: idx={image_idx} pos=({x},{y})")
    img = image_extract_100.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
    else :
        print (f"  idx={image_idx} NOT FOUND")
def display_image_id_100 (id : str, x : int = 0, y : int = 0) :
    print (f"display_id_100: id={id} pos=({x},{y})")
    img = image_extract_100.get_image_id (id)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
    else :
        print (f"  id={id} NOT FOUND")

def display_image_index_150 (image_idx : int, x : int = 0, y : int = 0) :
    print (f"display_index_150: idx={image_idx} pos=({x},{y})")
    img = image_extract_150.get_image (image_idx)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
    else :
        print (f"  idx={image_idx} NOT FOUND")
def display_image_id_150 (id : str, x : int = 0, y : int = 0) :
    print (f"display_id_150: id={id} pos=({x},{y})")
    img = image_extract_150.get_image_id (id)
    if img is not None :
        display.draw_sprite (img [0], x, y, img [1], img [2])
    else :
        print (f"  id={id} NOT FOUND")

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

image_extract_100.set_default_image_id ("imagenotfound")
image_extract_150.set_default_image_id ("imagenotfound")

print ("Large images")
display.clear (WHITE)
#display_image_id_150 ("glacier", 5, 10) # only room for 2 images
#display_image_id_150 ("mountain", 160, 10)
display_image_id_150 ("bear", 5, 10)
display_image_id_150 ("river", 160, 10)

print ("Small images")
display.clear (BLUE)
display_image_index_100 (1, 0, 10)
display_image_index_100 (2, 105, 10)
display_image_index_100 (3, 210, 10)
display_image_index_100 (4, 0, 115)
display_image_index_100 (5, 105, 115)
display_image_index_100 (6, 210, 115)

print ("Mixed images")
display.clear (BROWN)
display_image_id_150 ("mountain", 20, 30)
display_image_id_100 ("kennecott", 180, 30)
display_image_id_100 ("iditarod", 180, 120)

print ("Error images")
display.clear (YELLOW_ORANGE)
display_image_id_150 ("bad", 20, 30)
display_image_index_100 (999, 180, 30)
#display_image_index_100 (999, 500, 300)

image_extract_100.shut_down ()
image_extract_150.shut_down ()


