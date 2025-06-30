import os
import cv2
import pandas as pd
import matplotlib.pyplot as plt

def plot_points_on_images(tiff_folder, csv_folder, output_folder=None, show_images=True):
    if output_folder:
        os.makedirs(output_folder, exist_ok=True)

    tiff_files = [f for f in os.listdir(tiff_folder) if f.lower().endswith('.tif')]

    for tiff_file in tiff_files:
        base_name = os.path.splitext(tiff_file)[0]
        csv_file = os.path.join(csv_folder, base_name + '.csv')
        tiff_path = os.path.join(tiff_folder, tiff_file)

        if not os.path.exists(csv_file):
            print(f"CSV file not found for {tiff_file}, skipping...")
            continue

        img = cv2.imread(tiff_path)
        if img is None:
            print(f"Could not read image {tiff_path}, skipping...")
            continue

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        df = pd.read_csv(csv_file)
        
        # Check columns and load coords
        if {'row', 'column'}.issubset(df.columns):
            ys = df['row'].values
            xs = df['column'].values
        elif {'y', 'x'}.issubset(df.columns):
            ys = df['y'].values
            xs = df['x'].values
        else:
            print(f"CSV {csv_file} missing expected coordinate columns, skipping...")
            continue

        print(f"Image: {tiff_file} shape: {img.shape}")
        print(f"Points count: {len(xs)}")
        print(f"X range: {xs.min()} - {xs.max()}")
        print(f"Y range: {ys.min()} - {ys.max()}")

        plt.figure(figsize=(10, 10))
        plt.imshow(img_rgb)
        plt.scatter(xs, ys, c='red', s=50, marker='o', edgecolors='black', linewidth=0.5)
        plt.title(f"Points over Image: {tiff_file}")
        plt.axis('off')

        if output_folder:
            output_path = os.path.join(output_folder, base_name + '_with_points.png')
            plt.savefig(output_path, bbox_inches='tight')
            print(f"Saved image with points to {output_path}")

        if show_images:
            plt.show()
            plt.pause(0.1)
        else:
            plt.close()

# Usage example with your paths:
tiff_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity"
csv_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\csv_output"
output_folder = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\plotted_lines_coordinates"

plot_points_on_images(tiff_folder, csv_folder, output_folder=output_folder, show_images=True)


print("All images processed.")