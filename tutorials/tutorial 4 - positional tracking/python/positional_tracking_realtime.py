import pyzed.sl as sl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Global lists to hold the data
timestamps = []
translations = {'Tx': [], 'Ty': [], 'Tz': []}
orientations = {'Ox': [], 'Oy': [], 'Oz': [], 'Ow': []}
imu_accelerations = {'Ax': [], 'Ay': [], 'Az': []}
imu_angular_velocities = {'Vx': [], 'Vy': [], 'Vz': []}
imu_orientations = {'Ox': [], 'Oy': [], 'Oz': [], 'Ow': []}

def update_data(frame, zed, runtime_parameters, zed_pose, zed_sensors, can_compute_imu, line1, line2, line3, line4):
    if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
        zed.get_position(zed_pose, sl.REFERENCE_FRAME.WORLD)

        # Get translation and orientation
        py_translation = sl.Translation()
        tx = zed_pose.get_translation(py_translation).get()[0]
        ty = zed_pose.get_translation(py_translation).get()[1]
        tz = zed_pose.get_translation(py_translation).get()[2]
        translations['Tx'].append(tx)
        translations['Ty'].append(ty)
        translations['Tz'].append(tz)

        py_orientation = sl.Orientation()
        ox = zed_pose.get_orientation(py_orientation).get()[0]
        oy = zed_pose.get_orientation(py_orientation).get()[1]
        oz = zed_pose.get_orientation(py_orientation).get()[2]
        ow = zed_pose.get_orientation(py_orientation).get()[3]
        orientations['Ox'].append(ox)
        orientations['Oy'].append(oy)
        orientations['Oz'].append(oz)
        orientations['Ow'].append(ow)

        timestamps.append(zed_pose.timestamp.get_milliseconds())

        if can_compute_imu:
            zed.get_sensors_data(zed_sensors, sl.TIME_REFERENCE.IMAGE)
            zed_imu = zed_sensors.get_imu_data()

            # Get IMU acceleration
            acceleration = [0, 0, 0]
            zed_imu.get_linear_acceleration(acceleration)
            ax = acceleration[0]
            ay = acceleration[1]
            az = acceleration[2]
            imu_accelerations['Ax'].append(ax)
            imu_accelerations['Ay'].append(ay)
            imu_accelerations['Az'].append(az)

            # Get IMU angular velocity
            a_velocity = [0, 0, 0]
            zed_imu.get_angular_velocity(a_velocity)
            vx = a_velocity[0]
            vy = a_velocity[1]
            vz = a_velocity[2]
            imu_angular_velocities['Vx'].append(vx)
            imu_angular_velocities['Vy'].append(vy)
            imu_angular_velocities['Vz'].append(vz)

            # Get IMU orientation
            zed_imu_pose = sl.Transform()
            ox = zed_imu.get_pose(zed_imu_pose).get_orientation().get()[0]
            oy = zed_imu.get_pose(zed_imu_pose).get_orientation().get()[1]
            oz = zed_imu.get_pose(zed_imu_pose).get_orientation().get()[2]
            ow = zed_imu.get_pose(zed_imu_pose).get_orientation().get()[3]
            imu_orientations['Ox'].append(ox)
            imu_orientations['Oy'].append(oy)
            imu_orientations['Oz'].append(oz)
            imu_orientations['Ow'].append(ow)

        # Update plots
        line1.set_data(timestamps, translations['Tx'])
        line2.set_data(timestamps, translations['Ty'])
        line3.set_data(timestamps, imu_accelerations['Ax'])
        line4.set_data(timestamps, imu_angular_velocities['Vx'])
    
    return line1, line2, line3, line4

def main():
    # Create a Camera object
    global zed, runtime_parameters, zed_pose, zed_sensors, can_compute_imu
    zed = sl.Camera()

    # Create a InitParameters object and set configuration parameters
    init_params = sl.InitParameters()
    init_params.camera_resolution = sl.RESOLUTION.AUTO # Use HD720 or HD1200 video mode (default fps: 60)
    init_params.coordinate_system = sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP # Use a right-handed Y-up coordinate system
    init_params.coordinate_units = sl.UNIT.METER  # Set units in meters

    # Open the camera
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Camera Open : "+repr(err)+". Exit program.")
        exit()

    # Enable positional tracking with default parameters
    py_transform = sl.Transform()  # First create a Transform object for TrackingParameters object
    tracking_parameters = sl.PositionalTrackingParameters(_init_pos=py_transform)
    err = zed.enable_positional_tracking(tracking_parameters)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Enable positional tracking : "+repr(err)+". Exit program.")
        zed.close()
        exit()

    zed_pose = sl.Pose()
    zed_sensors = sl.SensorsData()
    runtime_parameters = sl.RuntimeParameters()
    can_compute_imu = zed.get_camera_information().camera_model != sl.MODEL.ZED

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))

    ax1.set_title('Translations over Time')
    ax1.set_xlabel('Time (ms)')
    ax1.set_ylabel('Translation (m)')
    line1, = ax1.plot([], [], label='Tx')
    line2, = ax1.plot([], [], label='Ty')
    ax1.legend()

    ax2.set_title('IMU Data over Time')
    ax2.set_xlabel('Time (ms)')
    ax2.set_ylabel('IMU Data')
    line3, = ax2.plot([], [], label='Ax')
    line4, = ax2.plot([], [], label='Vx')
    ax2.legend()

    def init():
        ax1.set_xlim(0, 10000)
        ax1.set_ylim(-5, 5)
        ax2.set_xlim(0, 10000)
        ax2.set_ylim(-20, 20)
        return line1, line2, line3, line4

    ani = animation.FuncAnimation(fig, update_data, fargs=(zed, runtime_parameters, zed_pose, zed_sensors, can_compute_imu, line1, line2, line3, line4),
                                  init_func=init, blit=True, interval=50)
    plt.tight_layout()
    plt.show()

    # Close the camera
    zed.close()

if __name__ == "__main__":
    main()
