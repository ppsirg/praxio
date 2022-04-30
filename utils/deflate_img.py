import os
from subprocess import run
from urllib.parse import quote


extensions = ('.jpg', '.jpeg', '.png')
destination = 'mini'


def assert_folder(destination_folder:str):
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)


def is_img(res:str)-> bool:
    # is_file = os.path.isfile(res)
    is_img = any([res.endswith(a) for a in extensions])
    return is_img


def webp_replace(img:str):
    for xts in extensions:
        if img.endswith(xts):
            return img.replace(xts, '.webp')


def compress_img(destination:str = 'mini', folder_dir:str = '.'):
    assert_folder(destination_folder=destination)
    final = folder_dir.split('/')[-1]
    compress_original_order = ['7z', 'a', '-mmt7', f'original_{final}.zip', f'{folder_dir}/*.jpg']
    run(compress_original_order, check=True)
    resources = list_img(folder_dir=folder_dir)
    print(resources, folder_dir)
    for img in resources:
        order = ['cwebp', '-q', '80', f'{final}/{img}', '-o', os.path.join(destination, webp_replace(img))]
        run(order, check=True)


def list_img(folder_dir:str = '.')->list:
    print(folder_dir, os.listdir(folder_dir))
    return [quote(a.strip()) for a in os.listdir(folder_dir) if is_img(a.strip())]