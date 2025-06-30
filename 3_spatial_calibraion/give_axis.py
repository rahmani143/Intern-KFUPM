import cv2
import matplotlib.pyplot as plt
import numpy as np

# === Load image ===
img = cv2.imread(r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\blue_vertical_lines.png")
if img is None:
    raise FileNotFoundError("Image not found. Check your path.")

# === Convert BGR (OpenCV) to RGB (matplotlib) ===
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# === Flip image vertically to match bottom-left origin ===
img_rgb = np.flipud(img_rgb)

# === Calibration parameters ===
mm_per_pixel = 0.0463  # adjust based on your calibration
distance_mm = 4        # physical spacing between lines in mm
pixels_per_4mm = int(distance_mm / mm_per_pixel)

# === Prepare X-axis ticks in pixels and mm labels ===
img_width = img.shape[1]
num_ticks = img_width // pixels_per_4mm + 1

xticks = [i * pixels_per_4mm for i in range(num_ticks)]
xlabels = [str(i * distance_mm) for i in range(num_ticks)]

# === Plotting ===
plt.figure(figsize=(12, 6))
plt.imshow(img_rgb)
plt.xlabel("Distance (mm)")
plt.ylabel("Pixels")

# Set X-axis ticks (in mm)
plt.xticks(xticks, xlabels)

# Invert Y-axis to place origin at bottom-left
plt.gca().invert_yaxis()

# Add grid for visual aid
plt.title("Image with X-axis labeled in mm (4 mm between ticks)")
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()
