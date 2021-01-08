from commonfunctions import *
from glob import glob
import os
from PIL import Image


def inv(img_path, save_path):
    img = io.imread(img_path)
    img = rgb2gray(img)
    bw = (255*(1 - get_thresholded(img, threshold_otsu(img)))).astype(np.uint8)
    io.imsave(save_path, bw)


dir_name = 'Eight'
imgs_path = glob(f'train_data/data/natural/nat/*.bmp')
imgs_path = sorted(imgs_path)
res_path = f'train_data/data/#/sh'
imgs_names = [img.split('/')[3].split('.')[0] for img in imgs_path]

for i, img in enumerate(imgs_path):
    im = Image.open(img)
    im.save(f'train_data/data/cross/{imgs_names[i]}.png')
    os.remove(img)

os.mkdir(res_path)
for i, img in enumerate(imgs_path):
    inv(img, res_path+'/'+imgs_names[i])


dirs = [path for path in glob(f'train_data/data/*')]
dir_names = [path.split('/')[2] for path in dirs]

for i, directory in enumerate(dirs):
    imgs = glob(f'{directory}/*.png')
    for j, img in enumerate(imgs):
        os.rename(img, f'{directory}/{dir_names[i]}_{j}.png')
