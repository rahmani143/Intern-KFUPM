# import os
# import cv2
# import numpy as np
# import csv

# def process_image(image_path, output_csv_folder):
#     image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#     if image is None:
#         print(f"Failed to load image: {image_path}")
#         return

#     height, width = image.shape
#     max_intensity_points = []

#     for col in range(width):
#         column_values = image[:, col]
#         max_row = np.argmax(column_values)
#         max_intensity_points.append((col, max_row))  # (column, row)

#     image_name = os.path.splitext(os.path.basename(image_path))[0]
#     csv_path = os.path.join(output_csv_folder, f"{image_name}_points.csv")

#     with open(csv_path, mode='w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(["index", "column", "row"])
#         for idx, (col, row) in enumerate(max_intensity_points):
#             writer.writerow([idx, col, row])

#     print(f"Processed and saved: {csv_path}")

# def process_folder(folder_path, output_csv_folder):
#     os.makedirs(output_csv_folder, exist_ok=True)

#     supported_exts = ('.png', '.jpg', '.jpeg', '.tif', '.tiff', '.bmp')
#     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]

#     if not image_files:
#         print("No supported image files found.")
#         return

#     for image_file in image_files:
#         full_path = os.path.join(folder_path, image_file)
#         process_image(full_path, output_csv_folder)

# # === CONFIGURATION ===
# input_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"         
# output_csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"      

# process_folder(input_folder, output_csv_folder)








# edit 1:









# import os
# import cv2
# import numpy as np
# import csv

# def process_folder(folder_path, output_csv_path):
#     supported_exts = ('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.bmp')
#     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
#     image_files.sort()  # Optional: sort by name for consistent order

#     if not image_files:
#         print("No supported image files found in folder.")
#         return

#     with open(output_csv_path, mode='w', newline='') as file:
#         writer = csv.writer(file)

#         for image_file in image_files:
#             image_path = os.path.join(folder_path, image_file)
#             image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#             if image is None:
#                 print(f"Failed to load image: {image_path}")
#                 continue

#             height, width = image.shape
#             max_intensity_points = []

#             for col in range(width):
#                 column_values = image[:, col]
#                 max_row = int(np.argmax(column_values))
#                 max_intensity_points.append((col, max_row))

#             # Extract wavelength from file name (excluding extension)
#             wavelength = os.path.splitext(image_file)[0]

#             # Write header and data
#             writer.writerow([f"distance from origin = {wavelength}"])
#             writer.writerow(["index", "column", "row"])
#             for idx, (col, row) in enumerate(max_intensity_points):
#                 writer.writerow([idx, col, row])

#             writer.writerow([])  # Empty line for separation between images

#     print(f"All data saved to: {output_csv_path}")

# # === CONFIGURATION ===
# input_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"            # Update this
# output_csv_file = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\csv_output.csv"

# process_folder(input_folder, output_csv_file)










# edit 2:












# import os
# import cv2
# import numpy as np
# import csv

# def process_folder(folder_path, output_csv_folder):
#     supported_exts = ('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.bmp')
#     image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
#     image_files.sort()  # Optional: sort by name

#     if not image_files:
#         print("No supported image files found in folder.")
#         return

#     os.makedirs(output_csv_folder, exist_ok=True)

#     for image_file in image_files:
#         image_path = os.path.join(folder_path, image_file)
#         image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#         if image is None:
#             print(f"Failed to load image: {image_path}")
#             continue

#         height, width = image.shape
#         max_intensity_points = []

#         for col in range(width):
#             column_values = image[:, col]
#             max_row = int(np.argmax(column_values))
#             max_intensity_points.append((col, max_row))

#         # Create output CSV file path with same base name
#         base_name = os.path.splitext(image_file)[0]
#         csv_filename = f"{base_name}.csv"
#         csv_path = os.path.join(output_csv_folder, csv_filename)

#         # Write to CSV
#         with open(csv_path, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             writer.writerow([f"distance from origin = {base_name}"])
#             writer.writerow(["index", "column", "row"])
#             for idx, (col, row) in enumerate(max_intensity_points):
#                 writer.writerow([idx, col, row])

#         print(f"Saved: {csv_path}")

# # === CONFIGURATION ===
# input_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"
# output_csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\csv_output"

# process_folder(input_folder, output_csv_folder)










# edit 3:

















import os
import cv2
import numpy as np
import csv

def process_folder(folder_path, output_csv_folder):
    supported_exts = ('.tif', '.tiff', '.png', '.jpg', '.jpeg', '.bmp')
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(supported_exts)]
    image_files.sort()  # Optional: sort by name

    if not image_files:
        print("No supported image files found in folder.")
        return

    os.makedirs(output_csv_folder, exist_ok=True)

    for image_file in image_files:
        image_path = os.path.join(folder_path, image_file)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Failed to load image: {image_path}")
            continue

        height, width = image.shape
        max_intensity_points = []

        for col in range(width):
            column_values = image[:, col]
            max_row = int(np.argmax(column_values))
            max_intensity_points.append((col, max_row))

        # Create output CSV file path with same base name
        base_name = os.path.splitext(image_file)[0]
        csv_filename = f"{base_name}.csv"
        csv_path = os.path.join(output_csv_folder, csv_filename)

        # Write all points to CSV
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([f"distance from origin = {base_name}"])
            writer.writerow(["index", "column", "row"])
            for idx, (col, row) in enumerate(max_intensity_points):
                writer.writerow([idx, col, row])

        print(f"Saved: {csv_path}")

        # === Filter out rows where row == 0 ===
        with open(csv_path, mode='r') as file:
            lines = list(csv.reader(file))

        # First two lines are headers
        headers = lines[:2]
        data_rows = lines[2:]

        # Filter out rows where row == 0
        filtered_rows = [row for row in data_rows if row and row[2].isdigit() and int(row[2]) != 0]

        # Rewrite the CSV file with filtered data
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(headers)
            writer.writerows(filtered_rows)

        print(f"Filtered rows with row == 0 from: {csv_path}")

# === CONFIGURATION ===
input_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid"
output_csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spatial_grid\csv_output"

process_folder(input_folder, output_csv_folder)
