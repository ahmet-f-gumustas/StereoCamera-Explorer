import pyzed.sl as sl

def main():
    # Create a ZED camera object
    zed = sl.Camera()

    # Set configuration parameters
    init_params = sl.InitParameters()
    init_params.sdk_verbose = 0  # Change False to 0

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print(repr(err))
        zed.close()
        return

    # Capture 50 images and stop
    i = 0
    image = sl.Mat()
    while i < 50:
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # Retrieve the left image
            zed.retrieve_image(image, sl.VIEW.LEFT)
            # Display the image
            print("Image {} captured".format(i))
            i += 1

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
