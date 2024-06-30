import pyzed.sl as sl
import cv2
import numpy
import os



def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Use ULTRA depth mode
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Use meter units (for depth measurements)

    # Open the camera
    status = zed.open(init_params)
    if status != sl.ERROR_CODE.SUCCESS: #Ensure the camera has opened succesfully
        print("Camera Open : "+repr(status)+". Exit program.")
        exit()

    cam_info = zed.get_camera_information()
    cam_res = cam_info.camera_configuration.resolution

    # Create an RGBA sl.Mat object
    image_zed = sl.Mat(cam_res.width, cam_res.height, sl.MAT_TYPE.U8_C4)
    # Retrieve data in a numpy array with get_data()
    # image_ocv = image_zed.get_data()

    key = ' '
    while key != 123:
        if zed.grab() == sl.ERROR_CODE.SUCCESS :
            # Retrieve the left image in sl.Mat
            zed.retrieve_image(image_zed, sl.VIEW.RIGHT)
            # Use get_data() to get the numpy array
            image_ocv = image_zed.get_data()
            # Display the left image from the numpy array
            cv2.imshow("Image", image_ocv)

        key = cv2.waitKey(10)
    
    # Kamerayı kapatın ve kaynakları serbest bırakın
    zed.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

