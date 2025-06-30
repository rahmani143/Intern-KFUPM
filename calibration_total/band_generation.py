import re
import csv
import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial import Polynomial

# === CONFIG ===
input_file = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\max_intensity\ignore_max_intensity_points_spectral_total.csv"
output_csv = "pixel_to_wavelength.csv"
output_plot = "calibration_curve.png"

# === Step 1: Parse the file into wavelength blocks ===
wavelengths = []
mean_columns = []

with open(input_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

current_block = []
current_wavelength = None

for line in lines:
    line = line.strip()

    # Detect new wavelength section
    match = re.match(r"wavelength\s*=\s*(\d+)\s*nm", line.lower())
    if match:
        # Process previous block if exists
        if current_block and current_wavelength:
            try:
                reader = csv.reader(current_block)
                headers = next(reader)
                # Find index of "column" header
                if "column" not in headers:
                    raise ValueError(f"'column' header not found in block for {current_wavelength}nm")
                col_idx = headers.index("column")

                columns = []
                for row in reader:
                    if len(row) > col_idx and row[col_idx].isdigit():
                        columns.append(int(row[col_idx]))

                if columns:
                    mean_col = np.mean(columns)
                    wavelengths.append(float(current_wavelength))
                    mean_columns.append(mean_col)
                else:
                    print(f"[!] No valid 'column' values found for {current_wavelength}nm")
            except Exception as e:
                print(f"[!] Error processing block for {current_wavelength}nm: {e}")

        # Start new block for new wavelength
        current_wavelength = match.group(1)
        current_block = []
    else:
        # Append line as string (not split!) to current block if not empty
        if line:
            current_block.append(line)

# Process the last block after file ends
if current_block and current_wavelength:
    try:
        reader = csv.reader(current_block)
        headers = next(reader)
        if "column" not in headers:
            raise ValueError(f"'column' header not found in block for {current_wavelength}nm")
        col_idx = headers.index("column")

        columns = []
        for row in reader:
            if len(row) > col_idx and row[col_idx].isdigit():
                columns.append(int(row[col_idx]))

        if columns:
            mean_col = np.mean(columns)
            wavelengths.append(float(current_wavelength))
            mean_columns.append(mean_col)
        else:
            print(f"[!] No valid 'column' values found for {current_wavelength}nm")
    except Exception as e:
        print(f"[!] Error processing final block for {current_wavelength}nm: {e}")

# Check if data is sufficient for fitting
if len(wavelengths) < 2 or len(mean_columns) < 2:
    raise RuntimeError("Not enough calibration points to fit polynomial.")

# === Step 2: Fit polynomial curve ===
mean_columns = np.array(mean_columns)
wavelengths = np.array(wavelengths)

fit = Polynomial.fit(mean_columns, wavelengths, deg=2)
calibration_curve = fit.convert()

# === Step 3: Generate band-to-wavelength mapping ===
bands = np.arange(200)
mapped_wavelengths = calibration_curve(bands)

with open(output_csv, "w", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Band", "Wavelength (nm)"])
    for band, wl in zip(bands, mapped_wavelengths):
        writer.writerow([band, round(wl, 2)])

print(f"[✓] Saved band-to-wavelength mapping to {output_csv}")

# === Step 4: Plot calibration ===
plt.figure(figsize=(8, 5))
plt.plot(bands, mapped_wavelengths, label="Fitted Curve")
plt.scatter(mean_columns, wavelengths, color='red', label="Calibration Points")
plt.xlabel("Band Index (Mean Column)")
plt.ylabel("Wavelength (nm)")
plt.title("Band-to-Wavelength Calibration Curve")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(output_plot)
plt.show()

print(f"[✓] Saved plot to {output_plot}")
