# import os
# import numpy as np
# import tifffile as tiff
# import matplotlib.pyplot as plt

# # Folder containing your images
# folder_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\radiometric_white"

# # Collect all image files (assuming all images are .jpg here, change if needed)
# image_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.jpg')])

# print(f"Found image files: {image_files}")

# # Read all images and stack into a hyperspectral cube
# hsi_lines = []
# for filename in image_files:
#     filepath = os.path.join(folder_path, filename)
#     # Since they are JPG images, use tifffile.imread might fail, so use matplotlib or PIL
#     # Using matplotlib imread here:
#     img = plt.imread(filepath)
#     # Convert to grayscale or single band if needed
#     if img.ndim == 3:
#         # If RGB, convert to grayscale by averaging or select channel (e.g. R channel)
#         img_gray = np.mean(img, axis=2)
#     else:
#         img_gray = img
#     hsi_lines.append(img_gray)

# # Stack into numpy array (num_images, height, width)
# hsi_cube = np.stack(hsi_lines, axis=0)

# print(f"HSI Cube shape (num_images, height, width): {hsi_cube.shape}")

# # Transpose cube to (height, width, bands)
# hsi_cube = np.transpose(hsi_cube, (1, 2, 0))
# print(f"HSI Cube shape (height, width, bands): {hsi_cube.shape}")

# # Example: Save dummy wavelengths (assuming wavelength range 400-700 nm for illustration)
# num_bands = hsi_cube.shape[2]
# wavelengths = np.linspace(400, 700, num_bands)
# wavelength_file = os.path.join(folder_path, "wavelengths.txt")
# np.savetxt(wavelength_file, wavelengths, fmt="%.2f")
# print(f"✅ Estimated wavelengths saved to: {wavelength_file}")

# # RGB band indices (example indices, adjust according to your setup)
# rgb_indices = [83, 50, 17]

# def normalize_band(band):
#     # Normalize to 0-255 uint8, fixed for numpy 2.0+
#     return ((band - band.min()) / (np.ptp(band) + 1e-8) * 255).astype(np.uint8)

# try:
#     r = normalize_band(hsi_cube[:, :, rgb_indices[0]])
#     g = normalize_band(hsi_cube[:, :, rgb_indices[1]])
#     b = normalize_band(hsi_cube[:, :, rgb_indices[2]])
# except IndexError:
#     print(f"Error: RGB indices {rgb_indices} out of range for cube bands {num_bands}")
#     raise

# # Stack RGB channels into image
# rgb_image = np.stack([r, g, b], axis=2)

# # Show the RGB image
# plt.imshow(rgb_image)
# plt.title("Synthetic RGB Image from HSI Cube")
# plt.axis('off')
# plt.show()









# edit 1:










# import numpy as np
# import cv2
# import glob
# import os

# # Folder with pushbroom images
# image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images"

# # List files sorted by filename (assumes 'Acquisition-001.jpg', etc.)
# image_files = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))

# print(f"Found {len(image_files)} images")

# # Read images as grayscale, shape: (spectral_bands, spatial_pixels)
# images = []
# for f in image_files:
#     img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         print(f"Failed to read {f}")
#         continue
#     images.append(img)

# # Stack images along pushbroom scan axis (spatial Y)
# cube = np.stack(images, axis=1)  
# # shape: (spectral_bands, pushbroom_steps, spatial_pixels)

# print(f"Cube shape before transpose: {cube.shape}")

# # Rearrange axes to (spatial_Y, spatial_X, spectral_bands)
# # spatial_Y = pushbroom step axis (image index)
# # spatial_X = spatial pixels along slit (image width)
# # spectral_bands = spectral bands along height
# cube = np.transpose(cube, (1, 2, 0))

# print(f"Final cube shape (spatial_Y, spatial_X, spectral_bands): {cube.shape}")









# edit 2:








import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

# === Configuration ===
image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images"
output_path = os.path.join(image_folder, "hsi_cube.npy")  # Save as numpy array

# === Get all .jpg grayscale images in sorted order ===
image_files = sorted(glob.glob(os.path.join(image_folder, "*.jpg")))
print(f"Found {len(image_files)} images")

# === Read images ===
cube_bands = []
for file in image_files:
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"⚠️ Failed to read {file}")
        continue
    cube_bands.append(img)

# === Stack into a cube: shape (2048, 2048, 200) ===
hsi_cube = np.stack(cube_bands, axis=-1)  # Stack along 3rd axis (bands)

print(f"✅ Final HSI Cube shape: {hsi_cube.shape}")  # Expect (2048, 2048, 200)

# === Save cube as .npy ===
np.save(output_path, hsi_cube)
print(f"✅ Cube saved to: {output_path}")

# === Show an example RGB approximation ===
# Pick three representative bands for R, G, B
if hsi_cube.shape[2] >= 3:
    rgb_img = cv2.merge([
        cv2.normalize(hsi_cube[:, :, 150], None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
        cv2.normalize(hsi_cube[:, :, 100], None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
        cv2.normalize(hsi_cube[:, :, 50], None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8),
    ])
    
    plt.figure(figsize=(8, 8))
    plt.imshow(rgb_img)
    plt.title("Pseudo-RGB from Cube")
    plt.axis('off')
    plt.tight_layout()
    plt.show()
else:
    print("⚠️ Not enough bands to show RGB (need at least 151 bands).")
