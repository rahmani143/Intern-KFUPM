# import os
# import PySpin.PySpin

# NUM_IMAGES = 400
# SAVE_DIR = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images"
# os.makedirs(SAVE_DIR, exist_ok=True)

# def acquire_images(cam, nodemap, nodemap_tldevice):
#     print('*** IMAGE ACQUISITION ***\n')
#     try:
#         # Set pixel format to Mono8 (if supported)
#         node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
#         if PySpin.PySpin.IsAvailable(node_pixel_format) and PySpin.PySpin.IsWritable(node_pixel_format):
#             node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
#             if PySpin.PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.PySpin.IsReadable(node_pixel_format_mono8):
#                 pixel_format_mono8 = node_pixel_format_mono8.GetValue()
#                 node_pixel_format.SetIntValue(pixel_format_mono8)
#                 print("Pixel format set to Mono8.")
#             else:
#                 print("Mono8 pixel format not available.")
#                 return False

#         # Set acquisition mode to continuous
#         node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
#         node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#         acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
#         node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
#         print('Acquisition mode set to continuous...')

#         cam.BeginAcquisition()
#         print('Acquiring images...')

#         device_serial_number = ''
#         node_device_serial_number = PySpin.PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
#         if PySpin.PySpin.IsReadable(node_device_serial_number):
#             device_serial_number = node_device_serial_number.GetValue()
#             print('Device serial number retrieved as %s...' % device_serial_number)

#         for i in range(NUM_IMAGES):
#             image_result = cam.GetNextImage(1000)
#             if image_result.IsIncomplete():
#                 print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#             else:
#                 width = image_result.GetWidth()
#                 height = image_result.GetHeight()
#                 print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))

#                 if device_serial_number:
#                     filename = os.path.join(SAVE_DIR, f'Acquisition-{device_serial_number}-{i}.jpg')
#                 else:
#                     filename = os.path.join(SAVE_DIR, f'Acquisition-{i}.jpg')

#                 # Save the image directly
#                 image_result.Save(filename)
#                 print(f'Image saved at {filename}')

#             image_result.Release()
#             print('')

#         cam.EndAcquisition()

#     except PySpin.PySpin.SpinnakerException as ex:
#         print('Error: %s' % ex)
#         try:
#             cam.EndAcquisition()
#         except:
#             pass
#         return False

#     return True

# # Standard initialization and cleanup code here


# if __name__ == "__main__":
#     system = PySpin.PySpin.System.GetInstance()
#     print("system found")
#     cam_list = system.GetCameras()
#     if cam_list.GetSize() == 0:
#         print("No cameras detected.")
#         system.ReleaseInstance()
#         exit()

#     cam = cam_list.GetByIndex(0)
#     cam.Init()
#     nodemap = cam.GetNodeMap()
#     nodemap_tldevice = cam.GetTLDeviceNodeMap()

#     acquire_images(cam, nodemap, nodemap_tldevice)

#     cam.DeInit()
#     del cam
#     cam_list.Clear()
#     system.ReleaseInstance()


import os
import sys
import PySpin.PySpin

# Get number of images from command line argument, default to 400
if len(sys.argv) > 1:
    try:
        NUM_IMAGES = int(sys.argv[1])
    except ValueError:
        NUM_IMAGES = 400
else:
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
