# -*- coding: utf-8 -*-
"""
    Usage:
        python MusicNoteExtraction.py path
        path: Image path.
    Steps：
        1. Use `cv2.morphologyEx` to remove horizontal and vertical lines, and only notes are left.
        2. Use `cv2.findContours` to find the contours of the notes.
        3. Show the result with the found contours.
"""

import cv2
import numpy as np
import os
import sys


assert len(sys.argv) == 2, 'Please input the image path.'
path = sys.argv[1]
img = cv2.imread(path)

# Gray-scale image.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

"""
Select straight lines.
"""
kernel_f = np.array([[-2, -2, -2], [1, 1, 1], [2, 2, 2]], np.float32)
img_filter = cv2.filter2D(img, -1, kernel_f)

# Binarization gray-scale image with Canny function.
BinGray = cv2.Canny(img_filter, 900, 100, 10)

# Create a black image in the same shape as `img`.
black = np.zeros(img.shape)

# Use Hough Transform to recognize straight lines.
tmp_hough = cv2.HoughLinesP(BinGray, 1, (np.pi / 180), 100, minLineLength=(img.shape[1] * 2 // 3), maxLineGap=100)

hough = tmp_hough[:, 0, :]
# Save y-coordinate of all recognized straight lines.
lines = []

for x1, y1, x2, y2 in hough:
    if abs((y1 - y2) / (x2 - x1)) < 0.01:
        # Select horizontal lines.
        cv2.line(black, (x1, y1), (x2, y2), (0, 255, 0), 1)
        lines.append(y2)

# Sort by y-coordinate in ascendant order.
lines.sort()

"""
Segmentation.
"""
# Recognize the correct lines and find out the width of two adjacent lines.
def RecognizeCorrectLines(lines):
    # Save as (Position, Width): Times.
    tmp = {}

    for l in range(len(lines)):
        x = l + 1
        for k in range(len(lines)):
            for i in reversed(range(len(lines))):
                x -= i
                if x < 0:
                    x += i
                    break
            x -= 1
            tmp_index = (len(lines) - 1) - i

            if int(lines[k]) % int(lines[l]) == 0:
                if int(lines[l]) not in list(x for x, y in tmp.items()):
                    tmp[(lines[tmp_index], lines[l])] = 1
                else:
                    tmp_findindex = list(x[1] for x, y in tmp.items()).index(lines[l])
                    tmp[(tmp[tmp_findindex], lines[l])] += 1

    result = max(tmp[x] for x, y in tmp.items())       
    # return as (pos, width).
    return result

delta = []
for i in range(len(lines) - 1):
    for j in range((i + 1), (len(lines))):
        delta.append(lines[j] - lines[i])

(pos, tmp_width) = RecognizeCorrectLines(delta)

# Calculate the average width of two adjacent lines.
black2 = np.zeros(img.shape)
edge = np.array([])
for i in range(5):
    edge = np.append(edge, (pos + tmp_width * i))

for i in range(len(edge)):
    cv2.line(black2, (1, edge[i]), (black2.shape[1], edge[i]), (0, 255, 0), 1)

cv2.imshow("Line Detection", black2)
cv2.waitKey(0)

# Delete the edges that ratio of length to width is larger the threshold.
def EliminateRatio(MyContours, ratio=2):
    if len(MyContours) == 0:
        print("Error: Contours not found.")

    NewContours = []

    for i in range(len(MyContours)):
        if (MyContours[i]['w'] / MyContours[i]['h']) < ratio and (MyContours[i]['h'] / MyContours[i]['w']) < ratio:
            NewContours.append(MyContours[i])

    return  NewContours

# Delete the edges that the width is not equal to the average of width (Default: larger).
def EliminateWidth(MyContours, ratio = 1.0, big = 1):
    if len(MyContours) == 0:
        raise ZeroDivisionError('Error: Contours not found, so the average may be divided by zero.')

    NewContours = []
    average = 0

    for i in range(len(MyContours)):
        average += MyContours[i]['w']

    average /= len(MyContours)

    if big == 1:
        for i in range(len(MyContours)):
            if MyContours[i]['w'] < (ratio * average):
                NewContours.append(MyContours[i])
    else:
        for i in range(len(MyContours)):
            if MyContours[i]['w'] > (ratio * average):
                NewContours.append(MyContours[i])

    return NewContours

# Delete the edges that the height is not equal to the average of width (Default: larger).
def EliminateHeight(MyContours, ratio=1.0, big=1):
    if len(MyContours) == 0:
        raise ZeroDivisionError('Error: Contours not found, so the average may be divided by zero.')

    NewContours = []
    average = 0

    for i in range(len(MyContours)):
        average += MyContours[i]['h']

    average /= len(MyContours)

    if big == 1:
        for i in range(len(MyContours)):
            if MyContours[i]['h'] < (ratio * average):
                NewContours.append(MyContours[i])
    else:
        for i in range(len(MyContours)):
            if MyContours[i]['h'] > (ratio * average):
                NewContours.append(MyContours[i])

    return NewContours

# Delete the edges that the area is not equal to the average of width (Default: larger).
def EliminateSize(MyContours, ratio=1.0, big=1):
    if len(MyContours) == 0:
        raise ZeroDivisionError('Error: Contours not found, so the average may be divided by zero.')

    NewContours = []
    average = 0

    for i in range(len(MyContours)):
        average += MyContours[i]['h'] * MyContours[i]['w']

    average /= len(MyContours)

    if big == 1:
        for i in range(len(MyContours)):
            if MyContours[i]['h'] * MyContours[i]['w']< ratio * average:
                NewContours.append(MyContours[i])
    else:
        for i in range(len(MyContours)):
            if MyContours[i]['h'] * MyContours[i]['w'] > ratio * average:
                NewContours.append(MyContours[i])

    return NewContours

"""
Delete the five lines and bars of music notes.
"""
dst = cv2.adaptiveThreshold(~gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 15, -2)
# Horizontal lines extraction.
hor = dst.copy()
# Vertical lines extraction.
ver = dst.copy()

# Kernel for hor, use rectangle.
kernel_h = cv2.getStructuringElement(cv2.MORPH_RECT, ((len(hor[0]) // 30 + 1), 1))
# Kernel for ver, use rectangle.
kernel_v = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (len(ver[:, 0]) // 40)))
#kernel_v2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, (len(ver[:, 0]) // 5)))

# For the result, it's Close operation(dilating first, then eroding) because we'll operate `bitwise_not` later.
# Default anchorpoint uses (-1, -1).
hor = cv2.morphologyEx(hor, cv2.MORPH_OPEN, kernel_h)
ver = cv2.morphologyEx(ver, cv2.MORPH_OPEN, kernel_v)
#ver = cv2.dilate(ver, kernel_v2, (-1, -1))

# The background is white and notes are black.
del_lines = cv2.bitwise_not(ver)

"""
Find the heads of music notes.
"""
# Fixed threshold binarization with gray-scale image as input.
ret, binary = cv2.threshold(del_lines, 127, 255, cv2.THRESH_BINARY)
# Find contours.
img2, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Total area.
# Use to calculate the average of area, and delete the rectangles that is too small or too large.
tot_area = 0

MyContours = []
for j in range(len(contours)):
    x, y, w, h = cv2.boundingRect(contours[j])
    MyContours.append({'x': x, 'y': y, 'w': w, 'h': h})

"""
Test.
"""
# MyContours = EliminateRatio(MyContours, 2)
# print(len(MyContours))
# MyContours = EliminateWidth(MyContours, 1, 0)
# print(len(MyContours))
# MyContours = EliminateWidth(MyContours, 1, 1)
# print(len(MyContours))
# MyContours = EliminateHeight(MyContours, 2, 1)
# print(len(MyContours))
# MyContours = EliminateHeight(MyContours, 0.5, 0)
# print(len(MyContours))
# MyContours = EliminateSize(MyContours, 0.9, 0)
# print(len(MyContours))

"""
Draw rectangles.
"""
# Save as (x-coordinate(row), y-coordinate(column)): (width, height)
coordinate = {}

for i in range(0, len(edge) - 1, 2):
    for j in range(len(MyContours)):
        # x: column, y: row, w: width, h: height.
        x, y, w, h = MyContours[j]['x'], MyContours[j]['y'], MyContours[j]['w'], MyContours[j]['h']
        coordinate[(x, y)] = (w, h)

        # Draw rectangle to contours.
        cv2.rectangle(img, (x , (y + (edge[i] - 85 if (edge[i] - 85) > 0 else 0))), (x + w , (y + h + (edge[i] - 85 if (edge[i] - 85) > 0 else 0))), (153, 153, 0), 1)

        # Select the rectangle(Capture).
        new_img = img[(y + 2): (y + h - 2), (x + 2): (x + w - 2)]

        # height = round((bottom[i] + width - (y + h / 2 + (edge[i] - 85 if (edge[i] - 85) > 0 else 0))) / (width / 2))
        # cv2.putText(img, str(height), (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.38, (0, 0, 255), 1)
    # print(bottom[i], img.shape[1], width)

"""
Save images.
"""
# Saving path of captures of notes.
savepath = ".\\music_note_extraction"
if not os.path.isdir(savepath):
    os.makedirs(savepath)

if __name__ == '__main__':
    # Show images.
    cv2.imshow('Deleted lines', del_lines)
    cv2.waitKey(0)
    cv2.imshow('Final', img)
    cv2.waitKey(0)
    cv2.imwrite((savepath + 'del_lines.png'), del_lines)
    cv2.imwrite((savepath + 'Final.png'), img)
    cv2.destroyAllWindows()