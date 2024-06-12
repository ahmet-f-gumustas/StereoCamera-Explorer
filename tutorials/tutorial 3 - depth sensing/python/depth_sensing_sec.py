import pyzed.sl as sl

def main():
    # Kamera ayarları
    zed = sl.Camera()
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.coordinate_units = sl.UNIT.MILLIMETER

    # Kamera başlatma
    err = zed.open(init_params)
    if err != sl.ERROR_CODE.SUCCESS:
        print("Kamera açma hatası:", err)
        exit(1)

    runtime_parameters = sl.RuntimeParameters()

    # Görüntü ve derinlik matrisleri
    image = sl.Mat()
    depth = sl.Mat()

    while True:
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            zed.retrieve_image(image, sl.VIEW.LEFT)
            zed.retrieve_measure(depth, sl.MEASURE.DEPTH)

            # Belirtilen koordinatlarda derinlik hesaplaması
            x, y = 640, 360
            distance = depth.get_value(x, y)
            if distance[0] == sl.ERROR_CODE.SUCCESS:
                print(f"Distance at ({x}, {y}): {distance[1]}")
            else:
                print(f"The distance can not be computed at ({x}, {y})")

    zed.close()

if __name__ == "__main__":
    main()