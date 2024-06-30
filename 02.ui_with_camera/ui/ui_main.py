import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# First Initialize
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout
from PyQt5.QtCore import Qt

from ui.ui_left_camera import LeftFrame
from ui.ui_right_camera import RightFrame
from ui.ui_yolo_frame import YOLOFrame
from ui.ui_depth_frame import DepthFrame

from utils.settings import Variables



class STEREO_CAM(QWidget):
    def __init__(self):
        super().__init__()

        self.variables = Variables()
        self.grid_layout = QGridLayout()
        
        self.setFixedSize(self.variables.width, self.variables.height)
        self.setWindowTitle("MOVE ON - VIO")
        
        self.left_frame = LeftFrame(self)
        self.right_frame = RightFrame(self)
        self.yolo_frame = YOLOFrame(self)
        self.depth_frame = DepthFrame(self)

        # Add Grid Layout
        self.grid_layout.addWidget(self.left_frame, *self.left_frame.grid_position)
        self.grid_layout.addWidget(self.right_frame, *self.right_frame.grid_position)
        self.grid_layout.addWidget(self.yolo_frame, *self.yolo_frame.grid_position)
        self.grid_layout.addWidget(self.depth_frame, *self.depth_frame.grid_position)        

        # Set Layout
        self.setLayout(self.grid_layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stereo_cam = STEREO_CAM()
    stereo_cam.show()
    sys.exit(app.exec_())
