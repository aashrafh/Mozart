from commonfunctions import *
from skimage.transform import probabilistic_hough_line,hough_line, rotate

def deskew(image):
    thresh = threshold_otsu(image)
    normalize = image > thresh
    blur = gaussian(image, 3)
    edges = canny(blur)
    out, angles, d = hough_line(edges)
    x = np.where(out == np.max(out))
    rotation_number = np.average(np.degrees(angles[x[1]]))
    #hough_lines = probabilistic_hough_line(edges)
    #slopes = [(y2 - y1)/(x2 - x1) if (x2-x1) else 0 for (x1,y1), (x2, y2) in hough_lines]
    #rad_angles = [np.arctan(x) for x in slopes]
    #deg_angles = [np.degrees(x) for x in rad_angles]
    #histo = np.histogram(deg_angles, bins=180)
    #rotation_number = histo[1][np.argmax(histo[0])]   
    if rotation_number < 45 and rotation_number != 0:   
        rotation_number+=90
    return rotation_number
def rotation(img , angle):
    img = rotate(img , angle,resize = True)
    return img
def binary(img, threshold):
    gray = rgb2gray(img)*255
    bin_img = 255*(gray > threshold)
    return bin_img    