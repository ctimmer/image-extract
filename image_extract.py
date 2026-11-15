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
import gc
import json

class ImageExtract :
    buffer = None
    buffer_view = None
    def __init__ (self ,
                  image_file_name : str = None
                  ) :
        #print ("ImageExtract : __init__")
        
        self.image_file = None
        self.image_config = None
        self.image_count = 0
        self.initialize_image_file (image_file_name)
        gc.collect ()

    def allocate_buffer (self,
                         buffer_size) :
        if ImageExtract.buffer is not None :
            if buffer_size <= len (ImageExtract.buffer) :
                return buffer_size
            else :
                ImageExtract.buffer_view = None
                ImageExtract.buffer = None
                gc.collect ()
        ImageExtract.buffer = bytearray (buffer_size)
        ImageExtract.buffer_view = memoryview (ImageExtract.buffer)

    def initialize_image_file (self ,
                                image_file_name : str
                                ) :
        #print ("initialize_image_file")
        if image_file_name is None :
            return None
        l_max = 0
        self.image_file = None
        self.image_config = None
        self.image_count = 0
        try :
            self.image_file = open (image_file_name, "rb")
            offset = self.image_file.read (10)
            param_offset = int (offset)
            self.image_file.seek (param_offset)
            params = self.image_file.read ().decode ()
            self.image_config = json.loads (params)
            self.image_count = self.image_config ["count"]
        except Exception as e :
            print ("load_image_file:", e)
            return None
        for _, image_data in enumerate (self.image_config ["images"]) :
            if image_data ["l"] > l_max :
                l_max = image_data ["l"]
        self.image_config ["l_max"] = l_max
        self.allocate_buffer (l_max)
        return self.image_count

    def rename_id (self ,
                    old_id : str ,
                    new_id : str ,
                    delete_old_id : bool = True) :
        if old_id not in self.image_config ["image_ids"] :
            print ("missing:", old_id)
            return None
        self.image_config ["image_ids"][new_id] \
            = self.image_config ["image_ids"][old_id]
        if delete_old_id :
            del self.image_config ["image_ids"][old_id]
        return self.image_config ["image_ids"][new_id] # return index
    def rename_index (self ,
                        image_idx : int ,
                        new_name : str) :
        if image_idx < 0 \
        or image_idx >= self.image_count :
            return None
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
        img_length = image_data ["l"]
        self.image_file.seek (image_data ["pos"])
        read_length = self.image_file.readinto (ImageExtract.buffer_view [:img_length])
        return (ImageExtract.buffer_view [:image_data ["l"]],
                image_data ["w"],
                image_data ["h"])
    
    def get_image_id (self,
                        image_id : str) :
        if image_id not in self.image_config ["image_ids"] :
            return None
        return self.get_image (self.image_config ["image_ids"][image_id])

    def show (self) :
        for _, (img_id, image_idx) in enumerate (self.image_config ["image_ids"].items ()) :
            print (img_id, image_idx)
            image_data = self.get_image_data (image_idx)
            length = image_data ["l"]
            width = image_data ["w"]
            height = image_data ["h"]
            print (f"  {length} {width} {height}")
            
    def shut_down (self) :
        if self.image_file is not None :
            self.image_file.close ()

# end ImageExtract

