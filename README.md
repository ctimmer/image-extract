# image-extract
Merge / Extract raw images for micropython displays

## Quick start

- If you have a CheapYellowDisplay (320x240)
  - run build_image_file.py
  - Copy the *.bin files to the device
  - Copy modules/* to the device
  - run cyd_image_extract.py on the device.
  - If you have an SD:
    - set USE_SDCARD to True. This will initialize the SD interface and mound the SD on /sd.
    - Copy the *.bin files to the SD card.
    - Change to ImageExtract input files to point to /sd/*.bin
  - This test application could be easily modified to work with any device. The only methods it uses are clear (clears display) and draw_sprite (display raw image on display).


## Applications

__build_image_file.py__ Builds extract file from 1 or more input image files.

- Parameters
  - --output
  - --thumbnail w h
    - Optional, if omitted image files will be stored with their original size.
    - Causes the generated raw images to be sized to fit in a width,height pixel window.
  - picture file(s) 1 or more picture (jpg, png, img, etc) files to be stored in the raw image file.
- Requires Pillow module which at this time has to be installed in a python virtual environment.

__build_images.bsh__ Example usage of build_image_file.py. Input images are in ./test_images/*.

- After running 2 files are created:
  - _images_100.bin_ Raw images that will fit into an 100 by 100 pixel area.
  - _images_150.bin_ Raw images that will fit into an 150 by 150 pixel area.

__image_extract.py__ ImageExtract module. Extracts raw images from extract file for displaying on various microprocessor displays.

## Files

- images_nnn.bin
  - Input to the image_extract module. 
  Created by build_image_file.py.
  - Format
    - Ascii - 10 digit file offset to raw file(s) parameters.
    - Binary - Raw images from the converted picture files.
    - Ascii - json object containing offset, length, width, height of the embedded raw files.