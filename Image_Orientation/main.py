import numpy as np
from skimage.color import rgb2gray
from skimage.transform import rotate
from skimage.transform import (hough_line, hough_line_peaks)
from scipy.stats import mode
from skimage.filters import threshold_otsu, sobel
import cv2

def binarizeImage(RGB_image):
    image = rgb2gray(RGB_image)
    threshold = threshold_otsu(image)
    bina_image = image < threshold

    return bina_image


def findEdges(bina_image):
    image_edges = sobel(bina_image)
    return image_edges


def findTiltAngle(image_edges):
    h, theta, d = hough_line(image_edges)
    accum, angles, dists = hough_line_peaks(h, theta, d)
    angle = np.rad2deg(mode(angles)[0])

    if (angle < 0):

        angle = angle + 90

    else:

        angle = angle - 90

    return angle


def rotateImage(RGB_image, angle):
    return rotate(RGB_image, angle)

for k in range(1,61):
    if k<10:
        im = cv2.imread(f"SigmaFluxDataset\\00{k}.jpg")
    else:
        im = cv2.imread(f"SigmaFluxDataset\\0{k}.jpg")
    l = im.tolist()
    req_cor = 0
    for i in range(len(l)):
        for j in l[i]:
            if max(j) < 50:
                req_cor = i
    img = im[req_cor - 10:req_cor + 10, len(im[0]) // 20: len(im[0]) - len(im[0]) // 20]

    b = binarizeImage(img)
    e = findEdges(b)
    t = findTiltAngle(e)

    i1 = im.tolist()

    if len(i1)>len(i1[0]):
        for j in range(len(i1)):
            for i in range(len(i1) - len(i1[j])):
                i1[j].append([0, 0, 0])

    else:
        L=[]
        for i in range(len(i1[0])):
            L.append([0,0,0])

        for i in range(len(i1[0]) - len(i1)):
            i1.append(L)

    im = np.array(i1)
    im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    image = rotateImage(im, t)
    cv2.waitKey(0)
    image = image - image.min()  # Shift minimum to 0
    image = image / image.max() * 255  # Scale max to 255
    image = np.uint8(image)
    cv2.imwrite(f"Dataset-Corrected\\{k}.jpg",image)
