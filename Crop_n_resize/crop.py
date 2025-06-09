import cv2
import numpy as np

def crop_attendance_sheet(resized_image, debug=False, save_debug_path=None):
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Step 1: Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 2: Apply adaptive thresholding to handle varying lighting
    adaptive_thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 15, 10
    )

    # Step 3: Use morphological operations to close small gaps in lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    morphed = cv2.morphologyEx(adaptive_thresh, cv2.MORPH_CLOSE, kernel)

    # Step 4: Find contours and select the largest one as the table boundary
    contours, _ = cv2.findContours(morphed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        table_cropped = resized_image[y:y+h, x:x+w]
        return cv2.cvtColor(table_cropped, cv2.COLOR_BGR2RGB)
    else:
        return cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)  # fallback


