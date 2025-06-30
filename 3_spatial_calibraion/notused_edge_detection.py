# import cv2
# import numpy as np
# import tifffile as tiff
# import matplotlib.pyplot as plt

# # Load TIFF
# img = tiff.imread('C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif')
# if img.ndim > 2:
#     img = img[:, :, 0]

# # Clip and normalize within signal range
# min_val, max_val = 20, 35
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # CLAHE (light contrast enhancement)
# clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
# img_clahe = clahe.apply(img_norm)

# # Blur to denoise
# blurred = cv2.GaussianBlur(img_clahe, (5, 5), 1.2)

# # Lower thresholds because intensity is low
# thresholds = [
#     (5, 15),
#     (10, 20),
#     (15, 30),
#     (20, 40),
#     (25, 50),
#     (30, 60)
# ]

# # Plotting
# n = len(thresholds)
# plt.figure(figsize=(18, 3 * ((n + 2) // 3)))

# for idx, (low, high) in enumerate(thresholds):
#     edges = cv2.Canny(blurred, low, high)
#     plt.subplot((n + 2) // 3, 3, idx + 1)
#     plt.imshow(edges, cmap='gray')
#     plt.title(f'Canny {low}-{high}')
#     plt.axis('off')

# plt.tight_layout()
# plt.show()



# edit 2:

# import cv2
# import numpy as np
# import tifffile as tiff
# import matplotlib.pyplot as plt

# # Load the image
# img = tiff.imread('C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif')
# if img.ndim > 2:
#     img = img[:, :, 0]

# # Auto-stretch contrast using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Show this to debug the image you're working with
# plt.imshow(img_norm, cmap='gray')
# plt.title("Normalized Image (Input to Canny)")
# plt.axis('off')
# plt.show()

# # Apply Gaussian blur
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# # Try several Canny threshold ranges
# thresholds = [
#     (80, 150),
#     (90, 160),
#     (100, 180),
#     (40, 100),
#     (50, 120),
#     (70, 140)
# ]

# n = len(thresholds)
# plt.figure(figsize=(18, 3 * ((n + 2) // 3)))

# for idx, (low, high) in enumerate(thresholds):
#     edges = cv2.Canny(blurred, low, high)
#     plt.subplot((n + 2) // 3, 3, idx + 1)
#     plt.imshow(edges, cmap='gray')
#     plt.title(f'Canny {low}-{high}')
#     plt.axis('off')

# plt.tight_layout()
# plt.show()

# edit 3:

import cv2
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import os

# Load the image
img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'
img = tiff.imread(img_path)
if img.ndim > 2:
    img = img[:, :, 0]

# Auto-stretch contrast using percentiles
min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
img_clipped = np.clip(img, min_val, max_val)
img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Show normalized image for debugging
plt.imshow(img_norm, cmap='gray')
plt.title("Normalized Image (Input to Canny)")
plt.axis('off')
plt.show()

# Apply Gaussian blur
blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# Thresholds to test
thresholds = [
    (80, 150),
    (90, 160),
    (100, 180),
    (40, 100),
    (50, 120),
    (70, 140)
]

# Plotting Canny results
n = len(thresholds)
plt.figure(figsize=(18, 3 * ((n + 2) // 3)))

for idx, (low, high) in enumerate(thresholds):
    edges = cv2.Canny(blurred, low, high)
    plt.subplot((n + 2) // 3, 3, idx + 1)
    plt.imshow(edges, cmap='gray')
    plt.title(f'Canny {low}-{high}')
    plt.axis('off')

plt.tight_layout()
plt.show()

# Save the (100, 180) result
low, high = 90, 170
edges_save = cv2.Canny(blurred, low, high)
output_path = os.path.join(os.path.dirname(img_path), 'my_image_edges_100_180.png')
cv2.imwrite(output_path, edges_save)
print(f"Saved Canny edge image (100, 180) to: {output_path}")
