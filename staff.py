from rle import *
from commonfunctions import *
from collections import Counter


def calculate_thickness_spacing(rle, most_common):
    bw_patterns = [most_common_bw_pattern(col, most_common) for col in rle]
    bw_patterns = [x for x in bw_patterns if x]  # Filter empty patterns

    flattened = []
    for col in bw_patterns:
        flattened += col

    pair, count = Counter(flattened).most_common()[0]

    line_thickness = min(pair)
    line_spacing = max(pair)

    return line_thickness, line_spacing


def whitene(rle, vals, max_height):
    rlv = []
    for length, value in zip(rle, vals):
        if value == 0 and length < 1.1*max_height:
            value = 1
        rlv.append((length, value))

    n_rle, n_vals = [], []
    count = 0
    for length, value in rlv:
        if value == 1:
            count = count + length
        else:
            if count > 0:
                n_rle.append(count)
                n_vals.append(1)

            count = 0
            n_rle.append(length)
            n_vals.append(0)
    if count > 0:
        n_rle.append(count)
        n_vals.append(1)

    return n_rle, n_vals


def remove_staff_lines(rle, vals, thickness, shape):
    n_rle, n_vals = [], []
    for i in range(len(rle)):
        rl, val = whitene(rle[i], vals[i], thickness)
        n_rle.append(rl)
        n_vals.append(val)

    return hv_decode(n_rle, n_vals, shape)


def get_staff_row_position(img):
    found = 0
    row_position = -1
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if(img[i][j] == 0):
                row_position = i
                found = 1
                break
        if found == 1:
            break
    print(row_position)
    return row_position


def get_rows(start, most_common, thickness, spacing):
    # start = start-most_common
    rows = []
    for k in range(7):
        row = []
        for i in range(thickness):
            row.append(start)
            start += 1

        start += (spacing)
        rows.append(row)
    # row = [start]
    # i = 1
    # for x in range(7*thickness):
    #     if i < thickness:
    #         start += 1
    #         i += 1
    #         row.append(start)
    #     else:
    #         rows.append(row)
    #         row = []
    #         start += spacing
    #         row.append(start)
    #         i = 1
    return rows


def horizontal_projection(img):
    projected = []
    rows, cols = img.shape
    for i in range(rows):
        proj_sum = 0
        for j in range(cols):
            proj_sum += img[i][j] == 1
        projected.append([1]*proj_sum + [0]*(cols-proj_sum))
        if(proj_sum <= 0.1*cols):
            return i
    return 0


def coordinator(bin_img):
    start = horizontal_projection(bin_img)
    rle, vals = hv_rle(bin_img)
    most_common = get_most_common(rle)
    thickness, spacing = calculate_thickness_spacing(rle, most_common)
    no_staff_img = remove_staff_lines(rle, vals, thickness, bin_img.shape)
    staff_lines = otsu(bin_img - no_staff_img)
    show_images([staff_lines])
    staff_lines_row_position = get_staff_row_position(staff_lines)
    staff_row_positions = get_rows(
        start-most_common, most_common, thickness, spacing)
    staff_row_positions = [np.average(x) for x in staff_row_positions]
    return spacing, staff_row_positions
