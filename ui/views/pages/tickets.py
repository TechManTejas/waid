from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class TicketsPage(QWidget):
    """Tickets Page"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Tickets Page"))
        self.setLayout(layout)
