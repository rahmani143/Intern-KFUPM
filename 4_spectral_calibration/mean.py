# import os
# import numpy as np
# from PIL import Image

# def mean_image(image_folder, output_folder, out_filename):
#     # Create output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)
#     out_filepath = os.path.join(output_folder, out_filename)

#     # List all image files in the folder (adjust extension as needed)
#     imlist = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder)
#               if fname.lower().endswith(('.png', '.tif', '.tiff', '.jpg', '.jpeg'))]
#     N = len(imlist)
#     if N == 0:
#         raise ValueError("No images found in folder: " + image_folder)
    
#     # Open first image to get dimensions
#     w, h = Image.open(imlist[0]).size
#     arr = np.zeros((h, w), np.float32)  # For grayscale; use (h, w, 3) for RGB
    
#     # Sum up all images
#     for imfile in imlist:
#         imarr = np.array(Image.open(imfile), dtype=np.float32)
#         arr += imarr / N
    
#     # Convert to uint16 and save
#     arr = np.round(arr).astype(np.uint16)
#     out = Image.fromarray(arr)
#     out.save(out_filepath)
#     print(f"Mean image saved as {out_filepath}")

# # Example usage:
# mean_image(
#     'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\spectral_calibration\\1000nm',
#     'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\spectral_calibration\\1000nm',
#     '1000_mean.tif'
# )



# edit 2:

# # Load one representative image
# img_path = glob.glob('aquired_images//radiometric_white//Acquisition-20474040-0.jpg')[0]
# img = np.array(Image.open(img_path))
# plt.hist(img.flatten(), bins=256)
# plt.title("Histogram of Pixel Intensities")
# plt.xlabel("Pixel Value")
# plt.ylabel("Frequency")
# plt.show()





import os
import numpy as np
from PIL import Image
import glob

import os
import numpy as np
from PIL import Image
import glob

def mean_white_region(image_folder, output_folder, out_filename, threshold=20):
    os.makedirs(output_folder, exist_ok=True)
    imlist = glob.glob(os.path.join(image_folder, '*.tiff'))
    N = len(imlist)
    if N == 0:
        raise ValueError("No images found in folder: " + image_folder)
    
    # Open first image to get target size
    with Image.open(imlist[0]) as im:
        im = im.convert('L')  # Convert to grayscale
        w, h = im.size
        arr = np.zeros((h, w), np.float32)
        mask_total = np.zeros((h, w), np.float32)

    for imfile in imlist:
        with Image.open(imfile) as im:
            im = im.convert('L')  # Ensure grayscale
            im = im.resize((w, h))  # Ensure same size
            imarr = np.array(im, dtype=np.float32)
            mask = imarr > threshold
            arr += imarr * mask
            mask_total += mask

    # Avoid division by zero
    mask_total[mask_total == 0] = 1
    mean_arr = arr / mask_total

    # Save as uint8 image (for visualization, though values will be low)
    mean_arr_uint8 = np.round(mean_arr).astype(np.uint8)
    out = Image.fromarray(mean_arr_uint8)
    out_filepath = os.path.join(output_folder, out_filename)
    out.save(out_filepath)
    print(f"Mean white region image saved as {out_filepath}")

    # If you want the mean value of the white region (for calibration):
    mean_value = mean_arr[mask_total > 1].mean()
    print(f"Mean intensity value of white region across all images: {mean_value}")

# Example usage:
mean_white_region(
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\spectral_calibration\\1000nm',
    'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\best_image\\spectral_calibration\\1000nm',
    '1000_mean.tif',
    threshold=20  # Use the threshold that worked for your single image
)






# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt

# img_path = 'C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images\\radiometric_white\\Acquisition-20474040-0.jpg'
# im = Image.open(img_path).convert('L')
# imarr = np.array(im, dtype=np.float32)

# threshold = 30  # Try 25, 30, 35
# mask = imarr > threshold

# plt.imshow(imarr, cmap='gray')
# plt.title('Original Image')
# plt.show()

# plt.imshow(mask, cmap='gray')
# plt.title(f'Mask with threshold {threshold}')
# plt.show()
