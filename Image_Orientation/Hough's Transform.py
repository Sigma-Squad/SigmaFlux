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
    print(angle)
    cv2.imshow('1',image_edges)
    cv2.waitKey(0)
    if (angle < 0):
        angle = angle + 90
    else:
        angle = angle - 90
    return angle


def rotateImage(RGB_image, angle):
    return rotate(RGB_image, angle,True)

def main(im):

    #img = im[len(im)//2 - 50 :len(im)//2 + 50, len(im[0]) // 2 - 50 :len(im[0]) // 2 + 50]
    l = im.tolist()
    req_cor = 0
    for i in range(len(l)//2):
        for j in l[i]:
            if max(j) < 50:
                req_cor = i

    img = im[req_cor - 10:req_cor+10,len(im[0])//8:(len(im[0])//4)]#len(im[0])//20: len(im[0]) - len(im[0])//20]
    cv2.imshow('1',img)
    cv2.waitKey(0)
    b = binarizeImage(img)
    e = findEdges(b)
    im1 = np.array(e)
    im1 = cv2.normalize(im1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    t = findTiltAngle(e)

    i1 = im.tolist()
    im = np.array(i1)
    im = cv2.normalize(im, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    image = rotateImage(im, t)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    image = image - image.min()  # Shift minimum to 0
    image = image / image.max() * 255  # Scale max to 255
    image = np.uint8(image)
    cv2.imwrite("Dataset-Corrected\\001\.jpg",image)