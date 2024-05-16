import pyzed.sl as sl
import os
import cv2


def main():
    # Create a Camera object
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 opr HD1200 video mode, depending on camera type.
    init_params.camera_fps = 30  # Set fps at 30

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()


    # Capture 50 frames and stop
    i = 0
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()

    if not os.path.exists("/home/moveon2/Desktop/Desktop1/All-Projects/Python-project/StereoCamera-Explorer/tutorials/tutorial 2 - image capture/python/DATA"):
        os.makedirs("DATA")
        print("Data directory created")

    while i < 50:
        # Grab an image, a RuntimeParameters object must be given to grab()
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # A new image is available if grab() returns SUCCESS
            zed.retrieve_image(image, sl.VIEW.LEFT)
            timestamp = zed.get_timestamp(sl.TIME_REFERENCE.CURRENT)  # Get the timestamp at the time the image was captured
            print("Image resolution: {0} x {1} || Image timestamp: {2}\n".format(image.get_width(), image.get_height(),
                  timestamp.get_milliseconds()))
            
            # Convert s1.Mat to umpy array
            image_np = image.get_data()

            # Convert the numpy array to BGR format (for OpenCV)
            image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGBA2BGR)

            # Save the image to the DTA directory
            image_path = os.path.join("DATA", "imge_{:04d}.png".format(i))
            cv2.imwrite(image_path, image_bgr)

            i = i + 1

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
