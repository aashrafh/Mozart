from commonfunctions import *
from skimage.measure import label, regionprops
from skimage.color import label2rgb
from box import Box


def get_connected_components(img_without_staff, img_with_staff):
    components = []
    boundary = []
    # thresh = threshold_otsu(img_without_staff)
    # bw = closing(img_without_staff <= thresh, square(3))
    bw = 1-img_without_staff
    label_img = label(bw)
    img_label_overlay = label2rgb(
        label_img, image=img_without_staff, bg_label=0)
    for region in regionprops(label_img):
        if region.area >= 100:
            boundary.append(region.bbox)

    boundary = sorted(boundary, key=lambda b: b[1])

    comp_with_staff = []
    for bbox in boundary:
        minr, minc, maxr, maxc = bbox
        components.append(img_without_staff[minr:maxr, minc:maxc])
        comp_with_staff.append(img_with_staff[minr:maxr, minc:maxc])
    return components, comp_with_staff, boundary
