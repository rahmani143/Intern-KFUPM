import os
import numpy as np
from PIL import Image
import cv2

# ---- Configuration ----
# Set paths
image_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\best_image_20250618_141920.tiff'
output_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\my_image_calibrated.tif'

mean_black_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\output\mean_black.tif'
mean_white_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\output\mean_white_masked.jpg"

# Create output directory if it doesn't exist
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# ---- Load Calibration References ----
mean_black = np.array(Image.open(mean_black_path).convert('L')).astype(np.float32)
mean_white = np.array(Image.open(mean_white_path).convert('L')).astype(np.float32)

# ---- Load and Process Target Image ----
with Image.open(image_path) as im:
    im = im.convert('L')  # Convert to grayscale
    imarr = np.array(im, dtype=np.float32)

    # Resize calibration images if dimensions don't match
    if mean_black.shape != imarr.shape:
        mean_black = cv2.resize(mean_black, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)
        mean_white = cv2.resize(mean_white, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)

    # ---- Radiometric Calibration ----
    denominator = mean_white - mean_black
    min_denominator = 5.0  # Prevent instability
    valid_denominator_mask = denominator > min_denominator

    # Prevent divide-by-zero in invalid areas
    denominator[~valid_denominator_mask] = 1

    # Identify raw black background (avoid boosting noise)
    raw_black_mask = imarr < 5  # Adjust if needed

    # Radiometric formula
    calibrated = (imarr - mean_black) / denominator
    calibrated = np.clip(calibrated, 0, 1)

    # Clean up: apply both masks
    calibrated[~valid_denominator_mask | raw_black_mask] = 0  # Keep noisy borders black

    # ---- Save as 8-bit TIFF image ----
    calibrated_img = (calibrated * 255).astype(np.uint8)
    Image.fromarray(calibrated_img).save(output_path, format='TIFF')
    print(f"✅ Calibrated image saved at: {output_path}")
