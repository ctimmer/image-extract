# image-extract
Merge / Extract raw images for micropython displays

## Quick start

- If you have a CheapYellowDisplay (320x240, ili9341)
  - Flash CYD device with micropython
  - Clone this repository
  - cd image-extract
  - run build_images.bsh
  - Copy the *.bin files to the CYD
  - Copy modules/* to the CYD
  - run cyd_image_extract.py on the CYD.
  - If you have an SD:
    - set the source USE_SDCARD to True. This will initialize the SD interface and mount the SD on /sd.
    - Copy the *.bin files to the SD card.
    - Change to ImageExtract input files to point to "/sd/*" directory.
  - This test application could be easily modified to work with any device. The only methods it uses are "clear" (clears display) and "draw_sprite" (displays raw image).

## Applications

__build_image_file.py__ Builds extract file from 1 or more input image files.

- Parameters
  - --output file_name
  - --thumbnail w h
    - Optional, if omitted image files will be stored with their original size.
    - Causes the generated raw images to be sized to fit in a width,height pixel window.
  - --littleendian
    - Writes raw files in little endian format.
  - picture file(s) 1 or more picture (jpg, png, img, etc) files to be stored in the raw image file.
- Requires Pillow module which at this time has to be installed in a python virtual environment.

__build_images.bsh__ Example usage of build_image_file.py. Input images are in ./test_images/*.

- After running 2 files are created:
  - _images_100.bin_ Raw images that will fit into an 100 by 100 pixel area.
  - _images_150.bin_ Raw images that will fit into an 150 by 150 pixel area.

__image_extract.py__ ImageExtract module. Extracts raw images from extract file for displaying on various microprocessor displays.

- Methods :
  - __init (image_file_name)__
  - __initialize_image_file (image_file_name)__
  - __rename_id (old_id, new_id, delete_old_id)__
  - __rename_index (image_idx, new_id)__
  - __get_image_data (image_idx)__
  - __get_image (image_idx)__
  - __get_image_id (image_id)__
  - __set_default_image (image_idx)__
  - __set_default_image_id (image_id)__
  - __get_default_image ()__
  - __show ()__
    - Used for debugging
    - prints
      - image id, image index
      - image size, image width, image_height
  - __shut_down ()__
    - Closes image_file, if open
    - Initializes attributes

## Files

- images_nnn.bin
  - Input to the image_extract module. 
  Created by build_image_file.py.
  - Format
    - Ascii - 10 digit file offset to raw file(s) parameters.
    - Binary - Raw images from the converted picture files.
    - Ascii - json object containing offset, length, width, height of the embedded raw files.