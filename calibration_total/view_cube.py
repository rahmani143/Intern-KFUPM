import napari
import numpy as np

# Load your hyperspectral cube
cube_path = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\hsi_cube_spectral_trial\test1.npy'
cube = np.load(cube_path)  # shape: (spectral, x, band)

# You may want to transpose to (Z, Y, X) if needed:
# cube.shape = (600, width, num_images)
# For napari: (slices, height, width) is best
cube_for_napari = np.transpose(cube, (2, 1, 0))  # shape: (bands, x, spectral)

# Launch napari viewer
viewer = napari.Viewer()
viewer.add_image(cube_for_napari, name='HSI Cube', colormap='gray')
napari.run()
