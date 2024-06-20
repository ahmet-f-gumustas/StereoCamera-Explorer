// Standard includes
#include <iostream>
#include <fstream>

// ZED includes
#include <sl/Camera.hpp>

// Using std and sl namespaces
using namespace std;
using namespace sl;

int main(int argc, char** argv) {
    // Create ZED objects
    Camera zed;
    InitParameters init_parameters;
    init_parameters.camera_resolution = RESOLUTION::AUTO;
    init_parameters.depth_mode = DEPTH_MODE::PERFORMANCE;
    init_parameters.coordinate_units = UNIT::METER;
    init_parameters.sdk_verbose = true;

    // Open the camera
    auto returned_state = zed.open(init_parameters);
    if (returned_state != ERROR_CODE::SUCCESS) {
        cout << "Error " << returned_state << ", exit program.\n";
        return EXIT_FAILURE;
    }

    // Define the Objects detection module parameters
    BodyTrackingParameters detection_parameters;
    // Different model can be chosen, optimizing the runtime or the accuracy
    detection_parameters.detection_model = BODY_TRACKING_MODEL::HUMAN_BODY_MEDIUM;
    // Body format
    detection_parameters.body_format = BODY_FORMAT::BODY_38;
    // run detection for every Camera grab
    detection_parameters.image_sync = true;
    // track detects object across time and space
    detection_parameters.enable_tracking = true;
    // Optimize the person joints position, requires more computations
    detection_parameters.enable_body_fitting = true;

    // If you want to have object tracking you need to enable positional tracking first
    if (detection_parameters.enable_tracking)
        zed.enablePositionalTracking();

    cout << "Body Tracking: Loading Module..." << endl;
    returned_state = zed.enableBodyTracking(detection_parameters);
    if (returned_state != ERROR_CODE::SUCCESS) {
        cout << "Error " << returned_state << ", exit program.\n";
        zed.close();
        return EXIT_FAILURE;
    }
    // detection runtime parameters
    BodyTrackingRuntimeParameters detection_parameters_rt;
    // For outdoor scene or long range, the confidence should be lowered to avoid missing detections (~20-30)
    // For indoor scene or closer range, a higher confidence limits the risk of false positives and increase the precision (~50+)
    detection_parameters_rt.detection_confidence_threshold = 40;
    // detection output
    Bodies objects;
    cout << setprecision(3);

    int nb_detection = 0;
    while (nb_detection < 100) {

        if (zed.grab() == ERROR_CODE::SUCCESS) {
            zed.retrieveBodies(objects, detection_parameters_rt);

            if (objects.is_new) {
                cout << objects.body_list.size() << " Person(s) detected\n\n";
                if (!objects.body_list.empty()) {

                    auto first_object = objects.body_list.front();

                    cout << "First Person attributes :\n";
                    cout << " Confidence (" << first_object.confidence << "/100)\n";

                    if (detection_parameters.enable_tracking)
                        cout << " Tracking ID: " << first_object.id << " tracking state: " <<
                            first_object.tracking_state << " / " << first_object.action_state << "\n";

                    cout << " 3D position: " << first_object.position <<
                            " Velocity: " << first_object.velocity << "\n";

                    cout << " 3D dimensions: " << first_object.dimensions << "\n";

                    cout << " Keypoints 2D \n";
                    // The body part meaning can be obtained by casting the index into a BODY_PARTS
                    // to get the BODY_PARTS index the getIdx function is available
                    for (int i = 0; i < first_object.keypoint_2d.size(); i++) {
                        auto &kp = first_object.keypoint_2d[i];
                        cout << "    " << i << " " << kp.x << ", " << kp.y << "\n";
                    }

                    // The BODY_PARTS can be link as bones, using sl::BODY_BONES which gives the BODY_PARTS pair for each
                    cout << " Keypoints 3D \n";
                    for (int i = 0; i < first_object.keypoint.size(); i++) {
                        auto &kp = first_object.keypoint[i];
                        cout << "    " <<  i << " " << kp.x << ", " << kp.y << ", " << kp.z << "\n";
                    }

                    cout << "\nPress 'Enter' to continue...\n";
                    cin.ignore();
                }
                nb_detection++;
            }
        }
    }
    zed.close();
    return EXIT_SUCCESS;
}
