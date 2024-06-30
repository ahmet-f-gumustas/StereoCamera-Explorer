# First Initiliaze
from PyQt5.QtWidgets import QApplication

from ui.ui_main import STEREO_CAM

import warnings
import sys
warnings.filterwarnings('ignore')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    stereo_cam = STEREO_CAM()
    stereo_cam.show()
    sys.exit(app.exec_())
