# import os
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# def fit_and_plot_on_image(image_path, csv_path, degree=3, max_pixel_gap=50, output_folder=None):
#     # Read image
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         print(f"Could not read image: {image_path}")
#         return

#     # Read CSV
#     df = pd.read_csv(csv_path)
#     if {'column', 'row'}.issubset(df.columns):
#         xs = df['column'].values
#         ys = df['row'].values
#     else:
#         print(f"CSV missing expected columns: {csv_path}")
#         return

#     # Sort by x to maintain order
#     sorted_idx = np.argsort(xs)
#     xs = xs[sorted_idx]
#     ys = ys[sorted_idx]

#     # Filter out outliers (vertical jumps)
#     filtered_x = [xs[0]]
#     filtered_y = [ys[0]]
#     for i in range(1, len(xs)):
#         if abs(ys[i] - ys[i - 1]) <= max_pixel_gap:
#             filtered_x.append(xs[i])
#             filtered_y.append(ys[i])

#     if len(filtered_x) < degree + 1:
#         print(f"Not enough valid points in {csv_path} to fit polynomial.")
#         return

#     # Fit polynomial
#     coeffs = np.polyfit(filtered_x, filtered_y, degree)
#     poly = np.poly1d(coeffs)

#     # Convert grayscale image to color for plotting red curve
#     img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

#     # Generate curve points
#     x_vals = np.linspace(min(filtered_x), max(filtered_x), num=1000)
#     y_vals = poly(x_vals)

#     # Clip curve to stay inside image
#     height, width = img.shape
#     valid_points = [(int(x), int(y)) for x, y in zip(x_vals, y_vals)
#                     if 0 <= int(x) < width and 0 <= int(y) < height]

#     # Draw curve
#     for pt in valid_points:
#         cv2.circle(img_color, pt, radius=1, color=(0, 0, 255), thickness=1)

#     # Display the result full-screen
#     window_name = os.path.basename(image_path)
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.imshow(window_name, img_color)
#     cv2.resizeWindow(window_name, 1280, 720)  # Fit to screen size
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Optional: Save result
#     if output_folder:
#         os.makedirs(output_folder, exist_ok=True)
#         output_path = os.path.join(output_folder, os.path.basename(image_path).replace('.tif', '_curve.png'))
#         cv2.imwrite(output_path, img_color)
#         print(f"Saved: {output_path}")

# def process_all_pairs(image_folder, csv_folder, output_folder=None, degree=3, max_pixel_gap=50):
#     image_files = [f for f in os.listdir(image_folder) if f.lower().endswith('.tif')]

#     for image_file in sorted(image_files):
#         base_name = os.path.splitext(image_file)[0]
#         image_path = os.path.join(image_folder, image_file)
#         csv_path = os.path.join(csv_folder, f"{base_name}.csv")

#         if not os.path.exists(csv_path):
#             print(f"Missing CSV for {image_file}, skipping.")
#             continue

#         print(f"Processing {base_name}...")
#         fit_and_plot_on_image(image_path, csv_path, degree, max_pixel_gap, output_folder)

# # === CONFIGURATION ===
# image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
# csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
# output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\curve_output"  # optional

# process_all_pairs(image_folder, csv_folder, output_folder, degree=3, max_pixel_gap=50)















# edit 1:












# import os
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# def fit_polynomial(xs, ys, max_degree=7, max_pixel_gap=50):
#     # Filter based on vertical jump
#     filtered_x, filtered_y = [xs[0]], [ys[0]]
#     for i in range(1, len(xs)):
#         if abs(ys[i] - ys[i-1]) <= max_pixel_gap:
#             filtered_x.append(xs[i])
#             filtered_y.append(ys[i])

#     filtered_x = np.array(filtered_x)
#     filtered_y = np.array(filtered_y)

#     best_poly = None
#     min_error = float('inf')
#     best_degree = 1

#     for degree in range(3, max_degree + 1):  # Try from degree 3 to max_degree
#         if len(filtered_x) < degree + 1:
#             continue
#         poly = np.poly1d(np.polyfit(filtered_x, filtered_y, degree))
#         error = np.mean((poly(filtered_x) - filtered_y)**2)
#         if error < min_error:
#             min_error = error
#             best_poly = poly
#             best_degree = degree

#     return best_poly, filtered_x, filtered_y, best_degree

# def fit_and_plot_on_image(image_path, csv_path, max_degree=7, max_pixel_gap=50, output_folder=None):
#     # Load image
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         print(f"Failed to read image: {image_path}")
#         return

#     # Load points
#     df = pd.read_csv(csv_path)
#     if not {'column', 'row'}.issubset(df.columns):
#         print(f"CSV missing expected columns: {csv_path}")
#         return

#     xs = df['column'].values
#     ys = df['row'].values

#     # Sort by x
#     sorted_idx = np.argsort(xs)
#     xs, ys = xs[sorted_idx], ys[sorted_idx]

#     # Fit best polynomial
#     poly, filtered_x, filtered_y, best_degree = fit_polynomial(xs, ys, max_degree=max_degree, max_pixel_gap=max_pixel_gap)
#     if poly is None:
#         print(f"Not enough points in {csv_path} to fit polynomial.")
#         return

#     # Create color image and draw curve
#     img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     height, width = img.shape

#     x_vals = np.linspace(min(filtered_x), max(filtered_x), 1000)
#     y_vals = poly(x_vals)

#     valid_points = [(int(x), int(y)) for x, y in zip(x_vals, y_vals)
#                     if 0 <= int(x) < width and 0 <= int(y) < height]

#     for x, y in valid_points:
#         cv2.circle(img_color, (x, y), radius=1, color=(0, 0, 255), thickness=1)

#     # Show full-sized window
#     window_name = os.path.basename(image_path)
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.imshow(window_name, img_color)
#     cv2.resizeWindow(window_name, 1280, 720)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if output_folder:
#         os.makedirs(output_folder, exist_ok=True)
#         out_path = os.path.join(output_folder, os.path.basename(image_path).replace('.tif', '_curve.png'))
#         cv2.imwrite(out_path, img_color)
#         print(f"Saved: {out_path}")
#         print(f"Polynomial degree used: {best_degree}")
#         print(f"Polynomial: {poly}")

# def process_all_pairs(image_folder, csv_folder, output_folder=None, max_degree=7, max_pixel_gap=50):
#     for image_file in sorted(os.listdir(image_folder)):
#         if not image_file.lower().endswith('.tif'):
#             continue
#         base = os.path.splitext(image_file)[0]
#         image_path = os.path.join(image_folder, image_file)
#         csv_path = os.path.join(csv_folder, base + '.csv')

#         if not os.path.exists(csv_path):
#             print(f"Missing CSV for {image_file}, skipping.")
#             continue

#         fit_and_plot_on_image(image_path, csv_path, max_degree=max_degree,
#                               max_pixel_gap=max_pixel_gap, output_folder=output_folder)

# # === CONFIGURATION ===
# image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
# csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
# output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\curve_output"

# process_all_pairs(image_folder, csv_folder, output_folder, max_degree=7, max_pixel_gap=50)




















# edit 2:


















# import os
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# def filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=20):
#     filtered_x = []
#     filtered_y = []

#     for i in range(len(xs) - window_size + 1):
#         window_ys = ys[i:i + window_size]
#         if np.max(window_ys) - np.min(window_ys) <= max_range:
#             filtered_x.extend(xs[i:i + window_size])
#             filtered_y.extend(window_ys)

#     # Remove duplicates while preserving order
#     unique = list(dict.fromkeys(zip(filtered_x, filtered_y)))
#     filtered_x, filtered_y = zip(*unique) if unique else ([], [])
#     return np.array(filtered_x), np.array(filtered_y)

# def fit_polynomial(xs, ys, max_degree=7):
#     best_poly = None
#     min_error = float('inf')
#     best_degree = 1

#     for degree in range(3, max_degree + 1):
#         if len(xs) < degree + 1:
#             continue
#         poly = np.poly1d(np.polyfit(xs, ys, degree))
#         error = np.mean((poly(xs) - ys) ** 2)
#         if error < min_error:
#             min_error = error
#             best_poly = poly
#             best_degree = degree

#     return best_poly, best_degree

# def fit_and_plot_on_image(image_path, csv_path, output_folder=None):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         print(f"Failed to read image: {image_path}")
#         return

#     df = pd.read_csv(csv_path)
#     if not {'column', 'row'}.issubset(df.columns):
#         print(f"CSV missing expected columns: {csv_path}")
#         return

#     xs = df['column'].values
#     ys = df['row'].values

#     sorted_idx = np.argsort(xs)
#     xs, ys = xs[sorted_idx], ys[sorted_idx]

#     filtered_xs, filtered_ys = filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=20)

#     if len(filtered_xs) < 5:
#         print(f"Too few points after filtering in {csv_path}")
#         return

#     poly, best_degree = fit_polynomial(filtered_xs, filtered_ys)

#     img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     height, width = img.shape

#     x_vals = np.linspace(min(filtered_xs), max(filtered_xs), 1000)
#     y_vals = poly(x_vals)

#     valid_points = [(int(x), int(y)) for x, y in zip(x_vals, y_vals)
#                     if 0 <= int(x) < width and 0 <= int(y) < height]

#     for pt in valid_points:
#         cv2.circle(img_color, pt, radius=1, color=(0, 0, 255), thickness=1)

#     window_name = os.path.basename(image_path)
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.imshow(window_name, img_color)
#     cv2.resizeWindow(window_name, 1280, 720)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if output_folder:
#         os.makedirs(output_folder, exist_ok=True)
#         out_path = os.path.join(output_folder, os.path.basename(image_path).replace('.tif', '_curve.png'))
#         cv2.imwrite(out_path, img_color)
#         print(f"Saved: {out_path}")
#         print(f"Used polynomial degree: {best_degree}")

# def process_all(image_folder, csv_folder, output_folder=None):
#     for image_file in sorted(os.listdir(image_folder)):
#         if not image_file.lower().endswith('.tif'):
#             continue
#         base = os.path.splitext(image_file)[0]
#         image_path = os.path.join(image_folder, image_file)
#         csv_path = os.path.join(csv_folder, base + '.csv')

#         if not os.path.exists(csv_path):
#             print(f"Missing CSV for {image_file}, skipping.")
#             continue

#         fit_and_plot_on_image(image_path, csv_path, output_folder=output_folder)

# # === CONFIGURATION ===
# image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
# csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
# output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\curve_output"

# process_all(image_folder, csv_folder, output_folder)











# edit 3:














import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json

def filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=20):
    filtered_x = []
    filtered_y = []

    for i in range(len(xs) - window_size + 1):
        window_ys = ys[i:i + window_size]
        if np.max(window_ys) - np.min(window_ys) <= max_range:
            filtered_x.extend(xs[i:i + window_size])
            filtered_y.extend(window_ys)

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

    df = pd.read_csv(csv_path)
    if not {'column', 'row'}.issubset(df.columns):
        print(f"CSV missing expected columns: {csv_path}")
        return

    xs = df['column'].values
    ys = df['row'].values

    sorted_idx = np.argsort(xs)
    xs, ys = xs[sorted_idx], ys[sorted_idx]

    filtered_xs, filtered_ys = filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=20)

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
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.imshow(window_name, img_color)
    cv2.resizeWindow(window_name, 1280, 720)
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
        if not image_file.lower().endswith('.tif'):
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

    # Save polynomial coefficients info to JSON file
    if output_folder and results:
        json_path = os.path.join(save_json, "polynomials_coefficients.json")
        with open(json_path, 'w') as f:
            json.dump(results, f, indent=4)
        print(f"Polynomial coefficients saved to {json_path}")

# === CONFIGURATION ===
image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\curve_output"
save_json = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
process_all(image_folder, csv_folder, output_folder)











# edit 4:












# import os
# import cv2
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import json

# def filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=20):
#     filtered_x = []
#     filtered_y = []

#     for i in range(len(xs) - window_size + 1):
#         window_xs = xs[i:i + window_size]
#         window_ys = ys[i:i + window_size]
#         if np.max(window_ys) - np.min(window_ys) <= max_range:
#             mid_idx = i + window_size // 2
#             filtered_x.append(xs[mid_idx])
#             filtered_y.append(ys[mid_idx])

#     return np.array(filtered_x), np.array(filtered_y)


# def fit_polynomial(xs, ys, max_degree=7):
#     best_poly = None
#     min_error = float('inf')
#     best_degree = 1

#     for degree in range(3, max_degree + 1):
#         if len(xs) < degree + 1:
#             continue
#         poly = np.poly1d(np.polyfit(xs, ys, degree))
#         error = np.mean((poly(xs) - ys) ** 2)
#         if error < min_error:
#             min_error = error
#             best_poly = poly
#             best_degree = degree

#     return best_poly, best_degree

# def fit_and_plot_on_image(image_path, csv_path, output_folder=None):
#     img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if img is None:
#         print(f"Failed to read image: {image_path}")
#         return

#     df = pd.read_csv(csv_path)
#     if not {'column', 'row'}.issubset(df.columns):
#         print(f"CSV missing expected columns: {csv_path}")
#         return

#     xs = df['column'].values
#     ys = df['row'].values

#     sorted_idx = np.argsort(xs)
#     xs, ys = xs[sorted_idx], ys[sorted_idx]

#     filtered_xs, filtered_ys = filter_by_windowed_vertical_stability(xs, ys, window_size=10, max_range=100)

#     if len(filtered_xs) < 5:
#         print(f"Too few points after filtering in {csv_path}")
#         return

#     poly, best_degree = fit_polynomial(filtered_xs, filtered_ys)

#     img_color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     height, width = img.shape

#     x_vals = np.linspace(min(filtered_xs), max(filtered_xs), 1000)
#     y_vals = poly(x_vals)

#     valid_points = [(int(x), int(y)) for x, y in zip(x_vals, y_vals)
#                     if 0 <= int(x) < width and 0 <= int(y) < height]

#     for pt in valid_points:
#         cv2.circle(img_color, pt, radius=1, color=(0, 0, 255), thickness=1)

#     # === Fullscreen display ===
#     window_name = os.path.basename(image_path)
#     cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
#     cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow(window_name, img_color)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if output_folder:
#         os.makedirs(output_folder, exist_ok=True)
#         out_path = os.path.join(output_folder, os.path.basename(image_path).replace('.tif', '_curve.png'))
#         cv2.imwrite(out_path, img_color)
#         print(f"Saved: {out_path}")
#         print(f"Used polynomial degree: {best_degree}")

#     return {
#         "image": os.path.basename(image_path),
#         "polynomial_degree": best_degree,
#         "coefficients": poly.coefficients.tolist()
#     }

# def process_all(image_folder, csv_folder, output_folder=None):
#     results = []
#     for image_file in sorted(os.listdir(image_folder)):
#         if not image_file.lower().endswith('.tif'):
#             continue
#         base = os.path.splitext(image_file)[0]
#         image_path = os.path.join(image_folder, image_file)
#         csv_path = os.path.join(csv_folder, base + '.csv')

#         if not os.path.exists(csv_path):
#             print(f"Missing CSV for {image_file}, skipping.")
#             continue

#         result = fit_and_plot_on_image(image_path, csv_path, output_folder=output_folder)
#         if result:
#             results.append(result)

#     if output_folder and results:
#         json_path = os.path.join(output_folder, "polynomials_coefficients.json")
#         with open(json_path, 'w') as f:
#             json.dump(results, f, indent=4)
#         print(f"Polynomial coefficients saved to {json_path}")

# # === CONFIGURATION ===
# image_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
# csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
# output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\curve_output"

# process_all(image_folder, csv_folder, output_folder)







