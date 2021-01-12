from rle import *
from commonfunctions import *
from staff import calculate_thickness_spacing, remove_staff_lines
from staff import*


def get_staff_row_position2(img):
    found = 0
    row_position = -1
    for i in range(img.shape[0]-1, 0, -1):
        for j in range(img.shape[1]-1, img.shape[1]//2, -1):
            if(img[i][j] == 0):
                row_position = i
                found = 1
                break
        if found == 1:
            break
    return row_position


def camera_segment(img):
    imghelper = []
    rle, vals = hv_rle(img)
    most_common = get_most_common(rle)
    thickness, spacing = calculate_thickness_spacing(rle, most_common)
    no_staff_img = remove_staff_lines(rle, vals, thickness, img.shape)
    no_staff_img = median(no_staff_img)
    no_staff_img = binary_dilation(
        no_staff_img, np.ones((thickness+2, thickness+2)))
    no_staff_img = binary_erosion(
        no_staff_img, np.ones((thickness+2, thickness+2)))
    staff_lines = otsu(img - no_staff_img)
    staff_lines = binary_erosion(
        staff_lines, np.ones((thickness+2, thickness+2)))
    staff_lines = median(staff_lines)
    staff_lines_row_position = get_staff_row_position(staff_lines)
    staff_row_positions = get_rows(
        staff_lines_row_position-most_common, most_common, thickness, spacing)
    staff_row_positions = [np.average(x) for x in staff_row_positions]
    isa1 = img[int(staff_row_positions[0]):int(
        staff_row_positions[-1]+2*most_common), :]
    imghelper.append(isa1)
    lastIsa2Start = get_staff_row_position2(staff_lines)
    isaLast = img[int(lastIsa2Start-9*most_common):int(lastIsa2Start), :]
    area = int(lastIsa2Start)-int(lastIsa2Start-9*most_common)
    start = int(staff_row_positions[-1]+2*most_common)
    last = int(lastIsa2Start-9*most_common)
    ih = last-start
    if ih > 2*area:
        while(ih > 2*area):
            imgmid = img[int(start):int(start+area), :]
            start = start+area
            ih = last-start
            imghelper.append(imgmid)
    else:
        imgmid = img[int(start):int(last), :]
        imghelper.append(imgmid)
    imghelper.append(isaLast)
    imghelper[1:len(imghelper)-2].reverse()
    return imghelper, most_common
