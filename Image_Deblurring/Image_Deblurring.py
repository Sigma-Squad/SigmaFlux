import numpy as np
from skimage import img_as_float, restoration
import cv2


def deblur_image(image_path, output_path, sigma=1.5, num_iter=25):
    
    image = img_as_float(image)  # Convert to float64 in range [0,1]
    
    # Create a Gaussian blur kernel ensuring coverage at corners
    kernel_size = int(2 * sigma + 1)
    if kernel_size % 2 == 0:
        kernel_size += 1  # Ensure an odd-sized kernel for symmetry
    
    x = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    y = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    x, y = np.meshgrid(x, y)
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= kernel.sum()
    
    # Pad the image to enhance corner restoration
    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='reflect')
    
    deblurred_padded = restoration.richardson_lucy(padded_image, kernel, num_iter=num_iter)
    
    # Crop back to original size
    deblurred_image = deblurred_padded[pad_size:-pad_size, pad_size:-pad_size]
    
    cv2.imwrite(image, (deblurred_image * 255).astype(np.uint8))
    
    return image