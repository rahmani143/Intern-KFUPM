import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

def filter_by_windowed_horizontal_stability(xs, ys, window_size=10, max_range=20):
    filtered_x = []
    filtered_y = []

    for i in range(len(xs) - window_size + 1):
        window_xs = xs[i:i + window_size]
        if np.max(window_xs) - np.min(window_xs) <= max_range:
            filtered_x.extend(window_xs)
            filtered_y.extend(ys[i:i + window_size])

    # Remove duplicates while preserving order
    unique = list(dict.fromkeys(zip(filtered_x, filtered_y)))
    filtered_x, filtered_y = zip(*unique) if unique else ([], [])
    return np.array(filtered_x), np.array(filtered_y)

def fit_polynomial(xs, ys, max_degree=7):
    best_poly = None
    min_error = float('inf')
    best_degree = 1

    for degree in range(3, max_degree + 1):
        if len(xs) < degree + 1:
            continue
        poly = np.poly1d(np.polyfit(xs, ys, degree))
        error = np.mean((poly(xs) - ys) ** 2)
        if error < min_error:
            min_error = error
            best_poly = poly
            best_degree = degree

    return best_poly, best_degree

def fit_and_plot_on_image(image_path, csv_path, output_folder=None):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to read image: {image_path}")
        return

    # Skip first line of CSV which is a descriptive header, not column names
    df = pd.read_csv(csv_path, skiprows=1)
    if not {'column', 'row'}.issubset(df.columns):
        print(f"CSV missing expected columns: {csv_path}")
        return

    xs = df['column'].values
    ys = df['row'].values

    sorted_idx = np.argsort(xs)
    xs, ys = xs[sorted_idx], ys[sorted_idx]

    filtered_xs, filtered_ys = filter_by_windowed_horizontal_stability(xs, ys, window_size=10, max_range=20)

    if len(filtered_xs) < 5:
        print(f"Too few points after filtering in {csv_path}")
        return

    poly, best_degree = fit_polynomial(filtered_xs, filtered_ys)

    img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    height, width = img.shape

    x_vals = np.linspace(min(filtered_xs), max(filtered_xs), 1000)
    y_vals = poly(x_vals)

    valid_points = [(int(x), int(y)) for x, y in zip(x_vals, y_vals)
                    if 0 <= int(x) < width and 0 <= int(y) < height]

    for pt in valid_points:
        cv2.circle(img_color, pt, radius=1, color=(0, 0, 255), thickness=1)

    window_name = os.path.basename(image_path)
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow(window_name, img_color)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if output_folder:
        os.makedirs(output_folder, exist_ok=True)
        out_path = os.path.join(output_folder, os.path.basename(image_path).replace('.tif', '_curve.png'))
        cv2.imwrite(out_path, img_color)
        print(f"Saved: {out_path}")
        print(f"Used polynomial degree: {best_degree}")

    # Return polynomial info for JSON saving
    return {
        "image": os.path.basename(image_path),
        "polynomial_degree": best_degree,
        "coefficients": poly.coefficients.tolist()
    }

def process_all(image_folder, csv_folder, output_folder=None):
    results = []
    for image_file in sorted(os.listdir(image_folder)):
        if not image_file.lower().endswith('.png'):
            continue
        base = os.path.splitext(image_file)[0]
        image_path = os.path.join(image_folder, image_file)
        csv_path = os.path.join(csv_folder, base + '.csv')

        if not os.path.exists(csv_path):
            print(f"Missing CSV for {image_file}, skipping.")
            continue

        result = fit_and_plot_on_image(image_path, csv_path, output_folder=output_folder)
        if result:
            results.append(result)

    if output_folder and results:
        json_path = os.path.join(save_json, "polynomials_coefficients.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Polynomial coefficients saved to {json_path}")

# === CONFIGURATION ===
image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"
csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\csv_output"
output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\curve_output"
save_json = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"
process_all(image_folder, csv_folder, output_folder)


print("Processing complete.")