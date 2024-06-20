#include <sl/Camera.hpp>

using namespace std;
using namespace sl;

int main(int argc, char **argv) {

    // Create a ZED camera object
    Camera zed;

    // Set configuration parameters
    InitParameters init_parameters;
    init_parameters.camera_resolution = RESOLUTION::AUTO; // Use HD720 opr HD1200 video mode, depending on camera type.
    init_parameters.camera_fps = 30; // Set fps at 30

    // Open the camera
    auto returned_state = zed.open(init_parameters);
    if (returned_state != ERROR_CODE::SUCCESS) {
        cout << "Error " << returned_state << ", exit program." << endl;
        return EXIT_FAILURE;
    }

    // Capture 50 frames and stop
    int i = 0;
    sl::Mat image;
    while (i < 50) {
        // Grab an image
        returned_state = zed.grab();
        // A new image is available if grab() returns ERROR_CODE::SUCCESS
        if (returned_state == ERROR_CODE::SUCCESS) {

            // Get the left image
            zed.retrieveImage(image, VIEW::LEFT);
            
            // Display the image resolution and its acquisition timestamp
            cout<<"Image resolution: "<< image.getWidth()<<"x"<<image.getHeight() <<" || Image timestamp: "<<image.timestamp.data_ns<<endl;
            i++;
        }
    }

    // Close the camera
    zed.close();
    return EXIT_SUCCESS;
}
