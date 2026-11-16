#
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

from PIL import Image

import argparse
import json
from pathlib import Path
import struct

def img_to_rgb565 (img, big_endian=True):
    pixels = img.get_flattened_data ()
    length = img.width * img.height
    img_data = bytearray (length * 2)

    # '>H' for big-endian, '<H' for little-endian
    endian_format = ">H" if big_endian else "<H"

    data_idx = 0
    for r, g, b in pixels:
        rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
        data_pixel = struct.pack (endian_format, rgb565)
        img_data [data_idx] = data_pixel [0]
        data_idx += 1
        img_data [data_idx] = data_pixel [1]
        data_idx += 1
    return img_data

def write_file_offset (f, offset=0) :
    current_offset = f.tell ()
    f.seek (0)
    f.write (f"{offset:010d}".encode ())
    if current_offset > 10 :
        f.seek (current_offset)
    
def parse_arguments () :
    parser = argparse.ArgumentParser(description="merge images files to raw file.")
    # 
    parser.add_argument ("--output",
                        nargs="?",
                        default="image_extract.bin",
                        help="Optional output file")
    parser.add_argument ("-t",
                        "--thumbnail",
                        nargs=2,
                        type=int,
                        help="thumbnail w, h")
    parser.add_argument('-l', '--littleendian',
                        action='store_true',
                        help='Enable little endian')
    parser.add_argument ("files",
                        nargs="+",
                        help="One or more input files")
    
    return parser.parse_args()

args = parse_arguments ()

image_config = {
    "count" : 0 ,
    "thumbnail" : args.thumbnail ,
    "images" : [
        ] ,
    "image_ids" : {
        }
    }

fout = open (args.output, "wb")
write_file_offset (fout, 0)             # reserve offset field

for file_name in args.files :
    #print (file_name)
    file_path = Path(file_name)

    # Open the image and ensure it is in RGB mode (strips alpha channel if PNG)
    img = Image.open(file_name).convert("RGB")

    if args.thumbnail is not None :
        img.thumbnail ((args.thumbnail[0], args.thumbnail[1]))
    
    raw_bytes = img_to_rgb565 (img, not args.littleendian)

    img.close ()
    image_config ["images"].append ({
        "pos" : fout.tell () ,
        "l" : len (raw_bytes) ,
        "w" : img.width ,
        "h" : img.height
        })
    image_config ["image_ids"][file_path.stem] = image_config ["count"]
    image_config ["count"] += 1

    fout.write(raw_bytes)

write_file_offset (fout, fout.tell ())
#print (json.dumps (image_config).encode())
fout.write (json.dumps (image_config).encode())
fout.close ()

