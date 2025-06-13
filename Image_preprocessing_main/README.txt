🖼 Batch Image Enhancement for Attendance Sheets
This project provides an efficient way to process and enhance scanned images of attendance sheets using a
combination of OpenCV and image restoration techniques. It includes table detection, cropping, resizing,
deblurring, and brightness adjustment — all optimized for parallel batch processing.

Features
Auto-Crop Table Region: Detects and crops the largest rectangular table (assumed to be the
attendance sheet).
🔍 Image Deblurring: Uses Richardson-Lucy deconvolution to enhance sharpness.
Brightness Adjustment: Improves visibility under poor lighting.
Adaptive Thresholding: Handles lighting variations across the image.
⚡ Batch Processing: Utilizes multiple CPU cores for fast parallel processing.

Dependencies
Install the required packages via pip:

pip install opencv-python-headless scikit-image numpy

How to Use
Set Input and Output Paths:
Modify these lines in the script:

input_dir = r"Path\to\your\input\folder"
output_dir = r"Path\to\your\output\folder"

What the Script Does
For each image:

1) Converts to grayscale.
2) Applies Gaussian blur and adaptive thresholding.
3) Finds the largest contour (assumed to be the attendance sheet).
4) Crops to this contour area.
5) Resizes to a fixed dimension (2266×1841).
6) Deblurs using a Gaussian kernel and Richardson-Lucy algorithm.
7) Increases brightness.
8) Saves the final result to the output directory.

Performance Tip

The script uses ProcessPoolExecutor to leverage multiple CPU cores. You can tweak the following line to match your hardware:

cv2.setNumThreads(4)  # Set to number of physical CPU cores
