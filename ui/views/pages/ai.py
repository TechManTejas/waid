from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class AIPage(QWidget):
    """AI Page"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("AI Page"))
        self.setLayout(layout)
