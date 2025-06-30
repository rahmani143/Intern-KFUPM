# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\best_image_20250617_133628.tiff"
# image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
# if image is None:
#     raise FileNotFoundError(f"Could not load image. Check the path:\n{image_path}")

# positions = np.column_stack(np.where(image != 0))
# rows = positions[:, 0]
# cols = positions[:, 1]
# height = image.shape[0]
# y_flipped = height - 1 - rows

# margin = 10  # pixels of padding around points

# # Calculate limits with margin, ensuring they don't go below 0 or above image size
# x_min = max(cols.min() - margin, 0)
# x_max = min(cols.max() + margin, image.shape[1])
# y_min = max(y_flipped.min() - margin, 0)
# y_max = min(y_flipped.max() + margin, height)

# plt.figure(figsize=(8, 6))
# plt.scatter(cols, y_flipped, s=1, color='blue')
# plt.xlabel('X (column)')
# plt.ylabel('Y (row, flipped)')
# plt.title('Positions of Non-zero Pixels with Margin')
# plt.xlim(x_min, x_max)
# plt.ylim(y_min, y_max)
# plt.show()


# edit 1:

import cv2
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # needed for 3D plotting

# Load image (grayscale or single channel)
image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\my_image_calibrated.tif"
image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
if image is None:
    raise FileNotFoundError(f"Could not load image. Check the path:\n{image_path}")

# Get positions of all pixels (including zero intensities if you want full surface)
rows, cols = np.indices(image.shape)

# Flatten arrays for scatter plotting
x = cols.flatten()  # X axis = column index
y = rows.flatten()  # Y axis = row index
z = image.flatten()  # Z axis = pixel intensity

# Optionally filter out zero intensity pixels to reduce points and focus on meaningful data
nonzero_mask = z > 0
x = x[nonzero_mask]
y = y[nonzero_mask]
z = z[nonzero_mask]

# Plot
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot
scat = ax.scatter(x, y, z, c=z, cmap='viridis', marker='.', s=5)

ax.set_xlabel('X (column)')
ax.set_ylabel('Y (row)')
ax.set_zlabel('Intensity')
ax.set_title('3D Pixel Intensity Plot')

fig.colorbar(scat, ax=ax, label='Intensity')

plt.show()
