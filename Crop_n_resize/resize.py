import cv2

#if the input is an image
def resize(image):
    return cv2.resize(image,(2266,1841),interpolation=cv2.INTER_LANCZOS4)

#if the imput is string containing the image location
def resize_image_string(image_string):
    return cv2(cv2.imread(image_string),(2266,1841),interpolation=cv2.INTER_LANCZOS4) #this could be considered
