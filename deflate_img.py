import os
import htmlmin
from jinja2 import Template
from subprocess import call

extensions = ('.jpg', '.jpeg', '.png')
destination = 'miau'

def assert_folder():
    if not os.path.exists(destination):
        os.mkdir(destination)

def is_img(res:str)-> bool:
    is_file = os.path.isfile(res)
    is_img = any([res.endswith(a) for a in extensions])
    return is_img and is_file

def webp_replace(img:str):
    for xts in extensions:
        if img.endswith(xts):
            return img.replace(xts, '.webp')

def compress_img():
    resources = list_img()
    for img in resources:
        order = ['cwebp', '-q', '80', img, '-o', os.path.join(destination, webp_replace(img))]
        call(order)


def list_img()->list:
    return [a for a in os.listdir('.') if is_img(a)]



if __name__ == '__main__':
    assert_folder()
    compress_img()
