from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel, QSpacerItem
from PyQt5.QtCore import Qt

import sys


class LeftFrame(QGroupBox):
    def __init_(self, main):
        super().__init__()
        
        self.main = main
        self.grid_position = [0, 0]
        self.setTitle('Left Frame')

        self.grid_layout = QGridLayout()

        self.frame_label = QLabel()
        self.frame_label.setAlignment(Qt.AlignCenter)

        self.grid_layout.addWidget(self.frame_label, 0, 0)

        self.setLayout(self.grid_layout)