import cv2
import numpy as np
from skimage import img_as_float, restoration


# ----------- Image Enhancement Functions -----------

def crop_attendance_sheet(resized_image):                                                           # Crop
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        table_cropped = resized_image[y:y+h, x:x+w]
        return cv2.cvtColor(table_cropped, cv2.COLOR_BGR2RGB)
    else:
        return cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

def resize(image):                                                                                  # Resize
    return cv2.resize(image, (2266, 1841), interpolation=cv2.INTER_LANCZOS4)

def is_grayscale(image):                                                                           
    if len(image.shape) == 2:
        return True
    elif len(image.shape) == 3 and (image[:,:,0]==image[:,:,1]).all() and (image[:,:,1]==image[:,:,2]).all():
        return True
    return False

def deblur_image(image, sigma=1.5, num_iter=25):                                                    # Deblur
    image = img_as_float(image)
    if not is_grayscale(image):
        image = cv2.cvtColor((image*255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
        image = img_as_float(image)

    kernel_size = int(2 * sigma + 1)
    kernel_size += kernel_size % 2  # make odd
    x = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    y = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    x, y = np.meshgrid(x, y)
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= kernel.sum()

    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='reflect')
    deblurred = restoration.richardson_lucy(padded_image, kernel, num_iter=num_iter)
    deblurred_image = deblurred[pad_size:-pad_size, pad_size:-pad_size]

    return (deblurred_image * 255).astype(np.uint8)

def adjust_brightness(image):                                                                       # Lighting
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    avg_brightness = np.mean(gray)
    if avg_brightness < 150:
        return cv2.convertScaleAbs(image, alpha=1, beta=50)
    return image

# ----------- Main function to process single image -----------

def run_parallel_image_processing(image):
    if image is None:
        return None

    try:
        image = crop_attendance_sheet(image)
        image = resize(image)
        image = deblur_image(image)
        image = adjust_brightness(image)
        
        return image
        
    except Exception as e:
        print(f'Exception in pre_processing_pipeline: {e}')
        return None
