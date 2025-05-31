import PySpin

NUM_IMAGES = 10  # Number of images to acquire

def acquire_images():
    # Initialize system
    system = PySpin.System.GetInstance()
    cam_list = system.GetCameras()
    
    if cam_list.GetSize() == 0:
        print("No cameras detected.")
        system.ReleaseInstance()
        return

    cam = cam_list.GetByIndex(0)

    try:
        # Initialize camera
        cam.Init()
        nodemap = cam.GetNodeMap()
        nodemap_tldevice = cam.GetTLDeviceNodeMap()

        # Set acquisition mode to continuous
        node_acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        print("Acquisition mode set to continuous.")

        # Start acquisition
        cam.BeginAcquisition()
        print("Acquiring images...")

        # Get device serial number for unique file names
        device_serial_number = ""
        node_device_serial_number = PySpin.CStringPtr(nodemap_tldevice.GetNode('DeviceSerialNumber'))
        if PySpin.IsReadable(node_device_serial_number):
            device_serial_number = node_device_serial_number.GetValue()

        processor = PySpin.ImageProcessor()
        processor.SetColorProcessing(PySpin.SPINNAKER_COLOR_PROCESSING_ALGORITHM_HQ_LINEAR)

        for i in range(NUM_IMAGES):
            image_result = cam.GetNextImage(1000)
            if image_result.IsIncomplete():
                print(f"Image {i} incomplete with status {image_result.GetImageStatus()}")
            else:
                image_converted = processor.Convert(image_result, PySpin.PixelFormat_Mono8)
                filename = f"Acquisition-{device_serial_number}-{i}.jpg" if device_serial_number else f"Acquisition-{i}.jpg"
                image_converted.Save(filename)
                print(f"Saved {filename}")
            image_result.Release()

        cam.EndAcquisition()
        print("Image acquisition complete.")

        # Deinitialize camera
        cam.DeInit()
    except PySpin.SpinnakerException as ex:
        print(f"PySpin error: {ex}")
    finally:
        del cam
        cam_list.Clear()
        system.ReleaseInstance()

if __name__ == "__main__":
    acquire_images()
