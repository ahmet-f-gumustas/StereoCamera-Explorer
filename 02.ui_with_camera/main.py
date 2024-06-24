# First Initiliaze
from PyQt5.QtWidgets import QApplication

from ui.ui_main import STEREO_CAM

print("status TRUE")

import warnings
import sys
warnings.filterwarnings('ignore')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Call the class here
    stereo_cam = STEREO_CAM()
    stereo_cam.show()
    sys.exit(app.exec_())
