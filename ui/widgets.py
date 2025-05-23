from PyQt5.QtWidgets import (
    QListWidget, QListWidgetItem, QLabel, 
    QProgressBar, QWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt

class RideListItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

class LoadingWidget(QWidget):
    def __init__(self, message="Processing..."):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
        self.setLayout(layout)