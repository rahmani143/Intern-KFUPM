import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import json

stripe_image_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\output\mean_white_masked.jpg'
stripe_spacing_cm = 2

img = np.array(Image.open(stripe_image_path).convert('L'))
profile = img.mean(axis=0)
edges = np.abs(np.diff(profile))
peaks, _ = find_peaks(edges, distance=10)

print(f"Number of detected peaks: {len(peaks)}")
print("Peak indices:", peaks)

# === MANUALLY SELECT ONLY THE STRIPE REGION ===
# Adjust these numbers based on your actual peak indices!
stripe_region = (peaks >= 400) & (peaks <= 800)
peaks_stripes = peaks[stripe_region]
print(f"Number of stripe peaks: {len(peaks_stripes)}")
print("Stripe peak indices:", peaks_stripes)

physical_positions = np.arange(len(peaks_stripes)) * stripe_spacing_cm

coeffs = np.polyfit(peaks_stripes, physical_positions, 1)
pixel_size = coeffs[0]
offset = coeffs[1]
print(f"Corrected pixel size: {pixel_size:.4f} cm/pixel")
print(f"Corrected offset: {offset:.4f}")

calib_dict = {
    'pixel_size_cm_per_pixel': float(pixel_size),
    'offset_cm': float(offset)
}
with open('spatial_calibration_coeffs.json', 'w') as f:
    json.dump(calib_dict, f)
print("Corrected spatial calibration coefficients saved.")

# Visualize for confirmation
plt.figure(figsize=(12,4))
plt.plot(profile, label='Stripe profile')
plt.plot(peaks_stripes, profile[peaks_stripes], 'rx', label='Selected stripe peaks')
plt.legend()
plt.title("Stripe profile and selected stripe peaks")
plt.xlabel("Pixel index")
plt.ylabel("Mean intensity")
plt.show()
