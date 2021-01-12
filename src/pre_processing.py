from commonfunctions import *
from skimage.transform import probabilistic_hough_line, hough_line, rotate, hough_line_peaks
from skimage.feature import corner_harris
import cv2
from staff import *


def deskew(image):
    edges = canny(image, low_threshold=50, high_threshold=150, sigma=2)
    harris = corner_harris(edges)
    tested_angles = np.linspace(-np.pi / 2, np.pi / 2, 360)
    h, theta, d = hough_line(harris, theta=tested_angles)
    out, angles, d = hough_line_peaks(h, theta, d)
    rotation_number = np.average(np.degrees(angles))
    if rotation_number < 45 and rotation_number != 0:
        rotation_number += 90
    return rotation_number


def rotation(img, angle):
    image = rotate(img, angle, resize=True, mode='edge')
    return image


def get_closer(img):
    rows = []
    cols = []
    for x in range(16):
        no = 0
        for col in range(x*img.shape[0]//16, (x+1)*img.shape[0]//16):
            for row in range(img.shape[1]):
                if img[col][row] == 0:
                    no += 1
        if no >= 0.01*img.shape[1]*img.shape[0]//16:
            rows.append(x*img.shape[0]//16)
    for x in range(16):
        no = 0
        for row in range(x*img.shape[1]//16, (x+1)*img.shape[1]//16):
            for col in range(img.shape[0]):
                if img[col][row] == 0:
                    no += 1
        if no >= 0.01*img.shape[0]*img.shape[1]//16:
            cols.append(x*img.shape[1]//16)
    new_img = img[rows[0]:min(img.shape[0], rows[-1]+img.shape[0]//16),
                  cols[0]:min(img.shape[1], cols[-1]+img.shape[1]//16)]
    return new_img


def IsHorizontal(img):
    projected = []
    rows, cols = img.shape
    for i in range(rows):
        proj_sum = 0
        for j in range(cols):
            if img[i][j] == 0:
                proj_sum += 1
        projected.append([1]*proj_sum + [0]*(cols-proj_sum))
        if(proj_sum >= 0.9*cols):
            return True
    return False
