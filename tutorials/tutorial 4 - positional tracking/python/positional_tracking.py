import pyzed.sl as sl
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Create a Camera object
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

    # Data lists
    timestamps = []
    translations = {'Tx': [], 'Ty': [], 'Tz': []}
    orientations = {'Ox': [], 'Oy': [], 'Oz': [], 'Ow': []}
    imu_accelerations = {'Ax': [], 'Ay': [], 'Az': []}
    imu_angular_velocities = {'Vx': [], 'Vy': [], 'Vz': []}
    imu_orientations = {'Ox': [], 'Oy': [], 'Oz': [], 'Ow': []}

    # Track the camera position during 1000 frames
    i = 0
    zed_pose = sl.Pose()
    zed_sensors = sl.SensorsData()
    runtime_parameters = sl.RuntimeParameters()
    can_compute_imu = zed.get_camera_information().camera_model != sl.MODEL.ZED

    while i < 1000:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # Get the pose of the left eye of the camera with reference to the world frame
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
                acceleration = [0,0,0]
                zed_imu.get_linear_acceleration(acceleration)
                ax = acceleration[0]
                ay = acceleration[1]
                az = acceleration[2]
                imu_accelerations['Ax'].append(ax)
                imu_accelerations['Ay'].append(ay)
                imu_accelerations['Az'].append(az)

                # Get IMU angular velocity
                a_velocity = [0,0,0]
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

            i += 1

    # Create DataFrames
    df_translations = pd.DataFrame(translations, index=timestamps)
    df_orientations = pd.DataFrame(orientations, index=timestamps)
    df_imu_accelerations = pd.DataFrame(imu_accelerations, index=timestamps)
    df_imu_angular_velocities = pd.DataFrame(imu_angular_velocities, index=timestamps)
    df_imu_orientations = pd.DataFrame(imu_orientations, index=timestamps)

    # Close the camera
    zed.close()

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    df_translations.plot(ax=plt.gca(), title="Translation over Time")
    plt.ylabel("Meters")
    plt.xlabel("Time (ms)")

    plt.subplot(2, 1, 2)
    df_orientations.plot(ax=plt.gca(), title="Orientation over Time")
    plt.ylabel("Quaternion")
    plt.xlabel("Time (ms)")

    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    df_imu_accelerations.plot(ax=plt.gca(), title="IMU Acceleration over Time")
    plt.ylabel("Acceleration (m/s^2)")
    plt.xlabel("Time (ms)")

    plt.subplot(3, 1, 2)
    df_imu_angular_velocities.plot(ax=plt.gca(), title="IMU Angular Velocity over Time")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.xlabel("Time (ms)")

    plt.subplot(3, 1, 3)
    df_imu_orientations.plot(ax=plt.gca(), title="IMU Orientation over Time")
    plt.ylabel("Quaternion")
    plt.xlabel("Time (ms)")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
