# import os
# import sys
# import PySpin.PySpin
# import cv2
# import numpy as np

# def stream_video(cam, nodemap):
#     try:
#         # Set pixel format to Mono8 (same as your original)
#         node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
#         if PySpin.PySpin.IsAvailable(node_pixel_format) and PySpin.PySpin.IsWritable(node_pixel_format):
#             node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
#             if PySpin.PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.PySpin.IsReadable(node_pixel_format_mono8):
#                 pixel_format_mono8 = node_pixel_format_mono8.GetValue()
#                 node_pixel_format.SetIntValue(pixel_format_mono8)
#                 print("Pixel format set to Mono8.")
#             else:
#                 print("Mono8 pixel format not available.")
#                 return

#         # Set acquisition mode to continuous
#         node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
#         node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#         acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
#         node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
#         print('Acquisition mode set to continuous...')

#         cam.BeginAcquisition()
#         print('Streaming video... Press "q" to quit.')

#         window_name = 'FLIR Live View'
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#         cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

#         while True:
#             image_result = cam.GetNextImage(1000)

#             if image_result.IsIncomplete():
#                 print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#                 continue

#             image_data = image_result.GetNDArray()
#             image_result.Release()

#             if image_data is not None:
#                 screen_res = (1920, 1080)  # Adjust this to your actual screen resolution
#                 image_resized = cv2.resize(image_data, screen_res, interpolation=cv2.INTER_LINEAR)
#                 cv2.imshow(window_name, image_resized)

#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break

#         cam.EndAcquisition()
#         cv2.destroyAllWindows()

#     except PySpin.PySpin.SpinnakerException as ex:
#         print("Spinnaker Exception: %s" % ex)
#         try:
#             cam.EndAcquisition()
#         except:
#             pass

# if __name__ == "__main__":
#     system = PySpin.PySpin.System.GetInstance()
#     print("System initialized")

#     cam_list = system.GetCameras()
#     if cam_list.GetSize() == 0:
#         print("No cameras detected.")
#         system.ReleaseInstance()
#         exit()

#     cam = cam_list.GetByIndex(0)
#     cam.Init()
#     nodemap = cam.GetNodeMap()

#     stream_video(cam, nodemap)

#     cam.DeInit()
#     del cam
#     cam_list.Clear()
#     system.ReleaseInstance()


# Edit 2

# import os
# import sys
# import PySpin.PySpin
# import cv2
# import numpy as np
# import datetime  # <-- added

# def stream_video(cam, nodemap):
#     try:
#         # Set pixel format to Mono8 (same as your original)
#         node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
#         if PySpin.PySpin.IsAvailable(node_pixel_format) and PySpin.PySpin.IsWritable(node_pixel_format):
#             node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
#             if PySpin.PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.PySpin.IsReadable(node_pixel_format_mono8):
#                 pixel_format_mono8 = node_pixel_format_mono8.GetValue()
#                 node_pixel_format.SetIntValue(pixel_format_mono8)
#                 print("Pixel format set to Mono8.")
#             else:
#                 print("Mono8 pixel format not available.")
#                 return

#         # Set acquisition mode to continuous
#         node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
#         node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
#         acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
#         node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
#         print('Acquisition mode set to continuous...')

#         cam.BeginAcquisition()
#         print('Streaming video... Press "q" to quit, "s" to save.')

#         window_name = 'FLIR Live View'
#         cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
#         cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

#         save_dir = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image"
#         os.makedirs(save_dir, exist_ok=True)  # <-- create directory if it doesn't exist

#         while True:
#             image_result = cam.GetNextImage(1000)

#             if image_result.IsIncomplete():
#                 print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
#                 continue

#             image_data = image_result.GetNDArray()
#             image_result.Release()

#             if image_data is not None:
#                 screen_res = (1920, 1080)  # Adjust this to your actual screen resolution
#                 image_resized = cv2.resize(image_data, screen_res, interpolation=cv2.INTER_LINEAR)
#                 cv2.imshow(window_name, image_resized)

#             key = cv2.waitKey(1) & 0xFF
#             if key == ord('q'):
#                 break
#             elif key == ord('s'):
#                 timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#                 save_path = os.path.join(save_dir, f"best_image_{timestamp}.tiff")
#                 cv2.imwrite(save_path, image_data)  # <-- save original (not resized) image
#                 print(f"Saved image to {save_path}")

#         cam.EndAcquisition()
#         cv2.destroyAllWindows()

#     except PySpin.PySpin.SpinnakerException as ex:
#         print("Spinnaker Exception: %s" % ex)
#         try:
#             cam.EndAcquisition()
#         except:
#             pass

# if __name__ == "__main__":
#     system = PySpin.PySpin.System.GetInstance()
#     print("System initialized")

#     cam_list = system.GetCameras()
#     if cam_list.GetSize() == 0:
#         print("No cameras detected.")
#         system.ReleaseInstance()
#         exit()

#     cam = cam_list.GetByIndex(0)
#     cam.Init()
#     nodemap = cam.GetNodeMap()

#     stream_video(cam, nodemap)

#     cam.DeInit()
#     del cam
#     cam_list.Clear()
#     system.ReleaseInstance()


# edit 3


import os
import sys
import PySpin.PySpin
import cv2
import numpy as np
import datetime

def stream_video(cam, nodemap):
    try:
        # Set pixel format to Mono8
        node_pixel_format = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('PixelFormat'))
        if PySpin.PySpin.IsAvailable(node_pixel_format) and PySpin.PySpin.IsWritable(node_pixel_format):
            node_pixel_format_mono8 = node_pixel_format.GetEntryByName('Mono8')
            if PySpin.PySpin.IsAvailable(node_pixel_format_mono8) and PySpin.PySpin.IsReadable(node_pixel_format_mono8):
                pixel_format_mono8 = node_pixel_format_mono8.GetValue()
                node_pixel_format.SetIntValue(pixel_format_mono8)
                print("Pixel format set to Mono8.")
            else:
                print("Mono8 pixel format not available.")
                return

        # Set acquisition mode to continuous
        node_acquisition_mode = PySpin.PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
        node_acquisition_mode_continuous = node_acquisition_mode.GetEntryByName('Continuous')
        acquisition_mode_continuous = node_acquisition_mode_continuous.GetValue()
        node_acquisition_mode.SetIntValue(acquisition_mode_continuous)
        print('Acquisition mode set to continuous...')

        cam.BeginAcquisition()
        print('Streaming video... Press "q" to quit, "s" to save.')

        window_name = 'FLIR Live View'
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL)

        save_dir = r"C:\Users\bss10\OneDrive\Desktop\camera_env\aquired_images\best_image\spectral_calibration\960nm"
        os.makedirs(save_dir, exist_ok=True)

        show_msg = False
        msg_timer = 0
        msg_text = ""

        while True:
            image_result = cam.GetNextImage(1000)

            if image_result.IsIncomplete():
                print('Image incomplete with image status %d ...' % image_result.GetImageStatus())
                continue

            image_data = image_result.GetNDArray()
            image_result.Release()

            if image_data is not None:
                screen_res = (1920, 1080)
                image_resized = cv2.resize(image_data, screen_res, interpolation=cv2.INTER_LINEAR)

                if show_msg and (cv2.getTickCount() - msg_timer < 2 * cv2.getTickFrequency()):
                    cv2.putText(image_resized, msg_text, (50, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2, cv2.LINE_AA)

                cv2.imshow(window_name, image_resized)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('s'):
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(save_dir, f"best_image_{timestamp}.tiff")
                cv2.imwrite(save_path, image_data)
                msg_text = f"Saved: {save_path}"
                print(msg_text)
                show_msg = True
                msg_timer = cv2.getTickCount()

        cam.EndAcquisition()
        cv2.destroyAllWindows()

    except PySpin.PySpin.SpinnakerException as ex:
        print("Spinnaker Exception: %s" % ex)
        try:
            cam.EndAcquisition()
        except:
            pass

if __name__ == "__main__":
    system = PySpin.PySpin.System.GetInstance()
    print("System initialized")

    cam_list = system.GetCameras()
    if cam_list.GetSize() == 0:
        print("No cameras detected.")
        system.ReleaseInstance()
        exit()

    cam = cam_list.GetByIndex(0)

    
    cam.Init()

    cam.ExposureAuto.SetValue(PySpin.PySpin.ExposureAuto_Off)

    # Set exposure time to 10000 microseconds (10 milliseconds)
    exposure_time_us = 12117.14744
    cam.ExposureTime.SetValue(exposure_time_us)
    print(f"Exposure time set to {exposure_time_us} microseconds")
    nodemap = cam.GetNodeMap()

    stream_video(cam, nodemap)

    cam.DeInit()
    del cam
    cam_list.Clear()
    system.ReleaseInstance()
