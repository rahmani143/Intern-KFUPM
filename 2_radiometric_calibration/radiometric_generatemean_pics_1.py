import os
import numpy as np
from PIL import Image

def mean_image(image_folder, output_folder, out_filename):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    out_filepath = os.path.join(output_folder, out_filename)

    # List all image files in the folder (adjust extension as needed)
    imlist = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder)
              if fname.lower().endswith(('.png', '.tif', '.tiff', '.jpg', '.jpeg'))]
    N = len(imlist)
    if N == 0:
        raise ValueError("No images found in folder: " + image_folder)
    
    # Open first image to get dimensions
    w, h = Image.open(imlist[0]).size
    arr = np.zeros((h, w), np.float32)  # For grayscale; use (h, w, 3) for RGB
    
    # Sum up all images
    for imfile in imlist:
        imarr = np.array(Image.open(imfile), dtype=np.float32)
        arr += imarr / N
    
    # Convert to uint16 and save
    arr = np.round(arr).astype(np.uint16)
    out = Image.fromarray(arr)
    out.save(out_filepath)
    print(f"Mean image saved as {out_filepath}")

# Example usage:
mean_image(
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\radiometric_black',
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\output',
    'mean_black.tif'
)
mean_image(
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\radiometric_white',
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\output',
    'mean_white.tif'
)
