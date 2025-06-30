import cv2
import numpy as np
import tifffile as tiff

# === Configuration ===
img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
screen_res = (1280, 960)

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

# === Get one line input ===
n_lines = 1
fit_lines = []
cumulative_img_display = img_display_orig.copy()

for line_idx in range(n_lines):
    print(f"\n--- Select 3 points for Line {line_idx + 1} ---")
    points_original = []
    img_display = cumulative_img_display.copy()

    def click_event(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            x_orig = int(x * scale_x)
            y_orig = int(y * scale_y)
            points_original.append((x_orig, y_orig))
            cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
            cv2.imshow("Select Points", img_display)

            if len(points_original) == 3:
                # === Fit the line ===
                pts_np = np.array(points_original, dtype=np.float32)
                line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
                vx, vy, x0, y0 = line_params.flatten()
                fit_lines.append((vx, vy, x0, y0))

                # === Draw the line from top to bottom ===
                if vy == 0:
                    print("❌ Cannot draw vertical line: vy=0")
                    return

                y_top = 0
                y_bottom = img.shape[0] - 1

                x_top = int(x0 + (y_top - y0) * (vx / vy))
                x_bottom = int(x0 + (y_bottom - y0) * (vx / vy))

                # Clip to bounds
                x_top = np.clip(x_top, 0, img.shape[1] - 1)
                x_bottom = np.clip(x_bottom, 0, img.shape[1] - 1)

                # Scale to display
                x_top_disp = int(x_top / scale_x)
                y_top_disp = int(y_top / scale_y)
                x_bottom_disp = int(x_bottom / scale_x)
                y_bottom_disp = int(y_bottom / scale_y)

                cv2.line(img_display, (x_top_disp, y_top_disp), (x_bottom_disp, y_bottom_disp), (255, 0, 0), 2)
                cv2.line(cumulative_img_display, (x_top_disp, y_top_disp), (x_bottom_disp, y_bottom_disp), (255, 0, 0), 2)
                cv2.imshow("Select Points", img_display)

    # Show image for point selection
    cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Select Points", img_display)
    cv2.setMouseCallback("Select Points", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# === Create and save black image with blue line ===
line_only_img = np.zeros_like(img)
for fit in fit_lines:
    if fit is None:
        continue
    vx, vy, x0, y0 = fit

    if vy == 0:
        continue

    y_top = 0
    y_bottom = img.shape[0] - 1

    x_top = int(x0 + (y_top - y0) * (vx / vy))
    x_bottom = int(x0 + (y_bottom - y0) * (vx / vy))

    x_top = np.clip(x_top, 0, img.shape[1] - 1)
    x_bottom = np.clip(x_bottom, 0, img.shape[1] - 1)

    cv2.line(line_only_img, (x_top, y_top), (x_bottom, y_bottom), (255, 0, 0), 2)

# Save result
output_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\blue_vertical_line_fitted.png"
success = cv2.imwrite(output_path, line_only_img)
if success:
    print(f"✅ Line image saved to: {output_path}")
else:
    print("❌ Error saving the image.")

# Show output
cv2.imshow("Blue Line Fitted", line_only_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
0