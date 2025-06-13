# Import necessary libraries
import cv2                    # OpenCV for image processing
import numpy as np            # NumPy for numerical operations
import os                     # OS module to handle file paths and directories
from skimage import img_as_float, restoration  # For deblurring
from concurrent.futures import ProcessPoolExecutor, as_completed  # For parallel processing

# ----------- Input and Output Directories -----------

# Path to input folder (change this path as needed)
input_dir = r"C:\Users\badri\OneDrive\Desktop\IIT Tirupati Academic Documents\SigmaFluxDataset"

# Path to save output images (processed)
output_dir = r"C:\Users\badri\OneDrive\Desktop\IIT Tirupati Academic Documents\SigmaFluxDataset\images"

# Set number of threads used by OpenCV to avoid using too many CPU cores unnecessarily
cv2.setNumThreads(4)  # You can change 4 to the number of cores in your system

# ----------- Image Enhancement Functions -----------

# Function to crop the main attendance sheet table from the image
def crop_attendance_sheet(resized_image, debug=False, save_debug_path=None):
    # Convert image to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Blur the image to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use adaptive threshold to handle lighting variation
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    # Morphological operation to close small gaps between lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # Find all contours and select the largest one (assumed to be the table)
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        table_cropped = resized_image[y:y+h, x:x+w]
        return cv2.cvtColor(table_cropped, cv2.COLOR_BGR2RGB)
    else:
        # If no contours found, return the original image
        return cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

# Function to resize image to standard size for consistency
def resize(image):
    return cv2.resize(image, (2266, 1841), interpolation=cv2.INTER_LANCZOS4)

# Function to deblur an image using Richardson-Lucy deconvolution
def deblur_image(image, sigma=1.5, num_iter=25):
    image = img_as_float(image)

    # If the image is not grayscale, convert it
    if not is_grayscale(image):
        image = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
        image = img_as_float(image)

    # Create a Gaussian blur kernel
    kernel_size = int(2 * sigma + 1)
    kernel_size += kernel_size % 2  # Make sure it's an odd number
    x = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    y = np.linspace(-kernel_size // 2, kernel_size // 2, kernel_size)
    x, y = np.meshgrid(x, y)
    kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    kernel /= kernel.sum()

    # Pad the image to avoid edge artifacts during deblurring
    pad_size = kernel_size // 2
    padded_image = np.pad(image, pad_size, mode='reflect')

    # Apply Richardson-Lucy deconvolution
    deblurred = restoration.richardson_lucy(padded_image, kernel, num_iter=num_iter)

    # Crop the image back to original size
    deblurred_image = deblurred[pad_size:-pad_size, pad_size:-pad_size]

    # Convert back to 8-bit image
    return (deblurred_image * 255).astype(np.uint8)

# Function to increase brightness of image
def adjust_brightness(image, filename):
    brightness_value = 50  # Increase brightness by 50
    return cv2.convertScaleAbs(image, alpha=1, beta=brightness_value)

# Function to check whether an image is grayscale
def is_grayscale(image):
    if len(image.shape) == 2:
        return True  # Already grayscale
    if len(image.shape) == 3 and (image[:, :, 0] == image[:, :, 1]).all() and (image[:, :, 1] == image[:, :, 2]).all():
        return True
    return False


os.makedirs(output_dir, exist_ok=True)  # Create folder if it doesn't exist

# ----------- Main Image Processing Function -----------

def process_image(filename):
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, filename)

    # Read the image from file
    image = cv2.imread(input_path, cv2.IMREAD_COLOR)
    if image is None:
        return f"Could not read: {filename}"  # Skip if image is corrupted

    try:
        # Apply all enhancement steps in order
        image = crop_attendance_sheet(image)
        image = resize(image)
        image = deblur_image(image)
        image = adjust_brightness(image, filename)

        # Save the processed image
        cv2.imwrite(output_path, image)
        return f"Processed and saved: {output_path}"
    except Exception as e:
        return f"Error processing {filename}: {e}"

# ----------- Batch Processing Section (Parallel Execution) -----------

if __name__ == "__main__":
    # Collect all image filenames in the input directory
    image_files = [f for f in os.listdir(input_dir)
                   if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    # Use ProcessPoolExecutor to speed up image processing using multiple CPU cores
    with ProcessPoolExecutor() as executor:
        # Submit each image file to be processed in parallel
        futures = [executor.submit(process_image, filename) for filename in image_files]

        # Print results as each image gets processed
        for future in as_completed(futures):
            print(future.result())
