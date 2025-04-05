import cv2
import numpy as np
import os

# Folder containing images
input_folder = "SigmaFluxDataset"   # Change to your folder path
output_folder = "SigmaFluxDataset New" # Change to your output folder path

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Brightness adjustment value
brightness_value = 50  # Increase (+) or decrease (-)

# Loop through all images in the folder
for filename in os.listdir(input_folder):
    if filename.endswith((".jpg", ".png", ".jpeg")):  # Check for image files
        img_path = os.path.join(input_folder, filename)

        # Read image
        image = cv2.imread(img_path)

        if filename.startswith(('034','035')):
            brightness_value=25
        else:
            brightness_value=50
        # Adjust brightness
        brightened_image = cv2.convertScaleAbs(image, alpha=1, beta=brightness_value)            

        # Save the brightened image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, brightened_image)

        print(f"Processed: {filename}")

print("Brightness adjustment completed for all images!")