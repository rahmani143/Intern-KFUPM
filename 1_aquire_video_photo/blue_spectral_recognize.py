import cv2
import numpy as np
import matplotlib.pyplot as plt

# Path to your image
img_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_spectral_grid.png"

# Your wavelengths from top to bottom (13 lines)
wavelengths = [
    410, 460, 510, 560, 610, 660, 710,
    760, 800, 860, 910, 960, 1000
]

# Load image
img = cv2.imread(img_path)
if img is None:
    raise FileNotFoundError(f"Cannot load image from {img_path}")

# Resize image for easier viewing (optional, comment if you want full res)
scale_percent = 50  # percent of original size, adjust if needed
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

print("INSTRUCTION:")
print("Click on a pixel in the image window to print its HSV values.")
print("Close the window when done inspecting.")

# Mouse callback for HSV inspection
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = hsv[y, x]
        print(f"HSV at ({x},{y}): {pixel}")

cv2.imshow("Image for HSV inspection", img)
cv2.setMouseCallback("Image for HSV inspection", mouse_callback)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Now set your blue range here after inspection or try defaults:
# (You can modify these based on printed HSV values from inspection)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([140, 255, 255])

# Create mask for blue regions
mask = cv2.inRange(hsv, lower_blue, upper_blue)
cv2.imshow("Blue Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save mask for debug if needed
cv2.imwrite("debug_mask.png", mask)

# Edge detection
edges = cv2.Canny(mask, 50, 150, apertureSize=3)
cv2.imshow("Edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("debug_edges.png", edges)

# Detect lines with Probabilistic Hough Transform
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,        # Lower threshold for more sensitive detection
    minLineLength=50,    # Lowered minimum length to detect smaller lines
    maxLineGap=20        # Max gap between segments to link as one line
)

if lines is None or len(lines) == 0:
    print("No lines detected!")
    exit()

print(f"Detected {len(lines)} lines.")

# Draw detected lines on a copy of the image
img_lines = img.copy()
for idx, line in enumerate(lines):
    x1, y1, x2, y2 = line[0]
    cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Detected Lines", img_lines)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite("debug_detected_lines.png", img_lines)

# Sort lines by their vertical position (average y)
lines_sorted = sorted(lines, key=lambda l: (l[0][1] + l[0][3]) / 2)

# If more than 13 lines detected, try to select the 13 most spaced or use clustering,
# but here we will just take 13 closest to top (assuming image top to bottom order)
lines_selected = lines_sorted[:13]

# Plot lines with wavelength labels using matplotlib
plt.figure(figsize=(10, 10))
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Detected Blue Lines with Wavelengths")

for i, line in enumerate(lines_selected):
    x1, y1, x2, y2 = line[0]
    avg_y = (y1 + y2) / 2
    avg_x = (x1 + x2) / 2
    plt.plot([x1, x2], [y1, y2], color='lime', linewidth=2)
    if i < len(wavelengths):
        plt.text(avg_x + 10, avg_y, f"{wavelengths[i]} nm", color='yellow', fontsize=12, weight='bold')

plt.gca().invert_yaxis()  # Match image coordinate system
plt.show()
