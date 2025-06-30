# import os
# import json
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import interp1d

# def compute_wavelengths(coeffs, pixel_indices):
#     """
#     Given polynomial coefficients and pixel indices,
#     compute wavelength for each pixel (horizontal axis).
#     """
#     # coeffs expected highest degree first for np.polyval
#     wavelengths = np.polyval(coeffs, pixel_indices)
#     return wavelengths

# def resample_band_image(img, orig_wavelengths, target_wavelengths):
#     """
#     Resample the band image along the horizontal axis (wavelength axis)
#     so all bands align to the same wavelength grid.
#     """
#     height, width = img.shape
#     resampled_img = np.zeros((height, len(target_wavelengths)), dtype=img.dtype)

#     # For each row, interpolate intensity values to target wavelengths
#     for row in range(height):
#         interp_func = interp1d(orig_wavelengths, img[row, :], kind='linear',
#                                bounds_error=False, fill_value=0)
#         resampled_img[row, :] = interp_func(target_wavelengths)

#     return resampled_img

# def build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_path, target_wavelength_step=1.0):
#     # Load spectral polynomial data
#     with open(spectral_poly_json_path, 'r') as f:
#         spectral_data = json.load(f)

#     # Sort spectral data by wavelength (extract from filename)
#     def get_wavelength(fname):
#         digits = ''.join(filter(str.isdigit, fname))
#         return int(digits) if digits else 0

#     spectral_data_sorted = sorted(spectral_data, key=lambda x: get_wavelength(x['image']))

#     # Load first image to get shape and pixel count
#     first_image_path = os.path.join(image_folder, spectral_data_sorted[0]['image'])
#     first_img = cv2.imread(first_image_path, cv2.IMREAD_GRAYSCALE)
#     if first_img is None:
#         raise RuntimeError(f"Cannot read first image {first_image_path}")

#     height, width = first_img.shape
#     pixel_indices = np.arange(width)

#     # Compute wavelength ranges for all bands to find common wavelength range
#     all_min_wl = []
#     all_max_wl = []
#     all_wavelengths = []

#     for band in spectral_data_sorted:
#         wl = compute_wavelengths(band['coefficients'], pixel_indices)
#         all_wavelengths.append(wl)
#         all_min_wl.append(wl.min())
#         all_max_wl.append(wl.max())

#     # Define a common wavelength grid (uniform)
#     common_min_wl = max(all_min_wl)  # highest min wavelength to ensure overlap
#     common_max_wl = min(all_max_wl)  # lowest max wavelength for overlap
#     num_points = int(np.ceil((common_max_wl - common_min_wl) / target_wavelength_step)) + 1
#     common_wavelength_grid = np.linspace(common_min_wl, common_max_wl, num_points)

#     print(f"Common wavelength grid from {common_min_wl:.2f}nm to {common_max_wl:.2f}nm with {num_points} points.")

#     # Resample each band to the common wavelength grid
#     resampled_images = []

#     for band, wl in zip(spectral_data_sorted, all_wavelengths):
#         img_path = os.path.join(image_folder, band['image'])
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             print(f"Warning: Failed to load {band['image']}, skipping.")
#             continue

#         resampled_img = resample_band_image(img, wl, common_wavelength_grid)
#         resampled_images.append(resampled_img)

#     if not resampled_images:
#         raise RuntimeError("No images loaded successfully.")

#     # Stack images along spectral axis (bands)
#     cube = np.stack(resampled_images, axis=2)  # shape: height x wavelength_points x bands

#     print(f"Hyperspectral cube shape (height, spectral points, bands): {cube.shape}")

#     # Save cube and common wavelength grid
#     np.save(output_path, cube)
#     np.save(output_path.replace(".npy", "_wavelengths.npy"), common_wavelength_grid)

#     print(f"Saved hyperspectral cube to {output_path}")
#     print(f"Saved wavelength grid to {output_path.replace('.npy', '_wavelengths.npy')}")

#     # Optional visualization: mean intensity across spectral bands
#     plt.imshow(np.mean(cube, axis=2), cmap='gray')
#     plt.title("Mean intensity projection (averaged over bands)")
#     plt.axis('off')
#     plt.show()

# if __name__ == "__main__":
#     # Update these paths to your setup
#     image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
#     spectral_poly_json_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\polynomials_coefficients.json"
#     output_cube_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\hsi_cube_spectral_trial"

#     build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_cube_path)







# edit 1:










# import os
# import json
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.interpolate import interp1d

# def compute_wavelengths(coeffs, pixel_indices):
#     """
#     Given polynomial coefficients and pixel indices,
#     compute wavelength for each pixel (horizontal axis).
#     """
#     wavelengths = np.polyval(coeffs, pixel_indices)
#     return wavelengths

# def resample_band_image(img, orig_wavelengths, target_wavelengths):
#     """
#     Resample the band image along the horizontal axis (wavelength axis)
#     so all bands align to the same wavelength grid.
#     """
#     height, width = img.shape
#     resampled_img = np.zeros((height, len(target_wavelengths)), dtype=img.dtype)

#     for row in range(height):
#         interp_func = interp1d(orig_wavelengths, img[row, :], kind='linear',
#                                bounds_error=False, fill_value=0)
#         resampled_img[row, :] = interp_func(target_wavelengths)

#     return resampled_img

# def build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_path, target_wavelength_step=1.0):
#     # Load spectral polynomial data
#     with open(spectral_poly_json_path, 'r') as f:
#         spectral_data = json.load(f)

#     # Sort spectral data by wavelength extracted from filename
#     def get_wavelength(fname):
#         digits = ''.join(filter(str.isdigit, fname))
#         return int(digits) if digits else 0

#     spectral_data_sorted = sorted(spectral_data, key=lambda x: get_wavelength(x['image']))

#     # Load first image to get shape and pixel count
#     first_image_path = os.path.join(image_folder, spectral_data_sorted[0]['image'])
#     first_img = cv2.imread(first_image_path, cv2.IMREAD_GRAYSCALE)
#     if first_img is None:
#         raise RuntimeError(f"Cannot read first image {first_image_path}")

#     height, width = first_img.shape
#     pixel_indices = np.arange(width)

#     # Compute wavelength ranges for all bands
#     all_min_wl = []
#     all_max_wl = []
#     all_wavelengths = []

#     for band in spectral_data_sorted:
#         wl = compute_wavelengths(band['coefficients'], pixel_indices)
#         all_wavelengths.append(wl)
#         all_min_wl.append(wl.min())
#         all_max_wl.append(wl.max())

#     # Print wavelength ranges for debugging
#     print("Wavelength ranges for all bands:")
#     for band, min_wl, max_wl in zip(spectral_data_sorted, all_min_wl, all_max_wl):
#         print(f"{band['image']}: {min_wl:.2f} nm to {max_wl:.2f} nm")

#     # Use union of wavelength ranges (not intersection) to avoid negative sample count
#     common_min_wl = min(all_min_wl)
#     common_max_wl = max(all_max_wl)
#     num_points = int(np.ceil((common_max_wl - common_min_wl) / target_wavelength_step)) + 1
#     common_wavelength_grid = np.linspace(common_min_wl, common_max_wl, num_points)

#     print(f"Using common wavelength range: {common_min_wl:.2f} nm to {common_max_wl:.2f} nm")
#     print(f"Number of wavelength points in grid: {num_points}")

#     # Resample each band image to the common wavelength grid
#     resampled_images = []

#     for band, wl in zip(spectral_data_sorted, all_wavelengths):
#         img_path = os.path.join(image_folder, band['image'])
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
#         if img is None:
#             print(f"Warning: Failed to load {band['image']}, skipping.")
#             continue

#         resampled_img = resample_band_image(img, wl, common_wavelength_grid)
#         resampled_images.append(resampled_img)

#     if not resampled_images:
#         raise RuntimeError("No images loaded successfully.")

#     # Stack images into a cube: shape (height, wavelength_points, bands)
#     cube = np.stack(resampled_images, axis=2)

#     print(f"Hyperspectral cube shape (height, spectral points, bands): {cube.shape}")

#     # Save cube and wavelength grid
#     np.save(output_path, cube)
#     np.save(output_path.replace(".npy", "_wavelengths.npy"), common_wavelength_grid)

#     print(f"Saved hyperspectral cube to {output_path}")
#     print(f"Saved wavelength grid to {output_path.replace('.npy', '_wavelengths.npy')}")

#     # Optional: visualize average intensity across bands
#     plt.imshow(np.mean(cube, axis=2), cmap='gray')
#     plt.title("Mean intensity projection (averaged over bands)")
#     plt.axis('off')
#     plt.show()

# if __name__ == "__main__":
#     # Customize these paths for your setup:
#     image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
#     spectral_poly_json_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\polynomials_coefficients.json"
#     output_cube_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\hsi_cube_spectral_trial"


#     build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_cube_path)








# edit 2:
















import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def compute_wavelengths(coeffs, pixel_indices):
    """
    Given polynomial coefficients and pixel indices,
    compute wavelength for each pixel (horizontal axis).
    """
    wavelengths = np.polyval(coeffs, pixel_indices)
    return wavelengths

def resample_band_image(img, orig_wavelengths, target_wavelengths):
    """
    Resample the band image along the horizontal axis (wavelength axis)
    so all bands align to the same wavelength grid.
    """
    height, width = img.shape
    resampled_img = np.zeros((height, len(target_wavelengths)), dtype=img.dtype)

    for row in range(height):
        interp_func = interp1d(orig_wavelengths, img[row, :], kind='linear',
                               bounds_error=False, fill_value=0)
        resampled_img[row, :] = interp_func(target_wavelengths)

    return resampled_img

def build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_path, target_wavelength_step=1.0):
    # Load spectral polynomial data
    with open(spectral_poly_json_path, 'r') as f:
        spectral_data = json.load(f)

    # Sort spectral data by wavelength extracted from filename
    def get_wavelength(fname):
        digits = ''.join(filter(str.isdigit, fname))
        return int(digits) if digits else 0

    spectral_data_sorted = sorted(spectral_data, key=lambda x: get_wavelength(x['image']))

    # Load first image to get shape and pixel count
    first_image_path = os.path.join(image_folder, spectral_data_sorted[0]['image'])
    first_img = cv2.imread(first_image_path, cv2.IMREAD_GRAYSCALE)
    if first_img is None:
        raise RuntimeError(f"Cannot read first image {first_image_path}")

    height, width = first_img.shape
    pixel_indices = np.arange(width)

    # Compute wavelength ranges for all bands
    all_min_wl = []
    all_max_wl = []
    all_wavelengths = []

    for band in spectral_data_sorted:
        wl = compute_wavelengths(band['coefficients'], pixel_indices)
        all_wavelengths.append(wl)
        all_min_wl.append(wl.min())
        all_max_wl.append(wl.max())

    # Print wavelength ranges for debugging
    print("Wavelength ranges for all bands:")
    for band, min_wl, max_wl in zip(spectral_data_sorted, all_min_wl, all_max_wl):
        print(f"{band['image']}: {min_wl:.2f} nm to {max_wl:.2f} nm")

    # Define sensor limits
    sensor_min_wl = 400
    sensor_max_wl = 1000

    # Use union of wavelength ranges clipped to sensor range
    common_min_wl = max(min(all_min_wl), sensor_min_wl)
    common_max_wl = min(max(all_max_wl), sensor_max_wl)

    if common_min_wl >= common_max_wl:
        raise ValueError(f"No valid wavelength overlap within sensor range {sensor_min_wl}-{sensor_max_wl} nm.")

    num_points = int(np.ceil((common_max_wl - common_min_wl) / target_wavelength_step)) + 1
    common_wavelength_grid = np.linspace(common_min_wl, common_max_wl, num_points)

    print(f"Clipped wavelength range to sensor limits: {common_min_wl:.2f} nm to {common_max_wl:.2f} nm")
    print(f"Number of wavelength points in grid: {num_points}")

    # Resample each band image to the common wavelength grid
    resampled_images = []

    for band, wl in zip(spectral_data_sorted, all_wavelengths):
        img_path = os.path.join(image_folder, band['image'])
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Warning: Failed to load {band['image']}, skipping.")
            continue

        resampled_img = resample_band_image(img, wl, common_wavelength_grid)
        resampled_images.append(resampled_img)

    if not resampled_images:
        raise RuntimeError("No images loaded successfully.")

    # Stack images into a cube: shape (height, spectral points, bands)
    cube = np.stack(resampled_images, axis=2)

    print(f"Hyperspectral cube shape (height, spectral points, bands): {cube.shape}")

    # Save cube and wavelength grid
    np.save(output_path, cube)
    np.save(output_path.replace(".npy", "_wavelengths.npy"), common_wavelength_grid)

    print(f"Saved hyperspectral cube to {output_path}")
    print(f"Saved wavelength grid to {output_path.replace('.npy', '_wavelengths.npy')}")

    # Optional: visualize average intensity across bands
    plt.imshow(np.mean(cube, axis=2), cmap='gray')
    plt.title("Mean intensity projection (averaged over bands)")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
    spectral_poly_json_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\polynomials_coefficients.json"
    output_cube_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\hsi_cube_spectral_trial.npy"

    build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_cube_path)
