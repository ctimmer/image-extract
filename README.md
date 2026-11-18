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
    - image_file_name (optional) File that contains raw images
  - __initialize_image_file (image_file_name)__
    - image_file_name (optional) File that contains raw images
      - If omitted, class attributes are reset
      - image_file is created by __build_image_file.py__
  - __rename_id (old_id, new_id, delete_old_id)__
    - old_id current existing image_id
    - new_id image_id added to reference old_id raw image.
    - delete_old_id (default: True) Determines if old_id is removed.
    - returns new_id image index (success) or None (failed).
  - __rename_index (image_idx, new_id)__
    - image_idx Image to be referenced by new_id
    - new_id Id that will reference image_idx
    - returns image_idx (success) or None (failed).
  - __get_image_data (image_idx)__
    - returns (image, width, height) (success) or None (failed).
  - __get_image (image_idx)__
    - image_idx return raw image for this index.
    - returns (image, width, height) (success) or None (failed).
  - __get_image_id (image_id)__
    - image_id id of raw image to be returned.
    - returns (image, width, height) (success) or None (failed).
  - __set_default_image (image_idx)__
    - Sets the default image index to image_idx
    - If the requested image is not found, this image will be returned instead.
  - __set_default_image_id (image_id)__
    - Sets the default image index to the image_idx of image_id
  - __get_default_image ()__
    - Normally used internally.
    - returns (image, width, height) (success) or None (no default image).
  - __\_\_getitem\_\_ (key)__
    - Shortened image access:
      - instance [5] # returns get_image [5]
      - instance ["test"] # returns get_image_id ["test"]
      - returns (image, width, height) (success) or None (failed).
  - __show ()__
    - Used for debugging
    - prints
      - image id, image index
      - image size, image width, image_height
  - __shut_down ()__
    - Closes image_file, if open
    - Initializes attributes

__test_image_extract.py__ Test ImageExtract without a display.

All display calls with parameters are printed

class print output is preceded with an '*'

__cyg_image_extract.py__ Test ImageExtract with a Cheap Yellow Display (240x320)

## Best Practices

- buffer management
  - A byte array is created large enough to contain the largest raw file. This should minimize memory allocation issues. This byte array is shared with all instances of ImageExtract.
  - Multiple instances:
    - Try to instantiate the the image file with the largest raw files first. This will minimize resizing the byte array buffer.
  - Returned raw image:
    - Should be passed to the display before the next image request.
    - Do not save for later use, it will be overwritten.
- Image files with a large number of raw images could cause memory allocation problems. The size of the json parameter text could cause this.

## Files

- images_nnn.bin
  - Input to the image_extract module. 
  Created by build_image_file.py.
  - Format
    - Ascii - 10 digit file offset to raw file(s) parameters.
    - Binary - Raw images from the converted picture files.
    - Ascii - json object containing offset, length, width, height of the embedded raw files.