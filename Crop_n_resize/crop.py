import cv2
import numpy as np
from google.colab import files
from IPython.display import Image, display

def crop_attendance_sheet(resized_image):
    """
    Crops the attendance sheet from the given resized OpenCV image.

    :param resized_image: Input image (already resized)
    :return: Cropped image containing only the attendance sheet
    """
    # Convert to grayscale
    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to remove noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply edge detection (Canny)
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and get the largest one
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    if contours:
        largest_contour = contours[0]

        # Approximate the contour to a polygon
        epsilon = 0.02 * cv2.arcLength(largest_contour, True)
        approx = cv2.approxPolyDP(largest_contour, epsilon, True)

        if len(approx) == 4:  # If the detected contour has 4 corners, assume it's a rectangle
            pts = np.array([point[0] for point in approx], dtype="float32")

            # Define the output size of the cropped image
            width, height = 1800, 1400  # Adjust according to expected sheet dimensions

            # Destination points for the perspective transform
            dst_pts = np.array([
                [0, 0],
                [width - 1, 0],
                [width - 1, height - 1],
                [0, height - 1]
            ], dtype="float32")

            # Reorder points based on their position
            rect = np.zeros((4, 2), dtype="float32")
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]

            # Compute the perspective transform matrix and apply it
            M = cv2.getPerspectiveTransform(rect, dst_pts)  # Use 'rect' here
            cropped = cv2.warpPerspective(resized_image, M, (width, height))

            return cropped

    return resized_image  # Return original if no valid contour is found