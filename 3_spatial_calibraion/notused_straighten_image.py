import cv2
import numpy as np
import os

# Path to the original image
img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_filtered_lines_debug.png" # <-- Replace with your actual image path

# Load the image
image = cv2.imread(img_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold to extract white strip
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

# Edge detection
edges = cv2.Canny(thresh, 50, 150)

# Detect lines using Hough Transform
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

if lines is not None:
    rho, theta = lines[0][0]
    angle = np.rad2deg(theta)
    if angle > 45:
        angle -= 90  # keep angle between -45 and 45 degrees

    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_LINEAR)

    # Save rotated image
    folder = os.path.dirname(img_path)
    filename = os.path.basename(img_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(folder, f"{name}_straightened{ext}")
    cv2.imwrite(output_path, rotated)

    print(f"Saved straightened image to: {output_path}")
else:
    print("No slanted line detected.")
