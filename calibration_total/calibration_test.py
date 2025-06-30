import os
import cv2
import numpy as np
import json
from tqdm import tqdm
from scipy.interpolate import interp1d


def apply_polynomial(coeffs, y_indices):
    """
    Apply polynomial to y-indices to get corresponding wavelengths.
    """
    return np.polyval(coeffs, y_indices)


def build_hsi_cube_spectral(image_folder, spectral_poly_json_path, output_cube_path,
                             wavelength_range=(400, 1000), num_points=600):
    """
    Builds an HSI cube using spectral calibration.
    Assumes:
    - Spectral information is along the **vertical (y)** axis of images.
    - Spatial information is along the **horizontal (x)** axis.

    Args:
        image_folder: Folder containing TIFF/PNG grayscale spectral band images.
        spectral_poly_json_path: JSON file with polynomial coefficients per image.
        output_cube_path: Path to save final hyperspectral cube (NumPy .npy format).
        wavelength_range: Tuple (min_wavelength, max_wavelength).
        num_points: Number of wavelengths to sample across the range.
    """
    # Load polynomial coefficients
    with open(spectral_poly_json_path, 'r') as f:
        spectral_data = json.load(f)

    # Build common wavelength axis
    wl_min, wl_max = wavelength_range
    common_wavelengths = np.linspace(wl_min, wl_max, num_points)

    # Prepare HSI cube holder
    example_img_path = os.path.join(image_folder, spectral_data[0]['image'])
    example_img = cv2.imread(example_img_path, cv2.IMREAD_GRAYSCALE)
    if example_img is None:
        raise FileNotFoundError(f"Could not read example image: {example_img_path}")

    height, width = example_img.shape
    hsi_cube = np.zeros((num_points, width, len(spectral_data)), dtype=np.float32)

    print("\nBuilding HSI cube with spectral calibration...")

    for band_idx, band_info in enumerate(tqdm(spectral_data)):
        image_name = band_info['image']
        coeffs = band_info['coefficients']

        img_path = os.path.join(image_folder, image_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Image not found: {img_path}")

        # Apply polynomial to y-indices
        y_indices = np.arange(height)
        wavelengths = apply_polynomial(coeffs, y_indices)

        # Interpolate image rows (spectral axis) to common wavelength grid
        for x in range(width):
            col_profile = img[:, x]  # vertical profile (spectral)
            try:
                interp_func = interp1d(wavelengths, col_profile,
                                       kind='linear', bounds_error=False, fill_value=0)
                hsi_cube[:, x, band_idx] = interp_func(common_wavelengths)
            except Exception as e:
                print(f"Warning: interpolation failed at column {x} in {image_name}: {e}")

    # Save cube
    np.save(output_cube_path, hsi_cube)
    print(f"\n✅ HSI cube saved to: {output_cube_path}")


# ======== Example usage ========
if __name__ == '__main__':
    image_folder = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity'
    spectral_poly_json_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\polynomials_coefficients.json"
    output_cube_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\hsi_cube_spectral_trial\test1.npy'

    build_hsi_cube_spectral(
        image_folder,
        spectral_poly_json_path,
        output_cube_path,
        wavelength_range=(400, 1000),
        num_points=600
    )
