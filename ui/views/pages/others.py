from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class OthersPage(QWidget):
    """Others Page"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Others Page"))
        self.setLayout(layout)
