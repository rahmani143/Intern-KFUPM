# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from tifffile import imread

# # Load image
# img_path = 'C:/Users/bss10/OneDrive/Desktop/camera_env/aquired_images/calibration_spatial_misc/the_op.png'  # <-- change if needed
# img = imread(img_path)
# if img.ndim > 2:
#     img = img[:, :, 0]

# # Normalize intensity range
# min_val, max_val = 20, 75
# img_norm = np.clip(img, min_val, max_val)
# img_norm = ((img_norm - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Apply Gaussian blur
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 0)

# # Canny edge detection
# edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

# # Detect lines using Probabilistic Hough Transform
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)

# # Prepare for drawing
# line_img = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# midpoints = []

# # Collect midpoints of all detected lines
# if lines is not None:
#     print(f"Total lines detected by Hough: {len(lines)}")
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
#         midpoints.append((xm, ym, x1, y1, x2, y2))
# else:
#     print("⚠ No lines detected.")
#     midpoints = []

# # Sort by x-coordinate (left to right)
# midpoints.sort(key=lambda x: x[0])

# # Print midpoint positions and distances
# print("Midpoint x-coordinates:")
# print([m[0] for m in midpoints])

# print("Distances between consecutive midpoints:")
# for i in range(len(midpoints) - 1):
#     d = np.hypot(midpoints[i+1][0] - midpoints[i][0],
#                  midpoints[i+1][1] - midpoints[i][1])
#     print(f"Line {i} to {i+1}: {d:.2f} px")

# # Filter lines based on spacing
# filtered = []
# if midpoints:
#     filtered.append(midpoints[0])
#     for i in range(1, len(midpoints)):
#         prev = filtered[-1]
#         curr = midpoints[i]
#         dist = np.hypot(curr[0] - prev[0], curr[1] - prev[1])
#         if 30 < dist < 120:  # Adjusted filtering
#             filtered.append(curr)

# # Fallback if filtering removed all lines
# if len(filtered) < 2:
#     print("⚠ Too few filtered lines; using all detected lines instead.")
#     filtered = midpoints

# # Compute average distance and real-world scale
# if len(filtered) > 1:
#     pixel_distances = [np.hypot(filtered[i+1][0] - filtered[i][0],
#                                 filtered[i+1][1] - filtered[i][1])
#                        for i in range(len(filtered) - 1)]
#     avg_pixel_dist = np.mean(pixel_distances)
#     scale_cm_per_pixel = 2.0 / avg_pixel_dist  # Assuming 2 cm between lines
# else:
#     avg_pixel_dist = 0
#     scale_cm_per_pixel = 0

# # Draw filtered lines and index labels
# for idx, (xm, ym, x1, y1, x2, y2) in enumerate(filtered):
#     cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#     cv2.putText(line_img, f'{idx}', (xm - 10, ym - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# # Display results
# line_img_rgb = cv2.cvtColor(line_img, cv2.COLOR_BGR2RGB)
# plt.figure(figsize=(12, 8))
# plt.imshow(line_img_rgb)
# plt.title("Detected & Filtered Slanted Lines (~2 cm Spacing)")
# plt.axis('off')
# plt.tight_layout()
# plt.show()

# # Final result print
# print(f"\n✅ Results:")
# print(f"  Filtered lines: {len(filtered)}")
# print(f"  Average pixel distance: {avg_pixel_dist:.2f} pixels")
# print(f"  Scale: {scale_cm_per_pixel:.4f} cm/pixel")


# edit 1:

import cv2
import numpy as np
import matplotlib.pyplot as plt
from tifffile import imread
import os

# # Use OpenCV instead of tifffile (your image is a PNG, not TIFF)
# img_path = 'C:/Users/bss10/OneDrive/Desktop/camera_env/aquired_images/calibration_spatial_misc/the_op.png'
# img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

# if img is None:
#     raise ValueError(f"Could not load image at {img_path}")

# # Normalize intensity range (adjusted)
# min_val, max_val = 20, 75
# img_norm = np.clip(img, min_val, max_val)
# img_norm = ((img_norm - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# # Apply Gaussian blur
# blurred = cv2.GaussianBlur(img_norm, (5, 5), 0)

# # Canny edge detection
# edges = cv2.Canny(blurred, 50, 150, apertureSize=3)

# # Show edges (optional debug plot)
# plt.figure(figsize=(10, 10))
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edges')
# plt.axis('off')
# plt.tight_layout()
# plt.show()

# # Detect lines using Probabilistic Hough Transform (tuned)
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=30, minLineLength=40, maxLineGap=20)

# # Prepare for drawing
# line_img = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)
# midpoints = []

# # Filter lines based on angle
# if lines is not None:
#     print(f"✅ Total lines detected by Hough: {len(lines)}")
#     for line in lines:
#         x1, y1, x2, y2 = line[0]
#         angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

#         # Keep vertical-slanted lines (between 60° and 120°)
#         if 60 < abs(angle) < 120:
#             xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
#             midpoints.append((xm, ym, x1, y1, x2, y2))
# else:
#     print("⚠ No lines detected.")
#     midpoints = []

# print(f"🧹 Midpoints after angle filtering: {len(midpoints)}")

# # Sort midpoints by x-coordinate
# midpoints.sort(key=lambda x: x[0])

# # Print midpoint positions and distances
# print("Midpoint x-coordinates:")
# print([m[0] for m in midpoints])

# print("Distances between consecutive midpoints:")
# for i in range(len(midpoints) - 1):
#     d = np.hypot(midpoints[i+1][0] - midpoints[i][0],
#                  midpoints[i+1][1] - midpoints[i][1])
#     print(f"Line {i} to {i+1}: {d:.2f} px")

# # Filter lines based on spacing (optional)
# filtered = []
# if midpoints:
#     filtered.append(midpoints[0])
#     for i in range(1, len(midpoints)):
#         prev = filtered[-1]
#         curr = midpoints[i]
#         dist = np.hypot(curr[0] - prev[0], curr[1] - prev[1])
#         if 30 < dist < 120:
#             filtered.append(curr)

# if len(filtered) < 2:
#     print("⚠ Too few filtered lines; using all angle-filtered midpoints instead.")
#     filtered = midpoints

# # Compute average pixel distance and real-world scale
# if len(filtered) > 1:
#     pixel_distances = [np.hypot(filtered[i+1][0] - filtered[i][0],
#                                 filtered[i+1][1] - filtered[i][1])
#                        for i in range(len(filtered) - 1)]
#     avg_pixel_dist = np.mean(pixel_distances)
#     scale_cm_per_pixel = 2.0 / avg_pixel_dist  # Assuming 2 cm between lines
# else:
#     avg_pixel_dist = 0
#     scale_cm_per_pixel = 0

# # Draw filtered lines and indices
# for idx, (xm, ym, x1, y1, x2, y2) in enumerate(filtered):
#     cv2.line(line_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#     cv2.putText(line_img, f'{idx}', (xm - 10, ym - 10),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

# # Display final result
# line_img_rgb = cv2.cvtColor(line_img, cv2.COLOR_BGR2RGB)
# plt.figure(figsize=(12, 8))
# plt.imshow(line_img_rgb)
# plt.title("Detected & Filtered Slanted Lines (~2 cm Spacing)")
# plt.axis('off')
# plt.tight_layout()
# plt.show()

# # Print final results
# print(f"\n✅ Results:")
# print(f"  Filtered lines: {len(filtered)}")
# print(f"  Average pixel distance: {avg_pixel_dist:.2f} pixels")
# print(f"  Scale: {scale_cm_per_pixel:.4f} cm/pixel")



# edit 2:

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # Load and preprocess image
# img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'
# img = cv2.imread(img_path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# edges = cv2.Canny(blurred, 50, 150)

# # Display Canny edges
# plt.figure(figsize=(12, 6))
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edges')
# plt.show()

# # Detect lines using Hough Transform
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)
# print(f"✅ Total lines detected by Hough: {len(lines)}")

# # Extract midpoints and filter by angle
# filtered = []
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
#     if abs(angle) > 80:  # Keep mostly vertical lines
#         xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
#         filtered.append((xm, ym, x1, y1, x2, y2))

# print(f"🧹 Midpoints after angle filtering: {len(filtered)}")

# # Sort midpoints by x-coordinate and cluster nearby ones
# filtered.sort(key=lambda x: x[0])
# clustered = []
# cluster_thresh = 10  # Pixels in x-direction

# for m in filtered:
#     if not clustered:
#         clustered.append([m])
#     else:
#         last_cluster = clustered[-1]
#         if abs(m[0] - np.mean([p[0] for p in last_cluster])) < cluster_thresh:
#             last_cluster.append(m)
#         else:
#             clustered.append([m])

# # Merge each cluster to form unique line
# merged_lines = []
# for cluster in clustered:
#     xm = int(np.mean([pt[0] for pt in cluster]))
#     ym = int(np.mean([pt[1] for pt in cluster]))
#     x1 = int(np.mean([pt[2] for pt in cluster]))
#     y1 = int(np.mean([pt[3] for pt in cluster]))
#     x2 = int(np.mean([pt[4] for pt in cluster]))
#     y2 = int(np.mean([pt[5] for pt in cluster]))
#     merged_lines.append((xm, ym, x1, y1, x2, y2))

# print(f"🔍 Unique merged lines: {len(merged_lines)}")

# # Draw merged lines
# img_lines = img.copy()
# for (xm, ym, x1, y1, x2, y2) in merged_lines:
#     cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.circle(img_lines, (xm, ym), 5, (0, 0, 255), -1)

# plt.figure(figsize=(12, 6))
# plt.imshow(cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB))
# plt.title('Merged Unique Lines')
# plt.show()

# # Sort again by x to compute distances
# merged_lines.sort(key=lambda x: x[0])
# midpoints_x = [np.int32(line[0]) for line in merged_lines]

# # Print midpoints
# print("Midpoint x-coordinates:")
# print(midpoints_x)

# # Compute pixel distances
# pixel_distances = []
# for i in range(len(midpoints_x) - 1):
#     d = np.abs(midpoints_x[i + 1] - midpoints_x[i])
#     pixel_distances.append(d)
#     print(f"Line {i} to {i + 1}: {d:.2f} px")

# # Final output
# print(f"\n✅ Results:")
# print(f"  Filtered lines: {len(merged_lines)}")
# if len(pixel_distances) > 0:
#     avg_pixel_dist = np.mean(pixel_distances)
#     print(f"  Average pixel distance: {avg_pixel_dist:.2f} pixels")

#     # Estimate scale (adjust manually if needed)
#     cm_per_pixel = 0.0346  # Example: measured based on real-world ref
#     print(f"  Scale: {cm_per_pixel:.4f} cm/pixel")
#     print(f"  Average physical distance: {avg_pixel_dist * cm_per_pixel:.2f} cm")
# else:
#     print("  Not enough lines to calculate spacing.")


# edit 3:


# import cv2
# import numpy as np
# import matplotlib.pyplot as plt

# # Load and preprocess image
# img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\calibration_spatial_misc\\the_op.png'
# img = cv2.imread(img_path)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# edges = cv2.Canny(blurred, 50, 150)

# # Display Canny edges
# plt.figure(figsize=(12, 6))
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edges')
# plt.show()

# # Detect lines using Hough Transform
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)
# print(f"✅ Total lines detected by Hough: {len(lines)}")

# # Extract midpoints and filter by angle
# filtered = []
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
#     if abs(angle) > 80:  # Keep mostly vertical lines
#         xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
#         filtered.append((xm, ym, x1, y1, x2, y2))

# print(f"🧹 Midpoints after angle filtering: {len(filtered)}")

# # Sort midpoints by x-coordinate and cluster nearby ones
# filtered.sort(key=lambda x: x[0])
# clustered = []
# cluster_thresh = 10  # Pixels in x-direction

# for m in filtered:
#     if not clustered:
#         clustered.append([m])
#     else:
#         last_cluster = clustered[-1]
#         if abs(m[0] - np.mean([p[0] for p in last_cluster])) < cluster_thresh:
#             last_cluster.append(m)
#         else:
#             clustered.append([m])

# # Merge each cluster to form unique line
# merged_lines = []
# for cluster in clustered:
#     xm = int(np.mean([pt[0] for pt in cluster]))
#     ym = int(np.mean([pt[1] for pt in cluster]))
#     x1 = int(np.mean([pt[2] for pt in cluster]))
#     y1 = int(np.mean([pt[3] for pt in cluster]))
#     x2 = int(np.mean([pt[4] for pt in cluster]))
#     y2 = int(np.mean([pt[5] for pt in cluster]))
#     merged_lines.append((xm, ym, x1, y1, x2, y2))

# print(f"🔍 Unique merged lines: {len(merged_lines)}")

# # Draw merged lines
# img_lines = img.copy()
# for (xm, ym, x1, y1, x2, y2) in merged_lines:
#     cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.circle(img_lines, (xm, ym), 5, (0, 0, 255), -1)

# plt.figure(figsize=(12, 6))
# plt.imshow(cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB))
# plt.title('Merged Unique Lines')
# plt.show()

# # Sort again by x to compute distances
# merged_lines.sort(key=lambda x: x[0])
# midpoints_x = [np.int32(line[0]) for line in merged_lines]

# # Print midpoints
# print("Midpoint x-coordinates:")
# print(midpoints_x)

# # Compute all pixel distances
# pixel_distances = []
# for i in range(len(midpoints_x) - 1):
#     d = np.abs(midpoints_x[i + 1] - midpoints_x[i])
#     pixel_distances.append(d)
#     print(f"Line {i} to {i + 1}: {d:.2f} px")

# # Initial stats
# print(f"\n✅ Results:")
# print(f"  Filtered lines: {len(merged_lines)}")
# if len(pixel_distances) > 0:
#     avg_pixel_dist = np.mean(pixel_distances)
#     print(f"  Average pixel distance: {avg_pixel_dist:.2f} pixels")
#     cm_per_pixel = 0.0346
#     print(f"  Scale: {cm_per_pixel:.4f} cm/pixel")
#     print(f"  Average physical distance: {avg_pixel_dist * cm_per_pixel:.2f} cm")
# else:
#     print("  Not enough lines to calculate spacing.")

# # ---------------------------------------------------------------
# # 🧼 Remove extreme edge lines (assumed to be picture frame)
# if len(midpoints_x) > 2:
#     clean_midpoints_x = midpoints_x[1:-1]  # remove first and last
# else:
#     clean_midpoints_x = midpoints_x  # not enough lines to clean

# print("\n🧼 Cleaned midpoint x-coordinates (after removing edges):")
# print(clean_midpoints_x)

# # Recalculate distances
# clean_pixel_distances = []
# for i in range(len(clean_midpoints_x) - 1):
#     d = np.abs(clean_midpoints_x[i + 1] - clean_midpoints_x[i])
#     clean_pixel_distances.append(d)
#     print(f"Line {i} to {i + 1}: {d:.2f} px")

# # Final output after cleaning
# print(f"\n✅ Final Results (Excluding edges):")
# print(f"  Valid lines: {len(clean_midpoints_x)}")
# if len(clean_pixel_distances) > 0:
#     avg_clean_dist = np.mean(clean_pixel_distances)
#     print(f"  Average pixel distance: {avg_clean_dist:.2f} pixels")
#     print(f"  Scale: {cm_per_pixel:.4f} cm/pixel")
#     print(f"  Average physical distance: {avg_clean_dist * cm_per_pixel:.2f} cm")
# else:
#     print("  Not enough lines to calculate spacing.")


# edit 4:

# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# # -------------------- Step 1: Load and Preprocess Image --------------------
# img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'

# # Load image
# img = cv2.imread(img_path)
# if img is None:
#     raise ValueError(f"❌ Image not found at: {img_path}")

# # Convert to grayscale and blur
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# edges = cv2.Canny(blurred, 50, 150)

# # Show Canny edges
# plt.figure(figsize=(12, 6))
# plt.imshow(edges, cmap='gray')
# plt.title('Canny Edges')
# plt.axis('off')
# plt.show()

# # -------------------- Step 2: Hough Line Detection --------------------
# lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=100, maxLineGap=20)
# if lines is None:
#     raise ValueError("❌ No lines detected by Hough Transform.")
# print(f"✅ Total lines detected by Hough: {len(lines)}")

# # -------------------- Step 3: Filter Vertical Lines --------------------
# filtered = []
# for line in lines:
#     x1, y1, x2, y2 = line[0]
#     angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
#     if abs(angle) > 80:  # keep vertical-ish lines
#         xm, ym = (x1 + x2) // 2, (y1 + y2) // 2
#         filtered.append((xm, ym, x1, y1, x2, y2))

# print(f"🧹 Midpoints after angle filtering: {len(filtered)}")

# # -------------------- Step 4: Cluster Nearby Lines by x --------------------
# filtered.sort(key=lambda x: x[0])
# cluster_thresh = 10  # pixel threshold in x-direction
# clustered = []

# for m in filtered:
#     if not clustered:
#         clustered.append([m])
#     else:
#         last_cluster = clustered[-1]
#         if abs(m[0] - np.mean([p[0] for p in last_cluster])) < cluster_thresh:
#             last_cluster.append(m)
#         else:
#             clustered.append([m])

# # -------------------- Step 5: Merge Clusters to Unique Lines --------------------
# merged_lines = []
# for cluster in clustered:
#     xm = int(np.mean([pt[0] for pt in cluster]))
#     ym = int(np.mean([pt[1] for pt in cluster]))
#     x1 = int(np.mean([pt[2] for pt in cluster]))
#     y1 = int(np.mean([pt[3] for pt in cluster]))
#     x2 = int(np.mean([pt[4] for pt in cluster]))
#     y2 = int(np.mean([pt[5] for pt in cluster]))
#     merged_lines.append((xm, ym, x1, y1, x2, y2))

# print(f"🔍 Unique merged lines: {len(merged_lines)}")

# # -------------------- Step 6: Visualize Final Lines --------------------
# img_lines = img.copy()
# for (xm, ym, x1, y1, x2, y2) in merged_lines:
#     cv2.line(img_lines, (x1, y1), (x2, y2), (0, 255, 0), 2)
#     cv2.circle(img_lines, (xm, ym), 5, (0, 0, 255), -1)

# plt.figure(figsize=(12, 6))
# plt.imshow(cv2.cvtColor(img_lines, cv2.COLOR_BGR2RGB))
# plt.title('Merged Unique Lines')
# plt.axis('off')
# plt.show()

# # Save output image
# output_path = 'merged_lines_output.png'
# cv2.imwrite(output_path, img_lines)
# print(f"🖼️ Output image saved at: {os.path.abspath(output_path)}")

# # -------------------- Step 7: Compute Distances --------------------
# merged_lines.sort(key=lambda x: x[0])
# midpoints_x = [int(line[0]) for line in merged_lines]
# print("\n📌 Midpoint x-coordinates:")
# print(midpoints_x)

# pixel_distances = []
# for i in range(len(midpoints_x) - 1):
#     d = abs(midpoints_x[i + 1] - midpoints_x[i])
#     pixel_distances.append(d)
#     print(f"Line {i} to {i + 1}: {d:.2f} px")

# # -------------------- Step 8: Calibration --------------------
# cm_per_pixel = 0.0346  # You can change this scale based on your calibration
# print(f"\n✅ Initial Results:")
# print(f"  Total merged lines: {len(merged_lines)}")
# if pixel_distances:
#     avg_pixel_dist = np.mean(pixel_distances)
#     print(f"  Average pixel distance: {avg_pixel_dist:.2f} px")
#     print(f"  Physical distance: {avg_pixel_dist * cm_per_pixel:.2f} cm")
# else:
#     print("  Not enough lines to compute spacing.")

# # -------------------- Step 9: Clean Edge Lines --------------------
# if len(midpoints_x) > 2:
#     clean_midpoints_x = midpoints_x[1:-1]  # Remove first & last (likely borders)
# else:
#     clean_midpoints_x = midpoints_x

# print("\n🧼 Cleaned midpoint x-coordinates (after removing edges):")
# print(clean_midpoints_x)

# # Recalculate spacing
# clean_pixel_distances = []
# for i in range(len(clean_midpoints_x) - 1):
#     d = abs(clean_midpoints_x[i + 1] - clean_midpoints_x[i])
#     clean_pixel_distances.append(d)
#     print(f"Line {i} to {i + 1}: {d:.2f} px")

# # Final summary
# print(f"\n✅ Final Results (Excluding edge lines):")
# print(f"  Valid lines: {len(clean_midpoints_x)}")
# if clean_pixel_distances:
#     avg_clean_dist = np.mean(clean_pixel_distances)
#     print(f"  Average pixel distance: {avg_clean_dist:.2f} px")
#     print(f"  Physical distance: {avg_clean_dist * cm_per_pixel:.2f} cm")
# else:
#     print("  Not enough valid lines to compute spacing.")



# edit 5:
# this code is making proper lines for the edges but with horizontal as well 

import cv2
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import os

# Load the image
img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'
img = tiff.imread(img_path)
if img.ndim > 2:
    img = img[:, :, 0]

# Auto-stretch contrast using percentiles
min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
img_clipped = np.clip(img, min_val, max_val)
img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Show normalized image (optional)
plt.imshow(img_norm, cmap='gray')
plt.title("Normalized Image (Input to Canny)")
plt.axis('off')
plt.show()

# Apply Gaussian blur
blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)

# Canny edge detection (90, 170)
low, high = 90, 170
edges = cv2.Canny(blurred, low, high)

# Save Canny edge result
edges_path = os.path.join(os.path.dirname(img_path), 'my_image_edges_90_170.png')
cv2.imwrite(edges_path, edges)
print(f"Saved Canny edge image (90, 170) to: {edges_path}")

# Reload grayscale as BGR for drawing colored lines
img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)

# Hough Line detection on the same edges
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=50,
    maxLineGap=10
)

# Draw green lines if found
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(img_color, (x1, y1), (x2, y2), (0, 255, 0), 2)
    print(f"Detected and drew {len(lines)} lines.")
else:
    print("No lines were detected.")

# Save the image with green lines
output_line_path = os.path.join(os.path.dirname(img_path), 'my_image_edges_with_lines.png')
cv2.imwrite(output_line_path, img_color)
print(f"Saved image with green lines to: {output_line_path}")


# edit 6:

import cv2
import numpy as np
import tifffile as tiff
import matplotlib.pyplot as plt
import os
from math import atan2, degrees, sqrt

# ===== CONFIGURATION =====
img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\my_image_calibrated.tif'

canny_low = 90
canny_high = 170
angle_range = (55, 95)       # degrees
min_distance = 10            # min dist between lines in px

# ===== LOAD IMAGE =====
img = tiff.imread(img_path)
if img.ndim > 2:
    img = img[:, :, 0]

# Contrast stretching using percentiles
min_val, max_val = np.percentile(img, 2), np.percentile(img, 98)
img_clipped = np.clip(img, min_val, max_val)
img_norm = ((img_clipped - min_val) / (max_val - min_val) * 255).astype(np.uint8)

# Show input image
plt.imshow(img_norm, cmap='gray')
plt.title("Normalized Image (Input to Canny)")
plt.axis('off')
plt.show()

# ===== PREPROCESS =====
blurred = cv2.GaussianBlur(img_norm, (5, 5), 1.2)
edges = cv2.Canny(blurred, canny_low, canny_high)

# Show Canny edges
plt.imshow(edges, cmap='gray')
plt.title(f"Canny Edges ({canny_low}, {canny_high})")
plt.axis('off')
plt.show()

# Save edge image
edges_path = os.path.join(os.path.dirname(img_path), 'debug_edges.png')
cv2.imwrite(edges_path, edges)

# ===== FUNCTIONS =====
def compute_angle(x1, y1, x2, y2):
    angle_rad = atan2((y2 - y1), (x2 - x1))
    return degrees(angle_rad) % 180

def line_midpoint(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def euclidean_dist(p1, p2):
    return sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

# ===== LINE DETECTION =====
raw_lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=50,
    minLineLength=50,
    maxLineGap=10
)

# Color image for line drawing
img_color = cv2.cvtColor(img_norm, cv2.COLOR_GRAY2BGR)

# Debug counters
total_lines = 0
kept_lines = 0
filtered_lines = []

if raw_lines is not None:
    print(f"\n--- Total raw lines detected: {len(raw_lines)} ---\n")
    for line in raw_lines:
        x1, y1, x2, y2 = line[0]
        total_lines += 1
        angle = compute_angle(x1, y1, x2, y2)
        midpoint = line_midpoint(x1, y1, x2, y2)

        print(f"Line {total_lines}: ({x1},{y1}) → ({x2},{y2}) | Angle: {angle:.2f}°", end='')

        # Check angle
        if not (angle_range[0] <= angle <= angle_range[1]):
            print(" ❌ Rejected (angle out of range)")
            continue

        # Check distance to other kept lines
        too_close = False
        for kept in filtered_lines:
            kx1, ky1, kx2, ky2 = kept
            k_mid = line_midpoint(kx1, ky1, kx2, ky2)
            if euclidean_dist(midpoint, k_mid) < min_distance:
                too_close = True
                break

        if too_close:
            print(" ❌ Rejected (too close to another line)")
            continue

        # Keep the line
        filtered_lines.append((x1, y1, x2, y2))
        kept_lines += 1
        print(" ✅ Kept")
else:
    print("No lines detected at all.")

# ===== DRAW FILTERED LINES =====
for x1, y1, x2, y2 in filtered_lines:
    cv2.line(img_color, (x1, y1), (x2, y2), (0, 255, 0), 2)

print(f"\n✅ Final lines drawn: {kept_lines} out of {total_lines} detected.")

# Save output
output_path = os.path.join(os.path.dirname(img_path), 'my_image_filtered_lines_debug.png')
cv2.imwrite(output_path, img_color)
print(f"\n🟢 Saved final image with green lines to:\n{output_path}")
