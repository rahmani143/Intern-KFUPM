import os
import json
import cv2
import numpy as np
import matplotlib.pyplot as plt

def compute_curve_y(coeffs, x_vals):
    return np.polyval(coeffs, x_vals).astype(int)

def straighten_image(img, curve_y):
    height, width = img.shape
    y_ref = int(np.median(curve_y))  # reference line

    straight_img = np.zeros_like(img)
    for x in range(width):
        shift = curve_y[x] - y_ref
        col = img[:, x]
        col_shifted = np.roll(col, -shift)
        # zero padding to avoid wrap-around
        if shift > 0:
            col_shifted[-shift:] = 0
        elif shift < 0:
            col_shifted[:-shift] = 0
        straight_img[:, x] = col_shifted
    return straight_img

def get_wavelength(fname):
    # Extract numeric wavelength from filename, e.g. '410nm.tif' → 410
    digits = ''.join(filter(str.isdigit, fname))
    return int(digits) if digits else 0

def build_hyperspectral_cube(image_folder, polynomial_json_path, output_cube_path):
    # Load polynomial JSON
    with open(polynomial_json_path, 'r') as f:
        poly_data = json.load(f)

    # Sort by wavelength (assuming filenames include wavelength numbers)
    poly_data_sorted = sorted(poly_data, key=lambda x: get_wavelength(x['image']))

    cube_images = []

    for entry in poly_data_sorted:
        image_path = os.path.join(image_folder, entry['image'])
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"Warning: could not load image {entry['image']}")
            continue
        width = img.shape[1]
        x_vals = np.arange(width)
        curve_y = compute_curve_y(entry['coefficients'], x_vals)
        straight_img = straighten_image(img, curve_y)
        cube_images.append(straight_img)

    if not cube_images:
        print("No images processed. Exiting.")
        return

    cube = np.stack(cube_images, axis=2)
    print(f"Hyperspectral cube shape: {cube.shape}")

    np.save(output_cube_path, cube)
    print(f"Saved cube to {output_cube_path}")

    # Visualization: mean intensity projection
    plt.imshow(np.mean(cube, axis=2), cmap='gray')
    plt.title("Mean Intensity Projection of Hyperspectral Cube")
    plt.axis('off')
    plt.show()

# === USAGE ===
if __name__ == "__main__":
    image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"             # Change this to your images folder
    polynomial_json_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\polynomials_coefficients.json" # Change this to your polynomial JSON file
    output_cube_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\hsi_cube_test"       # Output file

    build_hyperspectral_cube(image_folder, polynomial_json_path, output_cube_path)
