import os
import numpy as np
from PIL import Image
import glob
import cv2

def mean_image(image_folder, output_folder, out_filename):
    os.makedirs(output_folder, exist_ok=True)
    out_filepath = os.path.join(output_folder, out_filename)

    imlist = [os.path.join(image_folder, fname) for fname in os.listdir(image_folder)
              if fname.lower().endswith(('.png', '.tif', '.tiff', '.jpg', '.jpeg'))]
    N = len(imlist)
    if N == 0:
        raise ValueError("No images found in folder: " + image_folder)

    w, h = Image.open(imlist[0]).size
    arr = np.zeros((h, w), np.float32)

    for imfile in imlist:
        imarr = np.array(Image.open(imfile).convert('L'), dtype=np.float32)
        arr += imarr / N

    arr = np.round(arr).astype(np.uint16)
    out = Image.fromarray(arr)
    out.save(out_filepath)
    print(f"Mean image saved: {out_filepath}")

def mean_white_region(image_folder, output_folder, out_filename, threshold=40):
    os.makedirs(output_folder, exist_ok=True)
    imlist = glob.glob(os.path.join(image_folder, '*.jpg'))
    N = len(imlist)
    if N == 0:
        raise ValueError("No images found in folder: " + image_folder)

    with Image.open(imlist[0]) as im:
        im = im.convert('L')
        w, h = im.size
        arr = np.zeros((h, w), np.float32)
        mask_total = np.zeros((h, w), np.float32)

    for imfile in imlist:
        with Image.open(imfile) as im:
            im = im.convert('L').resize((w, h))
            imarr = np.array(im, dtype=np.float32)
            mask = imarr > threshold
            arr += imarr * mask
            mask_total += mask

    mask_total[mask_total == 0] = 1
    mean_arr = arr / mask_total

    mean_arr_uint8 = np.round(mean_arr).astype(np.uint8)
    out = Image.fromarray(mean_arr_uint8)
    out_filepath = os.path.join(output_folder, out_filename)
    out.save(out_filepath)
    print(f"Masked mean white image saved: {out_filepath}")

    mean_value = mean_arr[mask_total > 1].mean()
    print(f"Mean white region intensity: {mean_value}")

def calibrate_images(scene_folder, output_folder, mean_black_path, mean_white_path):
    os.makedirs(output_folder, exist_ok=True)

    mean_black = np.array(Image.open(mean_black_path).convert('L')).astype(np.float32)
    mean_white = np.array(Image.open(mean_white_path).convert('L')).astype(np.float32)

    scene_files = glob.glob(os.path.join(scene_folder, '*.jpg'))

    for filepath in scene_files:
        with Image.open(filepath) as im:
            im = im.convert('L')
            imarr = np.array(im, dtype=np.float32)

            if mean_black.shape != imarr.shape:
                mean_black_resized = cv2.resize(mean_black, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)
                mean_white_resized = cv2.resize(mean_white, (imarr.shape[1], imarr.shape[0]), interpolation=cv2.INTER_LINEAR)
            else:
                mean_black_resized = mean_black
                mean_white_resized = mean_white

            denominator = mean_white_resized - mean_black_resized
            denominator[denominator == 0] = 1
            calibrated = (imarr - mean_black_resized) / denominator
            calibrated = np.clip(calibrated, 0, 1)

            base_name = os.path.basename(filepath)
            out_tif = os.path.join(output_folder, base_name).replace('.jpg', '.tif')

            Image.fromarray((calibrated * 65535).astype(np.uint16)).save(out_tif)

            print(f"Saved calibrated TIFF: {out_tif}")


# === USER SETTINGS ===

root = r'C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images'
output_dir = os.path.join(root, 'output')
calibrated_dir = os.path.join(root, 'calibrated radiometric')

mean_image(
    os.path.join(root, 'radiometric_black'),
    output_dir,
    'mean_black.tif'
)

mean_image(
    os.path.join(root, 'radiometric_white'),
    output_dir,
    'mean_white.tif'
)

mean_white_region(
    os.path.join(root, 'radiometric_white'),
    output_dir,
    'mean_white_masked.jpg',
    threshold=30
)

calibrate_images(
    root,
    calibrated_dir,
    os.path.join(output_dir, 'mean_black.tif'),
    os.path.join(output_dir, 'mean_white_masked.jpg')
)
