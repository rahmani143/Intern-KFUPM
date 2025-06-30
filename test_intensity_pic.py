import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load image as 8-bit
image = cv2.imread('C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif', cv2.IMREAD_UNCHANGED)

# Check dtype
print(f"Loaded image dtype: {image.dtype}")  # Should show uint8

# Flatten and plot histogram
pixels = image.flatten()
plt.figure(figsize=(10, 5))
plt.hist(pixels, bins=256, range=(0, 255), color='steelblue', log=True)
plt.title("Histogram of 8-bit Pixel Intensities")
plt.xlabel("Pixel Intensity (0 to 255)")
plt.ylabel("Frequency (log scale)")
plt.grid(True)
plt.tight_layout()
plt.show()
