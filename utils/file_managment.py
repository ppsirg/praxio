import os
from urllib.parse import quote

img_extensions = ('.jpg', '.jpeg', '.png')


def is_img(target:str, res:str)-> bool:
    is_file = os.path.isfile(os.path.join(target, res))
    is_img = any([res.endswith(a) for a in img_extensions])
    return is_img and is_file


def assert_destination(foldername:str)->str:
    if not os.path.exists(foldername):
        os.mkdir(foldername)
    return foldername


def list_img(target:str)->list:
    return [a.strip() for a in os.listdir(target) if is_img(target, a.strip())]


def list_img_resources(target:str)->list:
    return [quote(a) for a in list_img(target)]