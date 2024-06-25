import pyzed.sl as sl
import torch
import cv2
import numpy as np

def main():
    # YOLOv5 modelini yükleyin
    model = torch.hub.load('/path/to/yolov5', 'custom', path='yolov5s.pt', source='local')

    # ZED kamera nesnesi oluşturun
    zed = sl.Camera()

    # Init parametrelerini ayarlayın
    init_params = sl.InitParameters()
    init_params.depth_mode = sl.DEPTH_MODE.ULTRA
    init_params.coordinate_units = sl.UNIT.MILLIMETER

    # Kamerayı başlatın
    if zed.open(init_params) != sl.ERROR_CODE.SUCCESS:
        print("Kamera açılamadı")
        zed.close()
        return

    # Görüntü nesnesi oluşturun
    image = sl.Mat()
    runtime_parameters = sl.RuntimeParameters()

    key = ' '
    while key != 113:  # 'q' tuşuna basılana kadar döngüyü çalıştırın
        if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
            # RGB görüntüsünü alın
            zed.retrieve_image(image, sl.VIEW.LEFT)
            frame = image.get_data()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # YOLOv5 modelini kullanarak nesne tespiti yapın
            results = model(frame)

            # Sonuçları alın ve gösterin
            df = results.pandas().xyxy[0]  # Nesne tespiti sonuçlarını dataframe olarak alın
            for index, row in df.iterrows():
                x1, y1, x2, y2, confidence, class_id, name = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax']), row['confidence'], row['class'], row['name']
                label = f"{name} {confidence:.2f}"
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            # Sonuçları gösterin
            cv2.imshow("ZED | YOLOv5", frame)

        key = cv2.waitKey(10)

    # Kamerayı kapatın ve kaynakları serbest bırakın
    zed.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

