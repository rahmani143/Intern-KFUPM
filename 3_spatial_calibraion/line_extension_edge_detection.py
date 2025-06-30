# import cv2
# import numpy as np
# import tifffile as tiff
# import os
# import math

# # --- Load original grayscale image ---
# img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'
# img = tiff.imread(img_path)
# if img.ndim > 2:
#     img = img[:, :, 0]

# # Normalize image using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Blur to reduce noise
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# # Canny edges with chosen thresholds
# edges = cv2.Canny(blurred, 90, 170)

# # Detect line segments with HoughLinesP
# lines = cv2.HoughLinesP(
#     edges,
#     rho=1,
#     theta=np.pi / 180,
#     threshold=50,
#     minLineLength=50,
#     maxLineGap=10
# )

# print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# # Function to compute angle of a line segment in degrees [0, 180)
# def line_angle_deg(x1, y1, x2, y2):
#     angle_rad = math.atan2((y2 - y1), (x2 - x1))
#     angle_deg = abs(np.degrees(angle_rad))
#     # Normalize angle to 0-180
#     if angle_deg > 180:
#         angle_deg -= 180
#     if angle_deg > 90:
#         angle_deg = 180 - angle_deg
#     return angle_deg

# # Filter lines by angle range 60 to 90 degrees
# angle_min = 60
# angle_max = 90

# filtered_lines = []
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = line_angle_deg(x1, y1, x2, y2)
#         if angle_min <= angle <= angle_max:
#             filtered_lines.append((x1, y1, x2, y2, angle))

# print(f"Lines after angle filtering: {len(filtered_lines)}")

# # Remove lines that are very close to each other
# def line_midpoint(line):
#     x1, y1, x2, y2, _ = line
#     return ((x1 + x2) / 2, (y1 + y2) / 2)

# def dist_points(p1, p2):
#     return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# def angle_diff(a1, a2):
#     return abs(a1 - a2)

# filtered_unique = []
# distance_thresh = 20  # pixels, tune as needed
# angle_thresh = 5      # degrees

# for candidate in filtered_lines:
#     keep = True
#     mp_cand = line_midpoint(candidate)
#     angle_cand = candidate[4]
#     for kept in filtered_unique:
#         mp_kept = line_midpoint(kept)
#         angle_kept = kept[4]
#         if dist_points(mp_cand, mp_kept) < distance_thresh and angle_diff(angle_cand, angle_kept) < angle_thresh:
#             keep = False
#             break
#     if keep:
#         filtered_unique.append(candidate)

# print(f"Lines after removing close duplicates: {len(filtered_unique)}")

# # Prepare colored image for drawing
# img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# height, width = img.shape

# # Extend each filtered line from y=0 to y=height
# for (x1, y1, x2, y2, angle) in filtered_unique:
#     # Handle vertical lines (avoid division by zero)
#     if x2 - x1 == 0:
#         x = x1
#         cv2.line(img_color, (x, 0), (x, height - 1), (0, 0, 255), 2)  # Red vertical line
#         continue

#     # Compute slope and intercept
#     m = (y2 - y1) / (x2 - x1)
#     c = y1 - m * x1

#     # Calculate x for y=0 and y=height
#     x_top = int((0 - c) / m)
#     x_bottom = int((height - 1 - c) / m)

#     # Clip x values inside image width
#     x_top = np.clip(x_top, 0, width - 1)
#     x_bottom = np.clip(x_bottom, 0, width - 1)

#     # Draw extended line in blue
#     cv2.line(img_color, (x_top, 0), (x_bottom, height - 1), (255, 0, 0), 2)

# print(f"Extended and drew {len(filtered_unique)} lines.")

# # Save final output
# output_path = os.path.join(os.path.dirname(img_path), 'my_image_lines_extended_full.png')
# cv2.imwrite(output_path, img_color)
# print(f"Saved extended lines image to: {output_path}")


# edit 2:

# import cv2
# import numpy as np
# import tifffile as tiff
# import os
# import math

# # --- Load original grayscale image ---
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_filtered_lines_debug_straightened.png"
# img = tiff.imread(img_path)
# if img.ndim > 2:
#     img = img[:, :, 0]

# # Normalize image using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Blur to reduce noise
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# # Canny edges with chosen thresholds
# edges = cv2.Canny(blurred, 90, 170)

# # Detect line segments with HoughLinesP
# lines = cv2.HoughLinesP(
#     edges,
#     rho=1,
#     theta=np.pi / 180,
#     threshold=50,
#     minLineLength=50,
#     maxLineGap=10
# )

# print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# # Function to compute angle of a line segment in degrees [0, 180)
# def line_angle_deg(x1, y1, x2, y2):
#     angle_rad = math.atan2((y2 - y1), (x2 - x1))
#     angle_deg = abs(np.degrees(angle_rad))
#     if angle_deg > 180:
#         angle_deg -= 180
#     if angle_deg > 90:
#         angle_deg = 180 - angle_deg
#     return angle_deg

# # Filter lines by angle range 60 to 90 degrees
# angle_min = 60
# angle_max = 90

# filtered_lines = []
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = line_angle_deg(x1, y1, x2, y2)
#         if angle_min <= angle <= angle_max:
#             filtered_lines.append((x1, y1, x2, y2, angle))

# print(f"Lines after angle filtering: {len(filtered_lines)}")

# # Remove lines that are very close to each other
# def line_midpoint(line):
#     x1, y1, x2, y2, _ = line
#     return ((x1 + x2) / 2, (y1 + y2) / 2)

# def dist_points(p1, p2):
#     return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# def angle_diff(a1, a2):
#     return abs(a1 - a2)

# filtered_unique = []
# distance_thresh = 20  # pixels
# angle_thresh = 5      # degrees

# for candidate in filtered_lines:
#     keep = True
#     mp_cand = line_midpoint(candidate)
#     angle_cand = candidate[4]
#     for kept in filtered_unique:
#         mp_kept = line_midpoint(kept)
#         angle_kept = kept[4]
#         if dist_points(mp_cand, mp_kept) < distance_thresh and angle_diff(angle_cand, angle_kept) < angle_thresh:
#             keep = False
#             break
#     if keep:
#         filtered_unique.append(candidate)

# print(f"Lines after removing close duplicates: {len(filtered_unique)}")

# # Further filter: keep only lines close to the median angle (parallelism)
# angles = [line[4] for line in filtered_unique]
# median_angle = np.median(angles)
# angle_tolerance = 3  # degrees
# final_lines = [line for line in filtered_unique if abs(line[4] - median_angle) < angle_tolerance]

# # Cluster lines by x-position (for vertical-ish lines)
# x_positions = [((line[0] + line[2]) / 2) for line in final_lines]
# x_positions = np.array(x_positions)
# sorted_indices = np.argsort(x_positions)
# x_positions_sorted = x_positions[sorted_indices]
# final_lines_sorted = [final_lines[i] for i in sorted_indices]

# min_spacing = 20  # pixels
# kept_indices = [0]
# for i in range(1, len(x_positions_sorted)):
#     if np.min(np.abs(x_positions_sorted[i] - x_positions_sorted[kept_indices])) > min_spacing:
#         kept_indices.append(i)
# final_lines_clustered = [final_lines_sorted[i] for i in kept_indices]

# print(f"Lines after clustering: {len(final_lines_clustered)}")

# # Optional: Intensity gradient check (keep lines with strong edge)
# def edge_strength(line, img, width=5):
#     x1, y1, x2, y2, _ = line
#     length = int(np.hypot(x2 - x1, y2 - y1))
#     if length == 0:
#         return 0
#     xs = np.linspace(x1, x2, length)
#     ys = np.linspace(y1, y2, length)
#     strengths = []
#     for i in range(length):
#         x, y = int(xs[i]), int(ys[i])
#         perp = np.array([-(y2 - y1), x2 - x1])
#         perp = perp / np.linalg.norm(perp)
#         p1 = np.array([x, y]) + perp * width
#         p2 = np.array([x, y]) - perp * width
#         p1 = np.clip(p1, [0, 0], [img.shape[1]-1, img.shape[0]-1]).astype(int)
#         p2 = np.clip(p2, [0, 0], [img.shape[1]-1, img.shape[0]-1]).astype(int)
#         intensity1 = img[p1[1], p1[0]]
#         intensity2 = img[p2[1], p2[0]]
#         strengths.append(abs(intensity1 - intensity2))
#     return np.mean(strengths)

# edge_thresh = 30  # adjust as needed
# final_lines_strong = []
# for line in final_lines_clustered:
#     strength = edge_strength(line, img_norm)
#     if strength > edge_thresh:
#         final_lines_strong.append(line)

# print(f"Lines after edge strength filtering: {len(final_lines_strong)}")

# # Prepare colored image for drawing
# img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# height, width = img.shape

# # Extend and draw only the final, clean lines
# for (x1, y1, x2, y2, angle) in final_lines_strong:
#     if x2 - x1 == 0:
#         x = x1
#         cv2.line(img_color, (x, 0), (x, height - 1), (0, 0, 255), 2)
#         continue
#     m = (y2 - y1) / (x2 - x1)
#     c = y1 - m * x1
#     x_top = int((0 - c) / m)
#     x_bottom = int((height - 1 - c) / m)
#     x_top = np.clip(x_top, 0, width - 1)
#     x_bottom = np.clip(x_bottom, 0, width - 1)
#     cv2.line(img_color, (x_top, 0), (x_bottom, height - 1), (255, 0, 0), 2)

# print(f"Extended and drew {len(final_lines_strong)} clean lines.")

# # Save final output
# output_path = os.path.join(os.path.dirname(img_path), 'my_image_lines_cleaned.png')
# cv2.imwrite(output_path, img_color)
# print(f"Saved cleaned lines image to: {output_path}")


# edit 3:

#almost done .. the red lines are close to perfect .. make sure to give only straightened lines to the code 

# import cv2
# import numpy as np
# import tifffile as tiff
# import os
# import math

# # --- Load original grayscale image ---
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_filtered_lines_debug_straightened.png"
# ext = os.path.splitext(img_path)[1].lower()

# # Read based on file extension
# if ext in ['.tif', '.tiff']:
#     img = tiff.imread(img_path)
# else:
#     img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# # Normalize image using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Blur to reduce noise
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# # Canny edges
# edges = cv2.Canny(blurred, 90, 170)

# # Detect line segments
# lines = cv2.HoughLinesP(
#     edges,
#     rho=1,
#     theta=np.pi / 180,
#     threshold=50,
#     minLineLength=50,
#     maxLineGap=10
# )

# print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# # --- Angle computation helper ---
# def line_angle_deg(x1, y1, x2, y2):
#     angle_rad = math.atan2((y2 - y1), (x2 - x1))
#     angle_deg = abs(np.degrees(angle_rad))
#     if angle_deg > 180:
#         angle_deg -= 180
#     if angle_deg > 90:
#         angle_deg = 180 - angle_deg
#     return angle_deg

# # Filter near-vertical lines
# angle_min = 85
# angle_max = 95
# filtered_lines = []
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = line_angle_deg(x1, y1, x2, y2)
#         if angle_min <= angle <= angle_max:
#             filtered_lines.append((x1, y1, x2, y2, angle))

# print(f"Lines after angle filtering: {len(filtered_lines)}")

# # Remove near-duplicate lines
# def line_midpoint(line):
#     x1, y1, x2, y2, _ = line
#     return ((x1 + x2) / 2, (y1 + y2) / 2)

# def dist_points(p1, p2):
#     return np.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

# def angle_diff(a1, a2):
#     return abs(a1 - a2)

# filtered_unique = []
# distance_thresh = 20  # pixels
# angle_thresh = 5      # degrees

# for candidate in filtered_lines:
#     keep = True
#     mp_cand = line_midpoint(candidate)
#     angle_cand = candidate[4]
#     for kept in filtered_unique:
#         mp_kept = line_midpoint(kept)
#         angle_kept = kept[4]
#         if dist_points(mp_cand, mp_kept) < distance_thresh and angle_diff(angle_cand, angle_kept) < angle_thresh:
#             keep = False
#             break
#     if keep:
#         filtered_unique.append(candidate)

# print(f"Lines after removing close duplicates: {len(filtered_unique)}")

# # Filter by median angle
# angles = [line[4] for line in filtered_unique]
# median_angle = np.median(angles)
# angle_tolerance = 3  # degrees
# final_lines = [line for line in filtered_unique if abs(line[4] - median_angle) < angle_tolerance]

# # Cluster lines by x-position (for vertical-ish lines)
# x_positions = [((line[0] + line[2]) / 2) for line in final_lines]
# x_positions = np.array(x_positions)
# sorted_indices = np.argsort(x_positions)
# x_positions_sorted = x_positions[sorted_indices]
# final_lines_sorted = [final_lines[i] for i in sorted_indices]

# min_spacing = 20  # pixels
# kept_indices = [0]
# for i in range(1, len(x_positions_sorted)):
#     if np.min(np.abs(x_positions_sorted[i] - x_positions_sorted[kept_indices])) > min_spacing:
#         kept_indices.append(i)
# final_lines_clustered = [final_lines_sorted[i] for i in kept_indices]

# print(f"Lines after clustering: {len(final_lines_clustered)}")

# # Edge strength filter
# def edge_strength(line, img, width=5):
#     x1, y1, x2, y2, _ = line
#     length = int(np.hypot(x2 - x1, y2 - y1))
#     if length == 0:
#         return 0
#     xs = np.linspace(x1, x2, length)
#     ys = np.linspace(y1, y2, length)
#     strengths = []
#     for i in range(length):
#         x, y = int(xs[i]), int(ys[i])
#         perp = np.array([-(y2 - y1), x2 - x1])
#         perp = perp / np.linalg.norm(perp)
#         p1 = np.array([x, y]) + perp * width
#         p2 = np.array([x, y]) - perp * width
#         p1 = np.clip(p1, [0, 0], [img.shape[1]-1, img.shape[0]-1]).astype(int)
#         p2 = np.clip(p2, [0, 0], [img.shape[1]-1, img.shape[0]-1]).astype(int)
#         intensity1 = img[p1[1], p1[0]]
#         intensity2 = img[p2[1], p2[0]]
#         strengths.append(abs(intensity1 - intensity2))
#     return np.mean(strengths)

# edge_thresh = 30  # adjust as needed
# final_lines_strong = []
# for line in final_lines_clustered:
#     strength = edge_strength(line, img_norm)
#     if strength > edge_thresh:
#         final_lines_strong.append(line)

# print(f"Lines after edge strength filtering: {len(final_lines_strong)}")

# # --- Draw lines ---
# img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# height, width = img.shape

# for (x1, y1, x2, y2, angle) in final_lines_strong:
#     if x2 - x1 == 0:
#         x = x1
#         cv2.line(img_color, (x, 0), (x, height - 1), (0, 0, 255), 2)
#         continue
#     m = (y2 - y1) / (x2 - x1)
#     c = y1 - m * x1
#     x_top = int((0 - c) / m)
#     x_bottom = int((height - 1 - c) / m)
#     x_top = np.clip(x_top, 0, width - 1)
#     x_bottom = np.clip(x_bottom, 0, width - 1)
#     cv2.line(img_color, (x_top, 0), (x_bottom, height - 1), (255, 0, 0), 2)

# print(f"Extended and drew {len(final_lines_strong)} clean lines.")

# # Save output
# output_path = os.path.join(os.path.dirname(img_path), 'my_image_lines_cleaned.png')
# cv2.imwrite(output_path, img_color)
# print(f"Saved cleaned lines image to: {output_path}")


# edit 4:

# import cv2
# import numpy as np
# import os
# import math

# # --- Load PNG image (already straightened) ---
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_lines_cleaned.png"
# img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# # Normalize using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Blur + Canny edge detection
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)
# edges = cv2.Canny(blurred, 90, 170)

# # Detect lines with Hough Transform
# lines = cv2.HoughLinesP(
#     edges,
#     rho=1,
#     theta=np.pi / 180,
#     threshold=50,
#     minLineLength=50,
#     maxLineGap=10
# )

# print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# # Calculate line angle
# def line_angle_deg(x1, y1, x2, y2):
#     angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
#     return 180 - angle if angle > 90 else angle

# # Filter near-vertical lines only
# angle_thresh = 5  # ±5° tolerance
# filtered_lines = []
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = line_angle_deg(x1, y1, x2, y2)
#         if abs(angle - 90) <= angle_thresh:
#             filtered_lines.append((x1, y1, x2, y2))

# print(f"Lines after vertical filtering: {len(filtered_lines)}")

# # Draw vertical lines in blue
# img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# height, width = img.shape

# for (x1, y1, x2, y2) in filtered_lines:
#     # Extend the vertical line across full height
#     x_avg = int((x1 + x2) / 2)
#     cv2.line(img_color, (x_avg, 0), (x_avg, height - 1), (255, 0, 0), 2)

# print(f"Drew {len(filtered_lines)} vertical lines.")

# # Save result
# output_path = os.path.join(os.path.dirname(img_path), 'clean_vertical_lines.png')
# cv2.imwrite(output_path, img_color)
# print(f"Saved final image to: {output_path}")


# edit 5:

#this code is givng a very clear straight lines (almost perfect)

# import cv2
# import numpy as np
# import os
# import math

# # --- Load PNG image (already straightened) ---
# img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_lines_cleaned.png"
# img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# # Normalize using percentiles
# min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
# img_clipped = np.clip(img, min_val, max_val)
# img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Blur + Canny edge detection
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)
# edges = cv2.Canny(blurred, 90, 170)

# # Detect line segments
# lines = cv2.HoughLinesP(
#     edges,
#     rho=1,
#     theta=np.pi / 180,
#     threshold=50,
#     minLineLength=50,
#     maxLineGap=10
# )

# print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# # Compute angle
# def line_angle_deg(x1, y1, x2, y2):
#     angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
#     return 180 - angle if angle > 90 else angle

# # Filter near-vertical lines only
# angle_thresh = 5  # ±5° from vertical
# vertical_lines = []
# if lines is not None:
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = line_angle_deg(x1, y1, x2, y2)
#         if abs(angle - 90) <= angle_thresh:
#             x_center = int((x1 + x2) / 2)
#             vertical_lines.append(x_center)

# print(f"Vertical lines before merging: {len(vertical_lines)}")

# # Cluster X positions to merge close lines
# vertical_lines = sorted(vertical_lines)
# merged_lines = []
# cluster = []

# distance_thresh = 10  # pixels

# for x in vertical_lines:
#     if not cluster:
#         cluster.append(x)
#     elif abs(x - cluster[-1]) <= distance_thresh:
#         cluster.append(x)
#     else:
#         merged_lines.append(int(np.mean(cluster)))
#         cluster = [x]

# # Add final cluster
# if cluster:
#     merged_lines.append(int(np.mean(cluster)))

# print(f"Vertical lines after merging: {len(merged_lines)}")

# # Draw merged vertical lines
# img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# height, width = img.shape

# for x in merged_lines:
#     cv2.line(img_color, (x, 0), (x, height - 1), (255, 0, 0), 2)

# # Save result
# output_path = os.path.join(os.path.dirname(img_path), 'clean_vertical_lines_clustered.png')
# cv2.imwrite(output_path, img_color)
# print(f"Saved clustered vertical lines image to: {output_path}")



# edit 6:
import cv2
import numpy as np
import os
import math

# --- Load PNG image (already straightened) ---
img_path = "C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_lines_cleaned.png"
img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# Normalize using percentiles
min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
img_clipped = np.clip(img, min_val, max_val)
img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Blur + Canny edge detection
blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)
edges = cv2.Canny(blurred, 90, 170)

# Detect line segments
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=50,
    maxLineGap=10
)

print(f"Detected {len(lines) if lines is not None else 0} total lines.")

# Compute angle of a line segment
def line_angle_deg(x1, y1, x2, y2):
    angle = abs(math.degrees(math.atan2(y2 - y1, x2 - x1)))
    return 180 - angle if angle > 90 else angle

# Filter near-vertical lines only (within ±5 degrees of vertical)
angle_thresh = 5
vertical_lines = []
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = line_angle_deg(x1, y1, x2, y2)
        if abs(angle - 90) <= angle_thresh:
            x_center = int((x1 + x2) / 2)
            vertical_lines.append(x_center)

print(f"Vertical lines before merging: {len(vertical_lines)}")

# Cluster X positions to merge lines close to each other
vertical_lines = sorted(vertical_lines)
merged_lines = []
cluster = []

distance_thresh = 10  # pixels

for x in vertical_lines:
    if not cluster:
        cluster.append(x)
    elif abs(x - cluster[-1]) <= distance_thresh:
        cluster.append(x)
    else:
        merged_lines.append(int(np.mean(cluster)))
        cluster = [x]

# Add last cluster
if cluster:
    merged_lines.append(int(np.mean(cluster)))

print(f"Vertical lines after merging: {len(merged_lines)}")

# Draw merged vertical lines on color image
img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
height, width = img.shape

for x in merged_lines:
    cv2.line(img_color, (x, 0), (x, height - 1), (255, 0, 0), 2)

# Save clustered vertical lines image
output_path = os.path.join(os.path.dirname(img_path), 'clean_vertical_lines_clustered.png')
cv2.imwrite(output_path, img_color)
print(f"Saved clustered vertical lines image to: {output_path}")

# --- Compute distances between lines in pixels and real-world mm ---

# Compute pixel distances between consecutive merged lines
pixel_distances = [merged_lines[i+1] - merged_lines[i] for i in range(len(merged_lines) - 1)]

# Known real-world spacing between lines (in mm)
known_real_spacing_mm = 3.7

# Estimate mm-per-pixel for each gap
mm_per_pixel_estimates = [known_real_spacing_mm / d for d in pixel_distances if d != 0]
avg_mm_per_pixel = np.mean(mm_per_pixel_estimates) if mm_per_pixel_estimates else 0

# Print pixel distances and conversion info
print("\n--- Line Gap Analysis ---")
print("Pixel distances between lines:", [round(d, 2) for d in pixel_distances])
print("Estimated mm/pixel per gap:", [round(r, 4) for r in mm_per_pixel_estimates])
print(f"Average mm/pixel ratio: {avg_mm_per_pixel:.5f}")

# Reusable conversion function from pixels to mm
def pixels_to_mm(pixels):
    return pixels * avg_mm_per_pixel

# Example conversion
example_pixel_gap = 50
print(f"{example_pixel_gap} pixels ≈ {pixels_to_mm(example_pixel_gap):.2f} mm")
