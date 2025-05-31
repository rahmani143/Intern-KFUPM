# Absolutely! Here’s a **sample README.md** file you can upload to your project folder. It’s based on your requirements and script details.

# ---

# # FLIR Camera Image Acquisition

# **Welcome to the FLIR Camera Image Acquisition Project!**

# This script is designed to capture images from a FLIR camera using the PySpin library and FLIR Spinnaker SDK.

# ---

# ## 📌 Important Notes

# - **Storage Location:**  
#   Images are saved to:  
#   ```
#   C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images
#   ```
# - **Environment:**  
#   Due to storage issues with uploaded files, you must run this script in an environment with the required libraries installed (see below).
# - **Parent Files:**  
#   These files are taken from a parent project and are intended for use in environments where the FLIR SDK and required Python libraries are available.

# ---

# ## 🛠️ Requirements

# - **Python** (tested with Python 3.7+)
# - **PySpin** (FLIR's Python SDK interface, included with the FLIR Spinnaker SDK)
# - **FLIR Spinnaker SDK** (must be installed manually from [FLIR’s official site](https://www.flir.com/support-center/iis/machine-vision/))
# - **os** (built-in Python library)

# ---

# ## 🚀 How to Use

# 1. **Install Dependencies:**
#    - Download and install the [FLIR Spinnaker SDK](https://www.flir.com/support-center/iis/machine-vision/).
#    - Install the PySpin wrapper:
#      ```bash
#      pip install pyspin
#      ```
#    - (Note: On some systems, PySpin may be included with the SDK and not available via pip. In that case, use the SDK's provided PySpin.)

# 2. **Prepare the Environment:**
#    - Ensure your FLIR camera is connected and recognized by the system.
#    - Make sure the output directory exists:
#      ```python
#      SAVE_DIR = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images"
#      ```

# 3. **Run the Script:**
#    ```bash
#    python flir_test.py
#    ```

# 4. **Check Output:**
#    - Captured images will be saved in the specified directory.
#    - Each image is named as `Acquisition-{SerialNumber}-{Index}.jpg` (or `Acquisition-{Index}.jpg` if no serial number is found).

# ---

# ## ❓ Troubleshooting

# - **No cameras detected:**  
#   - Verify the FLIR SDK installation.
#   - Ensure the camera is properly connected and powered on.
#   - Check that no other applications are accessing the camera.
# - **Permission issues:**  
#   - Make sure the output directory is writable.
# - **Missing dependencies:**  
#   - Confirm that the FLIR Spinnaker SDK and PySpin are installed correctly.

# ---

# ## 📜 License

# This project is intended for internal use. Please refer to FLIR’s licensing terms for the Spinnaker SDK.

# ---

# **Happy imaging!** 📷✨

# ---






import os
import PySpin.PySpin

NUM_IMAGES = 400
SAVE_DIR = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def acquire_images(cam, nodemap, nodemap_tldevice):
    print('*** IMAGE ACQUISITION ***\n')
    try:
        # Set pixel format to Mono8 (if supported)
        node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        if PySpin.PySpin.IsAvailable(node_pixel_format) and PySpin.PySpin.IsWritable(node_pixel_format):
            node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
            if PySpin.PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.PySpin.IsReadable(node_pixel_format_mono8):
                pixel_format_mono8 = node_pixel_format_mono8.GetValue()
                node_pixel_format.SetIntValue(pixel_format_mono8)
                print("Pixel format set to Mono8.")
            else:
                print("Mono8 pixel format not available.")
                return False

        # Set acquisition mode to continuous
        node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        print('Acquisition mode set to continuous...')

        cam.BeginAcquisition()
        print('Acquiring images...')

        device_serial_number = ''
        node_device_serial_number = PySpin.PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()
            print('Device serial number retrieved as %s...' % device_serial_number)

        for i in range(NUM_IMAGES):
            image_result = cam.GetNextImage(1000)
            if image_result.IsIncomplete():
                print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
            else:
                width = image_result.GetWidth()
                height = image_result.GetHeight()
                print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))

                if device_serial_number:
                    filename = os.path.join(SAVE_DIR, f'Acquisition-{device_serial_number}-{i}.jpg')
                else:
                    filename = os.path.join(SAVE_DIR, f'Acquisition-{i}.jpg')

                # Save the image directly
                image_result.Save(filename)
                print(f'Image saved at {filename}')

            image_result.Release()
            print('')

        cam.EndAcquisition()

    except PySpin.PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
        try:
            cam.EndAcquisition()
        except:
            pass
        return False

    return True

# Standard initialization and cleanup code here


if __name__ == "__main__":
    system = PySpin.PySpin.System.GetInstance()
    print("system found")
    cam_list = system.GetCameras()
    if cam_list.GetSize() == 0:
        print("No cameras detected.")
        system.ReleaseInstance()
        exit()

    cam = cam_list.GetByIndex(0)
    cam.Init()
    nodemap = cam.GetNodeMap()
    nodemap_tldevice = cam.GetTLDeviceNodeMap()

    acquire_images(cam, nodemap, nodemap_tldevice)

    cam.DeInit()
    del cam
    cam_list.Clear()
    system.ReleaseInstance()
