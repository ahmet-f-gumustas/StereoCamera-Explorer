from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel
from PyQt5.QtCore import Qt




class YOLOFrame(QGroupBox):
    def __init__(self, main):
        super().__init__()
        
        self.main = main
        self.grid_position = [1, 0]
        self.setTitle('YOLO Frame')
        
        self.grid_layout = QGridLayout()

        self.frame_label = QLabel()
        self.frame_label.setAlignment(Qt.AlignCenter)

        self.grid_layout.addWidget(self.frame_label, 0, 0)
        
        self.setLayout(self.grid_layout)
