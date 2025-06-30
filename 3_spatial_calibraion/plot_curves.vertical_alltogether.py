# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"  # 🔁 Change to your actual path
# screen_res = (1280, 960)  # Display size for image window

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# # Resize for display window (maintain aspect ratio)
# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display = cv2.resize(img.copy(), (display_w, display_h))

# # Scaling factors to map back to original
# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# # === Point selection ===
# points_scaled = []
# points_original = []

# def click_event(event, x, y, flags, param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         x_orig = int(x * scale_x)
#         y_orig = int(y * scale_y)
#         points_scaled.append((x, y))
#         points_original.append((x_orig, y_orig))
#         cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#         cv2.imshow("Select Points", img_display)

# cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
# cv2.imshow("Select Points", img_display)
# cv2.setMouseCallback("Select Points", click_event)

# print("Click on points to fit a curve. Press any key when done.")
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Print original coordinates
# for i, (x, y) in enumerate(points_original):
#     print(f"Point {i+1}: Original Image Coords = ({x}, {y})")

# if len(points_original) < 3:
#     print("❌ Need at least 3 points to fit a curve.")
#     exit()

# # === Polynomial Fitting ===
# x_coords = np.array([pt[0] for pt in points_original])
# y_coords = np.array([pt[1] for pt in points_original])

# min_error = float('inf')
# best_degree = 1
# best_poly = None

# for degree in range(1, min(10, len(x_coords))):
#     coeffs = np.polyfit(x_coords, y_coords, degree)
#     poly = np.poly1d(coeffs)
#     y_pred = poly(x_coords)
#     error = mean_squared_error(y_coords, y_pred)
#     if error < min_error:
#         min_error = error
#         best_degree = degree
#         best_poly = poly

# print(f"\n✅ Best polynomial degree: {best_degree}")
# print(f"   Polynomial coefficients: {best_poly.coefficients}\n")

# # === Plot Result ===
# x_line = np.linspace(min(x_coords), max(x_coords), 500)
# y_line = best_poly(x_line)

# plt.figure(figsize=(10, 8))
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), origin='upper')  # ✅ Correct orientation
# plt.plot(x_coords, y_coords, 'ro', label='Selected Points')
# plt.plot(x_line, y_line, 'b-', label=f'Best Fit (deg={best_degree})')
# plt.title("Best Polynomial Fit")
# plt.legend()
# plt.show()


# move to part 2:


# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)  # Adjust your display resolution here

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# # Resize image to fit screen_res while keeping aspect ratio
# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# # Scaling factors to map displayed image coords back to original image coords
# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# # Get number of lines to fit
# n_lines = int(input("Enter number of lines to fit: "))

# all_lines_points_original = []
# all_polynomials = []

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []

#     # Copy resized image fresh for this line's selection
#     img_display = img_display_orig.copy()

#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
#     cv2.imshow("Select Points", img_display)
#     cv2.setMouseCallback("Select Points", click_event)

#     print("Click points for this line. Press any key when done.")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 3:
#         print("❌ Need at least 3 points to fit a curve. Skipping this line.")
#         all_lines_points_original.append(points_original)
#         all_polynomials.append(None)
#         continue

#     x_coords = np.array([pt[0] for pt in points_original])
#     y_coords = np.array([pt[1] for pt in points_original])

#     # Find best polynomial fit degree with minimal MSE
#     min_error = float('inf')
#     best_degree = 1
#     best_poly = None

#     max_degree = min(10, len(x_coords))  # Degree can't exceed points count
#     for degree in range(1, max_degree):
#         coeffs = np.polyfit(x_coords, y_coords, degree)
#         poly = np.poly1d(coeffs)
#         y_pred = poly(x_coords)
#         error = mean_squared_error(y_coords, y_pred)
#         if error < min_error:
#             min_error = error
#             best_degree = degree
#             best_poly = poly

#     print(f"Line {line_idx + 1} best polynomial degree: {best_degree}")
#     print(f"Polynomial coefficients: {best_poly.coefficients}")

#     all_lines_points_original.append(points_original)
#     all_polynomials.append(best_poly)

#     # Show polynomial fit on resized image
#     img_fit_display = img_display_orig.copy()
#     # Draw selected points
#     for (x_p, y_p) in points_original:
#         x_disp = int(x_p / scale_x)
#         y_disp = int(y_p / scale_y)
#         cv2.circle(img_fit_display, (x_disp, y_disp), 3, (0, 0, 255), -1)

#     # Draw polynomial curve points on resized image
#     x_line = np.linspace(min(x_coords), max(x_coords), 500)
#     y_line = best_poly(x_line)
#     for xi, yi in zip(x_line.astype(int), y_line.astype(int)):
#         x_disp = int(xi / scale_x)
#         y_disp = int(yi / scale_y)
#         if 0 <= x_disp < img_fit_display.shape[1] and 0 <= y_disp < img_fit_display.shape[0]:
#             img_fit_display[y_disp, x_disp] = (255, 0, 0)  # Blue point

#     cv2.namedWindow(f"Line {line_idx + 1} Fit - Press any key", cv2.WINDOW_NORMAL)
#     cv2.imshow(f"Line {line_idx + 1} Fit - Press any key", img_fit_display)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # === After all lines selected, plot summary with matplotlib ===
# plt.figure(figsize=(12, 10))
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), origin='upper')

# colors = plt.cm.get_cmap('tab10', n_lines)

# for idx, (points, poly) in enumerate(zip(all_lines_points_original, all_polynomials)):
#     if poly is None or len(points) == 0:
#         continue
#     x_pts = np.array([p[0] for p in points])
#     y_pts = np.array([p[1] for p in points])
#     plt.plot(x_pts, y_pts, 'o', color=colors(idx), label=f'Line {idx + 1} Points')

#     x_line = np.linspace(min(x_pts), max(x_pts), 500)
#     y_line = poly(x_line)
#     plt.plot(x_line, y_line, '-', color=colors(idx), label=f'Line {idx + 1} Fit (deg={poly.order})')

# plt.title(f'Polynomial Fits for {n_lines} Lines')
# plt.legend()
# plt.show()


# move to part3:

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# # Resize image to fit display while maintaining aspect ratio
# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# # Scaling factors (displayed -> original)
# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# # Show original image before asking number of lines
# win_name = "Original Image - Press any key to continue"
# cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
# cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.imshow(win_name, img_display_orig)
# print("Showing original image. Press any key on the image window to continue.")
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# n_lines = int(input("Enter number of lines to fit: "))

# all_lines_points_original = []
# all_polynomials = []

# # cumulative image to draw all lines on (resized)
# cumulative_img_display = img_display_orig.copy()

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []

#     # Start selection on the cumulative image with previous lines drawn
#     img_display = cumulative_img_display.copy()

#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     win_name = "Select Points"
#     cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty(win_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow(win_name, img_display)
#     cv2.setMouseCallback(win_name, click_event)

#     print("Click points for this line. Press any key when done.")
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 3:
#         print("❌ Need at least 3 points to fit a curve. Skipping this line.")
#         all_lines_points_original.append(points_original)
#         all_polynomials.append(None)
#         continue

#     x_coords = np.array([pt[0] for pt in points_original])
#     y_coords = np.array([pt[1] for pt in points_original])

#     min_error = float('inf')
#     best_degree = 1
#     best_poly = None
#     max_degree = min(10, len(x_coords))
#     for degree in range(1, max_degree):
#         coeffs = np.polyfit(x_coords, y_coords, degree)
#         poly = np.poly1d(coeffs)
#         y_pred = poly(x_coords)
#         error = mean_squared_error(y_coords, y_pred)
#         if error < min_error:
#             min_error = error
#             best_degree = degree
#             best_poly = poly

#     print(f"Line {line_idx + 1} best polynomial degree: {best_degree}")
#     print(f"Polynomial coefficients: {best_poly.coefficients}")

#     all_lines_points_original.append(points_original)
#     all_polynomials.append(best_poly)

#     # Update cumulative_img_display by drawing current line's points and polynomial on it
#     for (x_p, y_p) in points_original:
#         x_disp = int(x_p / scale_x)
#         y_disp = int(y_p / scale_y)
#         cv2.circle(cumulative_img_display, (x_disp, y_disp), 3, (0, 0, 255), -1)

#     x_line = np.linspace(min(x_coords), max(x_coords), 500)
#     y_line = best_poly(x_line)
#     for xi, yi in zip(x_line.astype(int), y_line.astype(int)):
#         x_disp = int(xi / scale_x)
#         y_disp = int(yi / scale_y)
#         if 0 <= x_disp < cumulative_img_display.shape[1] and 0 <= y_disp < cumulative_img_display.shape[0]:
#             cumulative_img_display[y_disp, x_disp] = (255, 0, 0)

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # After all lines drawn, show final matplotlib plot
# plt.figure(figsize=(12, 10))
# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), origin='upper')

# colors = plt.cm.get_cmap('tab10', n_lines)

# for idx, (points, poly) in enumerate(zip(all_lines_points_original, all_polynomials)):
#     if poly is None or len(points) == 0:
#         continue
#     x_pts = np.array([p[0] for p in points])
#     y_pts = np.array([p[1] for p in points])
#     plt.plot(x_pts, y_pts, 'o', color=colors(idx), label=f'Line {idx + 1} Points')

#     x_line = np.linspace(min(x_pts), max(x_pts), 500)
#     y_line = poly(x_line)
#     plt.plot(x_line, y_line, '-', color=colors(idx), label=f'Line {idx + 1} Fit (deg={poly.order})')

# plt.title(f'Polynomial Fits for {n_lines} Lines')
# plt.legend()
# plt.show()


# edit 4:

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)
# real_world_spacing_cm = 0.4  # known spacing in cm

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Original Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.imshow("Original Image", img_display_orig)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# n_lines = int(input("Enter number of lines to fit: "))
# all_points = []
# fit_lines = []
# cumulative_img_display = img_display_orig.copy()

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []
#     img_display = cumulative_img_display.copy()

#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Select Points", img_display)
#     cv2.setMouseCallback("Select Points", click_event)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 2:
#         print("❌ Need at least 2 points to fit a line. Skipping this one.")
#         continue

#     all_points.append(points_original)
#     pts_np = np.array(points_original, dtype=np.float32)
#     line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
#     vx, vy, x0, y0 = line_params.flatten()
#     fit_lines.append((vx, vy, x0, y0))

#     # Draw line over extended image width
#     line_length = max(img.shape[1], img.shape[0])
#     x1 = int(x0 - vx * line_length)
#     y1 = int(y0 - vy * line_length)
#     x2 = int(x0 + vx * line_length)
#     y2 = int(y0 + vy * line_length)

#     x1_disp = int(x1 / scale_x)
#     y1_disp = int(y1 / scale_y)
#     x2_disp = int(x2 / scale_x)
#     y2_disp = int(y2 / scale_y)

#     cv2.line(cumulative_img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # === Distance Calculations ===
# print("\n=== Calculating Spacing Between Lines (cv2.fitLine) ===")
# distances_pixels = []
# distances_mm = []

# if len(fit_lines) >= 2:
#     for i in range(len(fit_lines) - 1):
#         vx1, vy1, x01, y01 = fit_lines[i]
#         vx2, vy2, x02, y02 = fit_lines[i + 1]

#         vec = np.array([vx2, vy2])
#         base_vec = np.array([x01 - x02, y01 - y02])
#         norm_vec = np.array([-vy2, vx2])
#         norm_vec = norm_vec / np.linalg.norm(norm_vec)

#         dist = np.abs(np.dot(base_vec, norm_vec))
#         distances_pixels.append(dist)

#     avg_pixel_dist = np.mean(distances_pixels)
#     cm_per_pixel = real_world_spacing_cm / avg_pixel_dist
#     mm_per_pixel = cm_per_pixel * 10
#     distances_mm = [d * mm_per_pixel for d in distances_pixels]

#     print(f"\nAverage pixel distance: {avg_pixel_dist:.2f} px")
#     print(f"Estimated cm/pixel: {cm_per_pixel:.4f} cm/px")
#     print(f"Estimated mm/pixel: {mm_per_pixel:.4f} mm/px")
#     print("Individual distances (mm):")
#     for idx, d_mm in enumerate(distances_mm, 1):
#         print(f"  Between line {idx} and {idx+1}: {d_mm:.2f} mm")
# else:
#     print("Not enough valid lines to compute distances.")


# edit 5:


# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from sklearn.metrics import mean_squared_error
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)
# real_world_spacing_cm = 0.4  # known spacing in cm

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Original Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.imshow("Original Image", img_display_orig)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# n_lines = int(input("Enter number of lines to fit: "))
# all_points = []
# fit_lines = []
# cumulative_img_display = img_display_orig.copy()

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []
#     img_display = cumulative_img_display.copy()

#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Select Points", img_display)
#     cv2.setMouseCallback("Select Points", click_event)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 2:
#         print("❌ Need at least 2 points to fit a line. Skipping this one.")
#         continue

#     all_points.append(points_original)
#     pts_np = np.array(points_original, dtype=np.float32)
#     line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
#     vx, vy, x0, y0 = line_params.flatten()
#     fit_lines.append((vx, vy, x0, y0))

#     # Draw line over extended image width
#     line_length = max(img.shape[1], img.shape[0])
#     x1 = int(x0 - vx * line_length)
#     y1 = int(y0 - vy * line_length)
#     x2 = int(x0 + vx * line_length)
#     y2 = int(y0 + vy * line_length)

#     x1_disp = int(x1 / scale_x)
#     y1_disp = int(y1 / scale_y)
#     x2_disp = int(x2 / scale_x)
#     y2_disp = int(y2 / scale_y)

#     cv2.line(cumulative_img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # === Distance Calculations ===
# print("\n=== Calculating Spacing Between Lines (cv2.fitLine) ===")
# distances_pixels = []
# distances_mm = []

# if len(fit_lines) >= 2:
#     for i in range(len(fit_lines) - 1):
#         vx1, vy1, x01, y01 = fit_lines[i]
#         vx2, vy2, x02, y02 = fit_lines[i + 1]

#         vec = np.array([vx2, vy2])
#         base_vec = np.array([x01 - x02, y01 - y02])
#         norm_vec = np.array([-vy2, vx2])
#         norm_vec = norm_vec / np.linalg.norm(norm_vec)

#         dist = np.abs(np.dot(base_vec, norm_vec))
#         distances_pixels.append(dist)

#     avg_pixel_dist = np.mean(distances_pixels)
#     cm_per_pixel = real_world_spacing_cm / avg_pixel_dist
#     mm_per_pixel = cm_per_pixel * 10
#     distances_mm = [d * mm_per_pixel for d in distances_pixels]

#     print(f"\nAverage pixel distance: {avg_pixel_dist:.2f} px")
#     print(f"Estimated cm/pixel: {cm_per_pixel:.4f} cm/px")
#     print(f"Estimated mm/pixel: {mm_per_pixel:.4f} mm/px")
#     print("Individual distances (mm):")
#     for idx, d_mm in enumerate(distances_mm, 1):
#         print(f"  Between line {idx} and {idx+1}: {d_mm:.2f} mm")
# else:
#     print("Not enough valid lines to compute distances.")


# edit 6:


# import cv2
# import numpy as np
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)
# real_world_spacing_cm = 0.4  # known spacing in cm

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# # === Calculate scale factors for display ===
# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# # Inverse scale to convert display coords back to original image coords
# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# # Show original resized image fullscreen for reference
# cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Original Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.imshow("Original Image", img_display_orig)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Ask user how many lines to fit
# n_lines = int(input("Enter number of lines to fit: "))

# all_points = []     # store points of each line (in original image coords)
# fit_lines = []      # store fitted line parameters (vx, vy, x0, y0)
# polynomials = []    # store polynomial coefficients for each line
# cumulative_img_display = img_display_orig.copy()

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []
#     img_display = cumulative_img_display.copy()

#     # Mouse callback to collect points
#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Select Points", img_display)
#     cv2.setMouseCallback("Select Points", click_event)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 2:
#         print("❌ Need at least 2 points to fit a line. Skipping this one.")
#         polynomials.append(None)
#         continue

#     all_points.append(points_original)

#     # Fit line using OpenCV
#     pts_np = np.array(points_original, dtype=np.float32)
#     line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
#     vx, vy, x0, y0 = line_params.flatten()
#     fit_lines.append((vx, vy, x0, y0))

#     # Draw the fitted line extended over the image
#     line_length = max(img.shape[1], img.shape[0])
#     x1 = int(x0 - vx * line_length)
#     y1 = int(y0 - vy * line_length)
#     x2 = int(x0 + vx * line_length)
#     y2 = int(y0 + vy * line_length)

#     x1_disp = int(x1 / scale_x)
#     y1_disp = int(y1 / scale_y)
#     x2_disp = int(x2 / scale_x)
#     y2_disp = int(y2 / scale_y)

#     cv2.line(cumulative_img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)

#     # Fit a 2nd-degree polynomial if at least 3 points selected
#     if len(points_original) >= 3:
#         pts_np = np.array(points_original)
#         x_pts = pts_np[:, 0]
#         y_pts = pts_np[:, 1]

#         # Polynomial fit y = f(x), degree 2
#         poly_coeffs = np.polyfit(x_pts, y_pts, deg=2)
#         polynomials.append(poly_coeffs)
#         print(f"Polynomial coefficients for line {line_idx + 1}: {poly_coeffs}")
#     else:
#         polynomials.append(None)

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # === Distance Calculations ===
# print("\n=== Calculating Spacing Between Lines (cv2.fitLine) ===")
# distances_pixels = []
# distances_mm = []

# if len(fit_lines) >= 2:
#     for i in range(len(fit_lines) - 1):
#         vx1, vy1, x01, y01 = fit_lines[i]
#         vx2, vy2, x02, y02 = fit_lines[i + 1]

#         base_vec = np.array([x01 - x02, y01 - y02])
#         norm_vec = np.array([-vy2, vx2])
#         norm_vec = norm_vec / np.linalg.norm(norm_vec)

#         dist = np.abs(np.dot(base_vec, norm_vec))
#         distances_pixels.append(dist)

#     avg_pixel_dist = np.mean(distances_pixels)
#     cm_per_pixel = real_world_spacing_cm / avg_pixel_dist
#     mm_per_pixel = cm_per_pixel * 10
#     distances_mm = [d * mm_per_pixel for d in distances_pixels]

#     print(f"\nAverage pixel distance: {avg_pixel_dist:.2f} px")
#     print(f"Estimated cm/pixel: {cm_per_pixel:.4f} cm/px")
#     print(f"Estimated mm/pixel: {mm_per_pixel:.4f} mm/px")
#     print("Individual distances (mm):")
#     for idx, d_mm in enumerate(distances_mm, 1):
#         print(f"  Between line {idx} and {idx+1}: {d_mm:.2f} mm")
# else:
#     print("Not enough valid lines to compute distances.")


# edit 7:

# import cv2
# import numpy as np
# import tifffile as tiff

# # === Configuration ===
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
# screen_res = (1280, 960)
# real_world_spacing_cm = 0.4  # known spacing in cm

# # === Load Image ===
# if img_path.lower().endswith(('.tiff', '.tif')):
#     img = tiff.imread(img_path)
#     if img.ndim == 2:
#         img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
#     elif img.ndim == 3 and img.shape[2] > 3:
#         img = img[:, :, :3]
# else:
#     img = cv2.imread(img_path)

# if img is None:
#     raise ValueError("Image could not be loaded. Check the path.")

# # === Calculate scale factors for display ===
# scale_x = screen_res[0] / img.shape[1]
# scale_y = screen_res[1] / img.shape[0]
# scale = min(scale_x, scale_y)
# display_w = int(img.shape[1] * scale)
# display_h = int(img.shape[0] * scale)
# img_display_orig = cv2.resize(img.copy(), (display_w, display_h))

# # Inverse scale to convert display coords back to original image coords
# scale_x = img.shape[1] / display_w
# scale_y = img.shape[0] / display_h

# # Show original resized image fullscreen for reference
# cv2.namedWindow("Original Image", cv2.WINDOW_NORMAL)
# cv2.setWindowProperty("Original Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# cv2.imshow("Original Image", img_display_orig)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# # Ask user how many lines to fit
# n_lines = int(input("Enter number of lines to fit: "))

# all_points = []     # store points of each line (in original image coords)
# fit_lines = []      # store fitted line parameters (vx, vy, x0, y0)
# polynomials = []    # store polynomial coefficients for each line
# cumulative_img_display = img_display_orig.copy()

# for line_idx in range(n_lines):
#     print(f"\n--- Select points for Line {line_idx + 1} ---")
#     points_scaled = []
#     points_original = []
#     img_display = cumulative_img_display.copy()

#     # Mouse callback to collect points
#     def click_event(event, x, y, flags, param):
#         if event == cv2.EVENT_LBUTTONDOWN:
#             x_orig = int(x * scale_x)
#             y_orig = int(y * scale_y)
#             points_scaled.append((x, y))
#             points_original.append((x_orig, y_orig))
#             cv2.circle(img_display, (x, y), 3, (0, 0, 255), -1)
#             cv2.imshow("Select Points", img_display)

#     cv2.namedWindow("Select Points", cv2.WINDOW_NORMAL)
#     cv2.setWindowProperty("Select Points", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
#     cv2.imshow("Select Points", img_display)
#     cv2.setMouseCallback("Select Points", click_event)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

#     if len(points_original) < 2:
#         print("❌ Need at least 2 points to fit a line. Skipping this one.")
#         polynomials.append(None)
#         continue

#     all_points.append(points_original)

#     # Fit line using OpenCV
#     pts_np = np.array(points_original, dtype=np.float32)
#     line_params = cv2.fitLine(pts_np, cv2.DIST_L2, 0, 0.01, 0.01)
#     vx, vy, x0, y0 = line_params.flatten()
#     fit_lines.append((vx, vy, x0, y0))

#     # Draw the fitted line extended over the image
#     line_length = max(img.shape[1], img.shape[0])
#     x1 = int(x0 - vx * line_length)
#     y1 = int(y0 - vy * line_length)
#     x2 = int(x0 + vx * line_length)
#     y2 = int(y0 + vy * line_length)

#     x1_disp = int(x1 / scale_x)
#     y1_disp = int(y1 / scale_y)
#     x2_disp = int(x2 / scale_x)
#     y2_disp = int(y2 / scale_y)

#     cv2.line(cumulative_img_display, (x1_disp, y1_disp), (x2_disp, y2_disp), (255, 0, 0), 2)

#     # Fit a 2nd-degree polynomial if at least 3 points selected
#     if len(points_original) >= 3:
#         pts_np = np.array(points_original)
#         x_pts = pts_np[:, 0]
#         y_pts = pts_np[:, 1]

#         # Polynomial fit y = f(x), degree 2
#         poly_coeffs = np.polyfit(x_pts, y_pts, deg=2)
#         polynomials.append(poly_coeffs)
#         print(f"Polynomial coefficients for line {line_idx + 1}: {poly_coeffs}")
#     else:
#         polynomials.append(None)

#     if line_idx < n_lines - 1:
#         print("Select points for next line now...")

# # === Distance Calculations ===
# print("\n=== Calculating Spacing Between Lines (cv2.fitLine) ===")
# distances_pixels = []
# distances_mm = []

# if len(fit_lines) >= 2:
#     for i in range(len(fit_lines) - 1):
#         vx1, vy1, x01, y01 = fit_lines[i]
#         vx2, vy2, x02, y02 = fit_lines[i + 1]

#         base_vec = np.array([x01 - x02, y01 - y02])
#         norm_vec = np.array([-vy2, vx2])
#         norm_vec = norm_vec / np.linalg.norm(norm_vec)

#         dist = np.abs(np.dot(base_vec, norm_vec))
#         distances_pixels.append(dist)

#     avg_pixel_dist = np.mean(distances_pixels)
#     cm_per_pixel = real_world_spacing_cm / avg_pixel_dist
#     mm_per_pixel = cm_per_pixel * 10
#     distances_mm = [d * mm_per_pixel for d in distances_pixels]

#     print(f"\nAverage pixel distance: {avg_pixel_dist:.2f} px")
#     print(f"Estimated cm/pixel: {cm_per_pixel:.4f} cm/px")
#     print(f"Estimated mm/pixel: {mm_per_pixel:.4f} mm/px")
#     print("Individual distances (mm):")
#     for idx, d_mm in enumerate(distances_mm, 1):
#         print(f"  Between line {idx} and {idx+1}: {d_mm:.2f} mm")
# else:
#     print("Not enough valid lines to compute distances.")

# # === Polynomial Intersections with Bottom Image Line & Convert to mm ===
# print("\n=== Polynomial Intersections with Bottom Line (y = bottom_y) ===")

# bottom_y = img.shape[0] - 1
# img_width = img.shape[1]

# for idx, poly in enumerate(polynomials, start=1):
#     if poly is None:
#         print(f"Line {idx}: No polynomial fitted (less than 3 points).")
#         continue

#     a, b, c = poly
#     # Solve a*x^2 + b*x + (c - bottom_y) = 0
#     coeffs = [a, b, c - bottom_y]

#     roots = np.roots(coeffs)  # roots may be complex

#     # Keep only real roots within image width bounds
#     real_roots = [r.real for r in roots if np.isreal(r) and 0 <= r.real <= img_width - 1]

#     if real_roots:
#         # Convert pixels to mm using known scale
#         real_roots_mm = [x_px * mm_per_pixel for x_px in real_roots]

#         # Print nicely formatted floats (rounded to 4 decimals)
#         pixels_str = ", ".join(f"{float(x):.4f}" for x in real_roots)
#         mm_str = ", ".join(f"{float(x):.4f}" for x in real_roots_mm)

#         print(f"Line {idx}: Intersection x-coordinates at bottom line (pixels): {pixels_str}")
#         print(f"Line {idx}: Intersection x-coordinates at bottom line (mm): {mm_str}")
#     else:
#         print(f"Line {idx}: No real intersection with bottom line within image width.")



# edit 8:


import cv2
import numpy as np
import tifffile as tiff

# === Configuration ===
img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif"
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

                # Draw fitted blue line (on current and cumulative images)
                line_length = max(img.shape[1], img.shape[0])
                x1 = int(x0 - vx * line_length)
                y1 = int(y0 - vy * line_length)
                x2 = int(x0 + vx * line_length)
                y2 = int(y0 + vy * line_length)

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
# === Draw blue fitted lines on a black background ===
print("\n=== Generating black image with blue fitted lines ===")
line_only_img = np.zeros_like(img)
blue_color = (255, 0, 0)
line_length = max(img.shape[0], img.shape[1])

for fit in fit_lines:
    if fit is None:
        continue
    vx, vy, x0, y0 = fit
    x1 = int(x0 - vx * line_length)
    y1 = int(y0 - vy * line_length)
    x2 = int(x0 + vx * line_length)
    y2 = int(y0 + vy * line_length)

    x1 = np.clip(x1, 0, img.shape[1] - 1)
    x2 = np.clip(x2, 0, img.shape[1] - 1)
    y1 = np.clip(y1, 0, img.shape[0] - 1)
    y2 = np.clip(y2, 0, img.shape[0] - 1)

    cv2.line(line_only_img, (x1, y1), (x2, y2), blue_color, 2)

# Save with absolute path and check success
output_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\blue_vertical_lines.png"
success = cv2.imwrite(output_path, line_only_img)
if success:
    print(f"File saved successfully at {output_path}")
else:
    print("Error saving the blue lines image!")

# Show saved image
cv2.imshow("Blue Lines Only", line_only_img)
cv2.waitKey(0)
cv2.destroyAllWindows()



