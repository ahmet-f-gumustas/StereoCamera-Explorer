import sys
import pyzed.sl as sl
import numpy as np
import cv2

def main():
    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.HD720  # Use HD720 video mode
    init_params.camera_fps = 30  # Set FPS at 30
    init_params.depth_mode = sl.DEPTH_MODE.PERFORMANCE  # Use performance depth mode

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(f"Error opening ZED camera: {err}")
        sys.exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_params = sl.RuntimeParameters()

    # Prepare new image size to retrieve half-resolution images
    image_size = zed.get_camera_information().camera_configuration.resolution
    new_width = image_size.width // 2
    new_height = image_size.height // 2

    # Create sl.Mat objects for image and optical flow
    image = sl.Mat(new_width, new_height, sl.MAT_TYPE.U8_C4)
    optical_flow = sl.Mat()

    # Main loop
    while True:
        if zed.grab(runtime_params) == sl.ERROR_CODE.SUCCESS:
            # Retrieve left image
            zed.retrieve_image(image, sl.VIEW.LEFT)

            # Retrieve optical flow
            zed.retrieve_measure(optical_flow, sl.MEASURE.OPTICAL_FLOW)

            # Get numpy arrays
            image_np = image.get_data()
            optical_flow_np = optical_flow.get_data()

            # Convert optical flow to HSV image
            hsv = np.zeros((optical_flow_np.shape[0], optical_flow_np.shape[1], 3), dtype=np.uint8)
            magnitude, angle = cv2.cartToPolar(optical_flow_np[..., 0], optical_flow_np[..., 1])
            hsv[..., 0] = angle * 180 / np.pi / 2
            hsv[..., 1] = 255
            hsv[..., 2] = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX)
            optical_flow_hsv = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            # Display images
            cv2.imshow("Image", image_np)
            cv2.imshow("Optical Flow", optical_flow_hsv)

            # Break loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
