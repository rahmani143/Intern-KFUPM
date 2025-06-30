# import cv2
# import numpy as np
# import os
# import glob

# # Folder containing your TIFF images
# folder_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\mean_images"

# # Find all TIFF files in folder (both .tif and .tiff)
# tiff_files = glob.glob(os.path.join(folder_path, "*.tif")) + glob.glob(os.path.join(folder_path, "*.tiff"))

# for img_path in tiff_files:
#     print(f"Processing {img_path} ...")

#     # Load the image
#     image = cv2.imread(img_path)
#     if image is None:
#         print(f"Failed to load {img_path}. Skipping...")
#         continue

#     # Convert to grayscale
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Threshold to extract white strip (adjust threshold if needed)
#     _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     # Edge detection
#     edges = cv2.Canny(thresh, 50, 150)

#     # Detect lines using Hough Transform
#     lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

#     if lines is not None:
#         # Use the first detected line
#         rho, theta = lines[0][0]
#         angle = np.rad2deg(theta)
#         if angle > 45:
#             angle -= 90  # keep angle between -45 and 45 degrees

#         (h, w) = image.shape[:2]
#         center = (w // 2, h // 2)

#         # Rotation matrix
#         M = cv2.getRotationMatrix2D(center, angle, 1.0)

#         # Rotate image
#         rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)

#         # Save rotated image
#         filename = os.path.basename(img_path)
#         name, ext = os.path.splitext(filename)
#         output_path = os.path.join(folder_path, f"{name}_straightened{ext}")
#         cv2.imwrite(output_path, rotated)
#         print(f"Saved straightened image to: {output_path}")

#     else:
#         print(f"No slanted line detected in {img_path}. Skipping rotation.")











# edit 1:




import cv2
import numpy as np
import os

img_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_spectral_grid.png"

image = cv2.imread(img_path)
if image is None:
    raise ValueError("Image not found or unable to load.")

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Tune these HSV values if needed
lower_blue = np.array([100, 150, 50])
upper_blue = np.array([140, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

kernel = np.ones((3, 3), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

edges = cv2.Canny(mask, 50, 150)

lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

if lines is not None:
    # Optional: average multiple line angles for stability
    angles = []
    for line in lines:
        rho, theta = line[0]
        angle_deg = np.rad2deg(theta)
        if angle_deg > 45:
            angle_deg -= 90
        angles.append(angle_deg)
    avg_angle = np.mean(angles)

    print(f"Average detected angle: {avg_angle:.2f} degrees")

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, avg_angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)

    folder = os.path.dirname(img_path)
    filename = os.path.basename(img_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(folder, f"{name}_straightened{ext}")
    cv2.imwrite(output_path, rotated)

    print(f"Saved straightened image to: {output_path}")
else:
    print("No blue slanted line detected.")
