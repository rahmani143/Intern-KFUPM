# import cv2
# import numpy as np
# import math

# def detect_blue_line_angle_and_coords(image_path):
#     # Load image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Image not found or unable to load: {image_path}")

#     # Convert to HSV color space
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define blue color range in HSV (adjust if needed)
#     lower_blue = np.array([100, 150, 50])
#     upper_blue = np.array([140, 255, 255])

#     # Create mask for blue regions
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Morphological clean up
#     kernel = np.ones((3, 3), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#     # Edge detection
#     edges = cv2.Canny(mask, 50, 150)

#     # Use probabilistic Hough Line Transform to get line segments with endpoints
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

#     if lines is None:
#         print("No blue lines detected.")
#         return None

#     # Find the longest line (most prominent)
#     longest_line = None
#     max_length = 0
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         length = math.hypot(x2 - x1, y2 - y1)
#         if length > max_length:
#             max_length = length
#             longest_line = (x1, y1, x2, y2)

#     x1, y1, x2, y2 = longest_line

#     # Calculate angle in degrees (-90 to 90)
#     angle_rad = math.atan2(y2 - y1, x2 - x1)
#     angle_deg = np.degrees(angle_rad)

#     # Normalize angle to [-90, 90]
#     if angle_deg > 90:
#         angle_deg -= 180
#     elif angle_deg < -90:
#         angle_deg += 180

#     print(f"Detected blue line angle: {angle_deg:.2f} degrees")
#     print(f"Line start coordinate: ({x1}, {y1})")
#     print(f"Line end coordinate: ({x2}, {y2})")

#     return angle_deg, (x1, y1), (x2, y2)

# # Example usage
# image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_910.png"
# detect_blue_line_angle_and_coords(image_path)








# edit 1:







# import cv2
# import numpy as np
# import math

# def detect_blue_line_angle_and_coords(image_path):
#     # Load image
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Image not found or unable to load: {image_path}")

#     output_image = image.copy()

#     # Convert to HSV color space
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Define blue color range in HSV
#     lower_blue = np.array([100, 150, 50])
#     upper_blue = np.array([140, 255, 255])

#     # Create mask for blue regions
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Morphological operations
#     kernel = np.ones((3, 3), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#     # Edge detection
#     edges = cv2.Canny(mask, 50, 150)

#     # Hough Line detection
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=10)

#     if lines is None:
#         print("No blue lines detected.")
#         return None

#     # Find the longest line
#     longest_line = None
#     max_length = 0
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         length = math.hypot(x2 - x1, y2 - y1)
#         if length > max_length:
#             max_length = length
#             longest_line = (x1, y1, x2, y2)

#     x1, y1, x2, y2 = longest_line

#     # Draw the detected blue line in red
#     cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

#     # Show fullscreen image window
#     cv2.namedWindow("Detected Line", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Detected Line", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Detected Line", output_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Save image
#     save_path = image_path.replace(".png", "_line_visualized.png")
#     cv2.imwrite(save_path, output_image)
#     print(f"Saved visualized image to: {save_path}")

#     # Calculate angle
#     angle_rad = math.atan2(y2 - y1, x2 - x1)
#     angle_deg = np.degrees(angle_rad)

#     # Normalize to [-90, 90]
#     if angle_deg > 90:
#         angle_deg -= 180
#     elif angle_deg < -90:
#         angle_deg += 180

#     print(f"Detected blue line angle: {angle_deg:.2f} degrees")
#     print(f"Line start coordinate: ({x1}, {y1})")
#     print(f"Line end coordinate: ({x2}, {y2})")

#     return angle_deg, (x1, y1), (x2, y2)

# # Example usage
# image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_910.png"
# detect_blue_line_angle_and_coords(image_path)










# edit 2:









# import cv2
# import numpy as np
# import math
# import os

# def detect_blue_line_full(image_path):
#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to read the image: {image_path}")

#     output_image = image.copy()
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Blue color mask
#     lower_blue = np.array([100, 150, 50])
#     upper_blue = np.array([140, 255, 255])
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Morphological cleanup
#     kernel = np.ones((3, 3), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#     # Edge detection
#     edges = cv2.Canny(mask, 50, 150)

#     # Detect lines
#     lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=50, minLineLength=100, maxLineGap=20)
#     if lines is None:
#         print("❌ No blue lines detected.")
#         return

#     # Find the longest line
#     longest_line = max(lines, key=lambda line: np.hypot(line[0][2] - line[0][0], line[0][3] - line[0][1]))
#     x1, y1, x2, y2 = longest_line[0]

#     # Calculate angle
#     angle_rad = math.atan2(y2 - y1, x2 - x1)
#     angle_deg = np.degrees(angle_rad)
#     angle_deg = (angle_deg + 180) % 180 - 90  # Normalize to [-90, 90]

#     print(f"✅ Angle: {angle_deg:.2f} degrees")
#     print(f"✅ Line segment: Start=({x1},{y1}), End=({x2},{y2})")

#     # Extend line across full width
#     h, w = image.shape[:2]
#     slope = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')

#     if slope == float('inf'):
#         x_full1 = x_full2 = x1
#         y_full1 = 0
#         y_full2 = h
#     else:
#         intercept = y1 - slope * x1
#         x_full1 = 0
#         y_full1 = int(slope * x_full1 + intercept)
#         x_full2 = w - 1
#         y_full2 = int(slope * x_full2 + intercept)

#     # Draw red full line
#     cv2.line(output_image, (x_full1, y_full1), (x_full2, y_full2), (0, 0, 255), 2)

#     # Safe display
#     window_name = "Detected Full Line"
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(window_name, min(w, 1920), min(h, 1080))  # Safe window size
#     cv2.imshow(window_name, output_image)
#     print("👁️  Press any key in the window to close...")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Save
#     save_path = image_path.replace(".png", "_full_line.png")
#     cv2.imwrite(save_path, output_image)
#     print(f"💾 Saved visualized image to: {save_path}")

#     return angle_deg, (x_full1, y_full1), (x_full2, y_full2)

# # --- Example usage ---
# image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_910.png"
# detect_blue_line_full(image_path)











# edit 3:











# import cv2
# import numpy as np
# import math
# import os

# def detect_blue_line_via_regression(image_path):
#     if not os.path.exists(image_path):
#         raise FileNotFoundError(f"Image not found: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to read the image: {image_path}")

#     output_image = image.copy()
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Blue mask
#     lower_blue = np.array([100, 150, 50])
#     upper_blue = np.array([140, 255, 255])
#     mask = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Clean mask
#     kernel = np.ones((3, 3), np.uint8)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
#     mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

#     # === DEBUG: Show mask ===
    
#     cv2.namedWindow("Blue Mask", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Blue Mask", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Blue Mask", mask)
#     cv2.waitKey(0)
#     cv2.destroyWindow("Blue Mask")

#     # Get coordinates of blue pixels
#     ys, xs = np.where(mask > 0)
#     if len(xs) < 2:
#         print("❌ Not enough blue pixels for line fitting.")
#         return

#     # Fit line: y = mx + c
#     coeffs = np.polyfit(xs, ys, 1)  # degree 1 line
#     slope, intercept = coeffs

#     # Calculate angle
#     angle_rad = math.atan(slope)
#     angle_deg = np.degrees(angle_rad)
#     angle_deg = (angle_deg + 180) % 180 - 90  # Normalize to [-90, 90]

#     print(f"✅ Best-fit blue line angle: {angle_deg:.2f} degrees")
#     print(f"✅ Line equation: y = {slope:.3f}x + {intercept:.1f}")

#     # Draw line across full width
#     h, w = image.shape[:2]
#     x1 = 0
#     y1 = int(slope * x1 + intercept)
#     x2 = w - 1
#     y2 = int(slope * x2 + intercept)

#     # Clamp Y values to image bounds
#     y1 = np.clip(y1, 0, h - 1)
#     y2 = np.clip(y2, 0, h - 1)

#     cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

#     # Show result
#     window_name = "Detected Blue Line (Best Fit)"
#     cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#     cv2.resizeWindow(window_name, min(w, 1920), min(h, 1080))
#     cv2.imshow(window_name, output_image)
#     print("👁️  Press any key to close windows.")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     # Save image
#     save_path = image_path.replace(".png", "_regression_line.png")
#     cv2.imwrite(save_path, output_image)
#     print(f"💾 Saved visualized image to: {save_path}")

#     return angle_deg, (x1, y1), (x2, y2)

# # --- Run it ---
# image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_910.png"
# detect_blue_line_via_regression(image_path)










# edit 4:











import cv2
import numpy as np
import math
import os

def detect_blue_line_via_regression(image_path):
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to read the image: {image_path}")

    output_image = image.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Blue mask
    lower_blue = np.array([100, 150, 50])
    upper_blue = np.array([140, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Clean mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Show mask fullscreen
    cv2.namedWindow("Blue Mask", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Blue Mask", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Blue Mask", mask)
    cv2.waitKey(0)
    cv2.destroyWindow("Blue Mask")

    # Get coordinates of blue pixels
    ys, xs = np.where(mask > 0)
    if len(xs) < 2:
        print("❌ Not enough blue pixels for line fitting.")
        return

    # Fit line: y = mx + c
    coeffs = np.polyfit(xs, ys, 1)
    slope, intercept = coeffs

    # Calculate angle
    angle_rad = math.atan(slope)
    angle_deg = np.degrees(angle_rad)
    angle_deg = (angle_deg + 180) % 180 - 90

    print(f"✅ Best-fit blue line angle: {angle_deg:.2f} degrees")
    print(f"✅ Line equation: y = {slope:.3f}x + {intercept:.1f}")

    # Define full-width line
    h, w = image.shape[:2]
    x1, x2 = 0, w - 1
    y1 = int(slope * x1 + intercept)
    y2 = int(slope * x2 + intercept)
    y1 = np.clip(y1, 0, h - 1)
    y2 = np.clip(y2, 0, h - 1)

    # Draw the main red line
    cv2.line(output_image, (x1, y1), (x2, y2), (0, 0, 255), 2)

    # === Draw parallel lines ===
    num_above = int(input("🔼 How many lines above? "))
    num_below = int(input("🔽 How many lines below? "))
    spacing = int(input("📏 Pixel spacing between lines: "))

    # Get direction vector and perpendicular
    dx = x2 - x1
    dy = y2 - y1
    line_len = math.hypot(dx, dy)
    perp_dx = -dy / line_len
    perp_dy = dx / line_len

    for i in range(1, num_above + 1):
        offset_x = int(perp_dx * spacing * i)
        offset_y = int(perp_dy * spacing * i)
        pt1 = (x1 + offset_x, y1 + offset_y)
        pt2 = (x2 + offset_x, y2 + offset_y)
        cv2.line(output_image, pt1, pt2, (0, 255, 0), 1)

    for i in range(1, num_below + 1):
        offset_x = int(-perp_dx * spacing * i)
        offset_y = int(-perp_dy * spacing * i)
        pt1 = (x1 + offset_x, y1 + offset_y)
        pt2 = (x2 + offset_x, y2 + offset_y)
        cv2.line(output_image, pt1, pt2, (0, 255, 0), 1)

    # Show final result fullscreen
    window_name = "Grid Overlay"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow(window_name, output_image)
    print("👁️  Press any key to close the grid overlay window.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save the final image
    save_path = image_path.replace(".png", "_grid_overlay.png")
    cv2.imwrite(save_path, output_image)
    print(f"💾 Saved grid image to: {save_path}")

    return angle_deg, (x1, y1), (x2, y2)

# --- Run the function ---
image_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\blue_horizontal_lines_760.png"
detect_blue_line_via_regression(image_path)
