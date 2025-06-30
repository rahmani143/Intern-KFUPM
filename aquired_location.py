# import os
# import PySpin
# import PySpin.PySpin



# NUM_IMAGES = 10  # Number of images to acquire
# SAVE_DIR = r"C:\\Users\bss10\\OneDrive\Desktop\\camera_env\\aquired_images"

# print(os.makedirs(SAVE_DIR, exist_ok=True))

# def acquire_images(cam, nodemap, nodemap_tldevice):
#     print('*** IMAGE ACQUISITION ***\n')
#     try:
#         result = True

#         # Ensure save directory exists
#         if not os.path.exists(SAVE_DIR):
#             os.makedirs(SAVE_DIR)

#         # Set acquisition mode to continuous
#         node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
#         if not PySpin.PySpin.IsReadable(node_acquisition_mode) or not PySpin.PySpin.IsWritable(node_acquisition_mode):
#             print('Unable to set acquisition mode to continuous (enum retrieval). Aborting...')
#             return False

#         node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#         if not PySpin.PySpin.IsReadable(node_acquisition_mode_continuous):
#             print('Unable to set acquisition mode to continuous (entry retrieval). Aborting...')
#             return False

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

#         processor = PySpin.PySpin.ImageProcessor()
#         processor.SetColorProcessing(PySpin.PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)

#         for i in range(NUM_IMAGES):
#             try:
#                 image_result = cam.GetNextImage(1000)
#                 if image_result.IsIncomplete():
#                     print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#                 else:
#                     width = image_result.GetWidth()
#                     height = image_result.GetHeight()
#                     print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))

#                     image_converted = processor.Convert(image_result, PySpin.PixelFormat_Mono8)

#                     # Create a unique filename in the desired directory
#                     if device_serial_number:
#                         filename = os.path.join(SAVE_DIR, f'Acquisition-{device_serial_number}-{i}.jpg')
#                     else:
#                         filename = os.path.join(SAVE_DIR, f'Acquisition-{i}.jpg')

#                     image_converted.Save(filename)
#                     print(f'Image saved at {filename}')

#                     image_result.Release()
#                     print('')

#             except PySpin.PySpin.SpinnakerException as ex:
#                 print('Error: %s' % ex)
#                 return False

#         cam.EndAcquisition()

#     except PySpin.PySpin.SpinnakerException as ex:
#         print('Error: %s' % ex)
#         return False

#     return result

# if __name__ == "__main__":
#     # Initialize system and camera
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

#     # Call your acquire_images function
#     acquire_images(cam, nodemap, nodemap_tldevice)

#     # Cleanup
#     cam.DeInit()
#     del cam
#     cam_list.Clear()
#     system.ReleaseInstance()







import os
import PySpin

NUM_IMAGES = 10
SAVE_DIR = r"C:\\Users\\bss10\\OneDrive\\Desktop\\camera_env\\aquired_images"
os.makedirs(SAVE_DIR, exist_ok=True)

def acquire_images(cam, nodemap, nodemap_tldevice):
    print('*** IMAGE ACQUISITION ***\n')
    try:
        # Set pixel format to Mono8
        node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
        pixel_format_mono8 = node_pixel_format_mono8.GetValue()
        node_pixel_format.SetIntValue(pixel_format_mono8)
        print("Camera pixel format set to Mono8.")

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

        processor = PySpin.PySpin.ImageProcessor()
        processor.SetColorProcessing(PySpin.PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)

        for i in range(NUM_IMAGES):
            try:
                image_result = cam.GetNextImage(1000)
                if image_result.IsIncomplete():
                    print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                else:
                    width = image_result.GetWidth()
                    height = image_result.GetHeight()
                    print('Grabbed Image %d, width = %d, height = %d' % (i, width, height))

                    image_converted = processor.Convert(image_result, pixel_format_mono8)

                    if device_serial_number:
                        filename = os.path.join(SAVE_DIR, f'Acquisition-{device_serial_number}-{i}.jpg')
                    else:
                        filename = os.path.join(SAVE_DIR, f'Acquisition-{i}.jpg')

                    image_converted.Save(filename)
                    print(f'Image saved at {filename}')

                image_result.Release()
                print('')

            except PySpin.PySpin.SpinnakerException as ex:
                print('Error: %s' % ex)
                return False

        cam.EndAcquisition()

    except PySpin.PySpin.SpinnakerException as ex:
        print('Error: %s' % ex)
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
