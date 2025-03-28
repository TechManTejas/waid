from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout

class JiraPage(QWidget):
    """Jira Page"""

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Jira Page"))
        self.setLayout(layout)
