import os
import cv2
import numpy as np
import tifffile as tiff
from glob import glob

# === Configuration ===
input_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\960nm"
output_path = os.path.join(input_folder, "combined_white_regions.tif")
white_threshold = 20  # Optional: can be used if you want to ignore low-intensity noise

# === Find all .tif images ===
image_paths = sorted(glob(os.path.join(input_folder, "*.tiff")))

if not image_paths:
    print("No TIFF images found in folder.")
    exit()

# === Load the first image to get shape ===
first_img = tiff.imread(image_paths[0])
base_image = np.zeros_like(first_img, dtype=np.uint8)  # Start from black

# === Process each image ===
for img_path in image_paths:
    img = tiff.imread(img_path)
    
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Optional: mask out low values
    gray = np.where(gray > white_threshold, gray, 0).astype(np.uint8)
    
    # Update base image with the brightest pixels
    base_image = np.maximum(base_image, gray)

# === Save the final result ===
tiff.imwrite(output_path, base_image)
print(f"Final accumulated white regions saved to: {output_path}")
