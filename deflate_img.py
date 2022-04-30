import os
from utils.deflate_img import compress_img

source_dir = 'img1'
destiny_dir = 'mn'

if __name__ == '__main__':
    compress_img(destination=os.path.abspath(destiny_dir), folder_dir=os.path.abspath(source_dir))
