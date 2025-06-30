import os
import numpy as np
from PIL import Image
import glob
import cv2
import json

# Set your paths
scene_folder = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images'
output_folder = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\calibrated radiometric'
mean_black_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\output\mean_black.tif'
mean_white_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\output\mean_white_masked.jpg"

os.makedirs(output_folder, exist_ok=True)

# Load mean black and mean white images as arrays
mean_black = np.array(Image.open(mean_black_path).convert('L')).astype(np.float32)
mean_white = np.array(Image.open(mean_white_path).convert('L')).astype(np.float32)

# Get all image files in the scene folder (adjust extensions as needed)
scene_files = glob.glob(os.path.join(scene_folder, '*.jpg'))

for filepath in scene_files:
    with Image.open(filepath) as im:
        im = im.convert('L')  # Ensure grayscale
        imarr = np.array(im, dtype=np.float32)
        # Resize mean images if needed
        if mean_black.shape != imarr.shape:
            import cv2

            # Replace this block:
            # mean_black_resized = np.resize(mean_black, imarr.shape)

            # With:
            mean_black_resized = cv2.resize(mean_black, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)
            mean_white_resized = cv2.resize(mean_white, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)
        else:
            mean_black_resized = mean_black
            mean_white_resized = mean_white

        # Radiometric calibration
        denominator = mean_white_resized - mean_black_resized
        denominator[denominator == 0] = 1  # Prevent division by zero
        calibrated = (imarr - mean_black_resized) / denominator
        calibrated = np.clip(calibrated, 0, 1)

        # Save as 8-bit image for visualization
        calibrated_img = (calibrated * 255).astype(np.uint8)
        out_path = os.path.join(output_folder, os.path.basename(filepath))
        Image.fromarray(calibrated_img).save(out_path)
        print(f"Calibrated image saved: {out_path}")
