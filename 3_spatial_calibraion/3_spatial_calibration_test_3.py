import os
import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# === USER INPUTS ===
calib_json = 'spatial_calibration_coeffs.json'
spatial_folder = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\calibrated_spatial'
example_img = None  # Set to None to auto-select the first image in the folder
stripe_spacing_cm = 2

# === LOAD CALIBRATION COEFFICIENTS ===
with open(calib_json) as f:
    coeffs = json.load(f)
pixel_size = coeffs['pixel_size_cm_per_pixel']
offset = coeffs['offset_cm']

print(f"pixel_size_cm_per_pixel: {pixel_size}")
print(f"offset_cm: {offset}")

# === LOAD AN EXAMPLE SPATIALLY CALIBRATED IMAGE ===
if example_img is None:
    # Auto-select the first image in the folder
    for fname in os.listdir(spatial_folder):
        if fname.lower().endswith(('.jpg', '.tif', '.tiff', '.png')):
            example_img = os.path.join(spatial_folder, fname)
            break
    if example_img is None:
        raise FileNotFoundError("No image found in calibrated_spatial folder!")
else:
    example_img = os.path.join(spatial_folder, example_img)

img = np.array(Image.open(example_img).convert('L'))
img_height, img_width = img.shape

# === CHECK MAPPING FOR A FEW PIXEL INDICES ===
pixel_indices = np.array([0, img_width // 2, img_width - 1])
real_world_positions = pixel_size * pixel_indices + offset
print("\nPixel indices:", pixel_indices)
print("Real-world positions (cm):", real_world_positions)

# === PLOT INTENSITY PROFILE WITH EXPECTED STRIPE POSITIONS ===
profile = img.mean(axis=0)
real_world_cm = pixel_size * np.arange(img_width) + offset
cm_min, cm_max = real_world_cm[0], real_world_cm[-1]
expected_stripes = np.arange(cm_min, cm_max + stripe_spacing_cm, stripe_spacing_cm)

plt.figure(figsize=(12, 4))
plt.plot(real_world_cm, profile, label='Intensity profile')
for i, stripe in enumerate(expected_stripes):
    plt.axvline(stripe, color='red', linestyle='--', alpha=0.5,
                label='Expected stripe' if i == 0 else None)
plt.title("Intensity Profile with Expected Stripe Positions")
plt.xlabel("Real-world position (cm)")
plt.ylabel("Mean intensity")
plt.legend()
plt.tight_layout()
plt.show()
