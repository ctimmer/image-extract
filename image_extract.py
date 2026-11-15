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
#import time
#import random
import json

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

    def rename_id (self ,
                    old_id : str ,
                    new_id : str ,
                    delete_old_id = True) :
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
        self.image_file.seek (image_data ["pos"])
        return (self.image_file.read (image_data ["l"]) ,
                image_data ["w"] ,
                image_data ["h"])
    
    def get_image_id (self,
                        image_id : str) :
        if image_id not in self.image_config ["image_ids"] :
            return None
        return self.get_image (self.image_config ["image_ids"][image_id])

    def shut_down (self) :
        if self.image_file is not None :
            self.image_file.close ()

# end ImageExtract

