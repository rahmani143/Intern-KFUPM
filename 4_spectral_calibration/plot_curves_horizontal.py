import cv2
import numpy as np
import tifffile as tiff

# === Configuration ===
img_path = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\mean_images\combined_white_regions.tif"
screen_res = (1280, 960)
real_world_spacing_cm = 0.4  # known spacing in cm

# === Load Image ===
if img_path.lower().endswith(('.tiff', '.tif')):
    img = tiff.imread(img_path)
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    elif img.ndim == 3 and img.shape[2] > 3:
        img = img[:, :, :3]
else:
    img = cv2.imread(img_path)

if img is None:
    raise ValueError("Image could not be loaded. Check the path.")

# === Calculate scale factors for display ===
scale_x = screen_res[0] / img.shape[1]
scale_y = screen_res[1] / img.shape[0]
scale = min(scale_x, scale_y)
display_w = int(img.shape[1] * scale)
display_h = int(img.shape[0] * scale)
img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# Inverse scale to convert display coords back to original image coords
scale_x = img.shape[1] / display_w
scale_y = img.shape[0] / display_h

# Show original resized image fullscreen for reference
cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("Original Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
cv2.imshow("Original Image", img_display_orig)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ask user how many lines to fit
n_lines = int(input("Enter number of lines to fit: "))

all_points = []
fit_lines = []
polynomials = []
cumulative_img_display = img_display_orig.copy()

for line_idx in range(n_lines):
    print(f"\n--- Select 3+ points for Line {line_idx + 1} ---")
    points_scaled = []
    points_original = []
    img_display = cumulative_img_display.copy()

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x_orig = int(x * scale_x)
            y_orig = int(y * scale_y)
            points_scaled.append((x, y))
            points_original.append((x_orig, y_orig))
            cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("Select Points", img_display)

            if len(points_original) == 3:
                # Fit line
                pts_np = np.array(points_original, dtype=np.float32)
                line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
                vx, vy, x0, y0 = line_params.flatten()
                fit_lines.append((vx, vy, x0, y0))

                # Horizontal extension: left to right
                x1 = 0
                x2 = img.shape[1] - 1
                slope = vy / vx if vx != 0 else 1e-5
                y1 = int(slope * (x1 - x0) + y0)
                y2 = int(slope * (x2 - x0) + y0)

                # Convert to display coords
                x1_disp = int(x1 / scale_x)
                y1_disp = int(y1 / scale_y)
                x2_disp = int(x2 / scale_x)
                y2_disp = int(y2 / scale_y)

                cv2.line(img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)
                cv2.line(cumulative_img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)
                cv2.imshow("Select Points", img_display)

    cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Select Points", img_display)
    cv2.setMouseCallback("Select Points", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    if len(points_original) < 3:
        print("❌ Need at least 3 points. Skipping.")
        fit_lines.append(None)
        polynomials.append(None)
        continue

    all_points.append(points_original)

    # Polynomial fit
    pts_np = np.array(points_original)
    x_pts = pts_np[:, 0]
    y_pts = pts_np[:, 1]
    poly_coeffs = np.polyfit(x_pts, y_pts, deg=2)
    polynomials.append(poly_coeffs)
    print(f"Polynomial coefficients for line {line_idx + 1}: {poly_coeffs}")

# === Distance Calculations ===
print("\n=== Calculating Spacing Between Lines (cv2.fitLine) ===")
distances_pixels = []
distances_mm = []

valid_fit_lines = [f for f in fit_lines if f is not None]

if len(valid_fit_lines) >= 2:
    for i in range(len(valid_fit_lines) - 1):
        vx1, vy1, x01, y01 = valid_fit_lines[i]
        vx2, vy2, x02, y02 = valid_fit_lines[i + 1]

        base_vec = np.array([x01 - x02, y01 - y02])
        norm_vec = np.array([-vy2, vx2])
        norm_vec = norm_vec / np.linalg.norm(norm_vec)

        dist = np.abs(np.dot(base_vec, norm_vec))
        distances_pixels.append(dist)

    avg_pixel_dist = np.mean(distances_pixels)
    cm_per_pixel = real_world_spacing_cm / avg_pixel_dist
    mm_per_pixel = cm_per_pixel * 10
    distances_mm = [d * mm_per_pixel for d in distances_pixels]

    print(f"\nAverage pixel distance: {avg_pixel_dist:.2f} px")
    print(f"Estimated cm/pixel: {cm_per_pixel:.4f} cm/px")
    print(f"Estimated mm/pixel: {mm_per_pixel:.4f} mm/px")
    print("Individual distances (mm):")
    for idx, d_mm in enumerate(distances_mm, 1):
        print(f"  Between line {idx} and {idx+1}: {d_mm:.2f} mm")
else:
    print("Not enough valid lines to compute distances.")

# === Polynomial Intersections with Bottom Line ===
print("\n=== Polynomial Intersections with Bottom Line (y = bottom_y) ===")

bottom_y = img.shape[0] - 1
img_width = img.shape[1]

for idx, poly in enumerate(polynomials, start=1):
    if poly is None:
        print(f"Line {idx}: No polynomial fitted (less than 3 points).")
        continue

    a, b, c = poly
    coeffs = [a, b, c - bottom_y]
    roots = np.roots(coeffs)
    real_roots = [r.real for r in roots if np.isreal(r) and 0 <= r.real <= img_width - 1]

    if real_roots:
        real_roots_mm = [x_px * mm_per_pixel for x_px in real_roots]
        pixels_str = ", ".join(f"{float(x):.4f}" for x in real_roots)
        mm_str = ", ".join(f"{float(x):.4f}" for x in real_roots_mm)
        print(f"Line {idx}: Intersection x-coordinates at bottom line (pixels): {pixels_str}")
        print(f"Line {idx}: Intersection x-coordinates at bottom line (mm): {mm_str}")
    else:
        print(f"Line {idx}: No real intersection with bottom line within image width.")

# === Draw blue fitted lines on a black background ===
print("\n=== Generating black image with blue fitted lines ===")
line_only_img = np.zeros_like(img)
blue_color = (255, 0, 0)

for fit in fit_lines:
    if fit is None:
        continue
    vx, vy, x0, y0 = fit
    x1 = 0
    x2 = img.shape[1] - 1
    slope = vy / vx if vx != 0 else 1e-5
    y1 = int(slope * (x1 - x0) + y0)
    y2 = int(slope * (x2 - x0) + y0)

    x1 = np.clip(x1, 0, img.shape[1] - 1)
    x2 = np.clip(x2, 0, img.shape[1] - 1)
    y1 = np.clip(y1, 0, img.shape[0] - 1)
    y2 = np.clip(y2, 0, img.shape[0] - 1)

    cv2.line(line_only_img, (x1, y1), (x2, y2), blue_color, 2)

# Save output
output_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\blue_horizontal_lines_910.png"
success = cv2.imwrite(output_path, line_only_img)
if success:
    print(f"File saved successfully at {output_path}")
else:
    print("Error saving the blue lines image!")

# Show saved image
cv2.imshow("Blue Lines Only", line_only_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
