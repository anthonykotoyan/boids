import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt

class ParamTweaker(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        # Align Strength
        hbox_align = QHBoxLayout()
        self.align_label = QLabel('Align Strength')
        self.align_slider = QSlider(Qt.Horizontal)
        self.align_slider.setMinimum(0)
        self.align_slider.setMaximum(100)
        self.align_slider.setValue(50)  # Initial value
        hbox_align.addWidget(self.align_label)
        hbox_align.addWidget(self.align_slider)

        # Avoid Strength
        hbox_avoid = QHBoxLayout()
        self.avoid_label = QLabel('Avoid Strength')
        self.avoid_slider = QSlider(Qt.Horizontal)
        self.avoid_slider.setMinimum(0)
        self.avoid_slider.setMaximum(100)
        self.avoid_slider.setValue(50)  # Initial value
        hbox_avoid.addWidget(self.avoid_label)
        hbox_avoid.addWidget(self.avoid_slider)

        # Cohesion Strength
        hbox_cohesion = QHBoxLayout()
        self.cohesion_label = QLabel('Cohesion Strength')
        self.cohesion_slider = QSlider(Qt.Horizontal)
        self.cohesion_slider.setMinimum(0)
        self.cohesion_slider.setMaximum(100)
        self.cohesion_slider.setValue(50)  # Initial value
        hbox_cohesion.addWidget(self.cohesion_label)
        hbox_cohesion.addWidget(self.cohesion_slider)

        vbox.addLayout(hbox_align)
        vbox.addLayout(hbox_avoid)
        vbox.addLayout(hbox_cohesion)

        self.setLayout(vbox)
        self.setWindowTitle('Parameter Tweaker')
        self.setGeometry(50, 50, 300, 200)
        self.show()

        # Start the simulation
        print("Starting simulation...")
        subprocess.Popen(["python", "main.py"])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    param_tweaker = ParamTweaker()
    sys.exit(app.exec_())
