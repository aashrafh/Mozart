from commonfunctions import *
from glob import glob
import os
from PIL import Image


def inv(img_path):
    img = io.imread(img_path)
    img = rgb2gray(img)
    bw = (255*(1 - get_thresholded(img, threshold_otsu(img)))).astype(np.uint8)
    return bw


for dir_n in ['p']:
    imgs = glob(f'train_data/Dataset/{dir_n}/*.png')
    for img in imgs:
        bw = inv(img)
        os.remove(img)
        io.imsave(img, bw)

# for dir_n in glob('train_data/Dataset/*'):
#     for img in glob(f'{dir_n}/*'):
#         name = img.split('.')[0]
#         extension = img.split('.')[1]
#         if extension != 'png' and extension != 'db':
#             im = Image.open(img)
#             im.save(f'{name}.png')

# for dir_n in glob('train_data/Dataset/*'):
#     for img in glob(f'{dir_n}/*'):
#         name = img.split('.')[0]
#         extension = img.split('.')[1]
#         if extension != 'png':
#             os.remove(img)
