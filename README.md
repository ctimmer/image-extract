# image-extract
Merge / Extract raw images for micropython displays

## Applications

__build_image_file.py__ Builds extract file from 1 or more input image files.

Requires Pillow module which at this time has to be installed in a python virtual environment.

__build_images.bsh__ Example usage of build_image_file.py. Input images are in ./test_images/*.

- After running 2 files are created:
  - _images_100.bin_ Raw images that will fit into an 100 by 100 pixel area.
  - _images_150.bin_ Raw images that will fit into an 150 by 150 pixel area.

__image_extract.py__ ImageExtract module. Extracts raw images from extract file for displaying on various microprocessor displays.