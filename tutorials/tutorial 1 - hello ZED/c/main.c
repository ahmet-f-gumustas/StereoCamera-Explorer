#include <sl/c_api/zed_interface.h>
#include <stdbool.h>
#include <stdio.h>


int main(int argc, char **argv) {

    // Create a ZED camera object
	int camera_id = 0;
	sl_create_camera(camera_id);

	struct SL_InitParameters init_param;
	init_param.camera_fps = 30;
	init_param.resolution = SL_RESOLUTION_HD1080;
	init_param.input_type = SL_INPUT_TYPE_USB;
	init_param.camera_device_id = camera_id;
	init_param.camera_image_flip = SL_FLIP_MODE_AUTO;
	init_param.camera_disable_self_calib = false;
	init_param.enable_image_enhancement = true;
	init_param.svo_real_time_mode = true;
	init_param.depth_mode = SL_DEPTH_MODE_PERFORMANCE;
	init_param.depth_stabilization = 1;
	init_param.depth_maximum_distance = 40;
	init_param.depth_minimum_distance = -1;
	init_param.coordinate_unit = SL_UNIT_METER;
	init_param.coordinate_system = SL_COORDINATE_SYSTEM_LEFT_HANDED_Y_UP;
	init_param.sdk_gpu_id = -1;
	init_param.sdk_verbose = false;
	init_param.sensors_required = false;
	init_param.enable_right_side_measure = false;
	init_param.open_timeout_sec = 5.0f;
	init_param.async_grab_camera_recovery = false;
	init_param.grab_compute_capping_fps = 0;


	// Open the camera
	int state = sl_open_camera(camera_id, &init_param, 0, "", "", 0, "", "", "");

    if (state != 0) {
		printf("Error Open: %i \n", state);
        return 1;
    }

	// Get camera information (ZED serial number)
	int sn = sl_get_zed_serial(camera_id);
	printf("Hello! This is my serial number: %d\n", sn);


	sl_close_camera(camera_id);
    return 0;
}

