import pyzed.sl as sl
import cv2
import numpy as np

def main():
    # ZED kamera nesnesi oluşturun
    zed = sl.Camera()

    # Init parametrelerini ayarlayın
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA  # Derinlik modunu ayarlayın
    init_params.coordinate_units = sl.UNIT.MILLIMETER  # Ölçü birimini milimetre olarak ayarlayın

    # Kamerayı başlatın
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Kamera açılamadı")
        zed.close()
        return

    cam_info = zed.get_camera_information()
    cam_res = cam_info.camera_configuration.resolution


    # Görüntü nesnesi oluşturun
    # Create an RGBA sl.Mat object
    image_zed = sl.Mat(cam_res.width, cam_res.height, sl.MAT_TYPE.U8_C4)
    # Retrieve data in a numpy array with get_data()
    image_ocv = image_zed.get_data()
    
    # Create a sl.Mat with float type (32-bit)
    depth_zed = sl.Mat(cam_res.width, cam_res.height, sl.MAT_TYPE.F32_C1)
    
    # Create an RGBA sl.Mat object
    image_depth_zed = sl.Mat(cam_res.width, cam_res.height, sl.MAT_TYPE.U8_C4)


    key = ' '
    while key != 113:  # 'q' tuşuna basılana kadar döngüyü çalıştırın
        if zed.grab() == sl.ERROR_CODE.SUCCESS:
            # RGB görüntüsünü alın
            zed.retrieve_image(image_zed, sl.VIEW.LEFT)
            # Derinlik verilerini alın
            zed.retrieve_measure(depth_zed, sl.MEASURE.DEPTH)
            
            # Derinlik verilerini normalize edin ve görselleştirin
            depth_image = depth_zed.get_data()
            # depth_image = np.nan_to_num(depth_image)  # NaN değerleri 0'a dönüştürün
            # depth_image = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX)
            # depth_image = np.uint8(depth_image)
            
            # Görüntüleri birleştirin ve gösterin
            #combined_image = cv2.hconcat([image.get_data(), cv2.applyColorMap(depth_image, cv2.COLORMAP_JET)])
            cv2.imshow("ZED | RGB ve Derinlik", depth_image)

        key = cv2.waitKey(10)
    
    # Kamerayı kapatın ve kaynakları serbest bırakın
    zed.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

