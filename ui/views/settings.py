from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QHBoxLayout,
    QFrame,
)
import sys
from ui.views.pages.ai import AIPage
from ui.views.pages.jira import JiraPage
from ui.views.pages.tickets import TicketsPage
from ui.views.pages.others import OthersPage


class SettingsWindow(QWidget):
    """Main Settings Window with Sidebar Navigation"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.setGeometry(100, 100, 800, 500)

        main_layout = QVBoxLayout(self)

        top_separator = QFrame()
        top_separator.setFrameShape(QFrame.Shape.HLine)
        top_separator.setFrameShadow(QFrame.Shadow.Sunken)
        top_separator.setStyleSheet("color: white;")

        content_layout = QHBoxLayout()

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(0)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        self.pages = QStackedWidget()

        self.add_sidebar_button("AI", AIPage, sidebar_layout)
        self.add_sidebar_button("Jira", JiraPage, sidebar_layout)
        self.add_sidebar_button("Tickets", TicketsPage, sidebar_layout)
        self.add_sidebar_button("Others", OthersPage, sidebar_layout)

        sidebar_layout.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar_layout)
        sidebar_widget.setFixedWidth(120)

        sidebar_separator = QFrame()
        sidebar_separator.setFrameShape(QFrame.Shape.VLine)
        sidebar_separator.setFrameShadow(QFrame.Shadow.Sunken)
        sidebar_separator.setStyleSheet("color: white;")

        content_layout.addWidget(sidebar_widget)
        content_layout.addWidget(sidebar_separator)
        content_layout.addWidget(self.pages, 4)

        main_layout.addWidget(top_separator)
        main_layout.addLayout(content_layout)

        self.pages.setCurrentIndex(0)

    def add_sidebar_button(self, name, page_class, layout):
        """Creates a button for the sidebar and links it to a page."""
        button = QPushButton(name)
        button.setFixedHeight(50)
        button.setStyleSheet("text-align: center; padding-left: 10px; font-size: 14px;")
        button.clicked.connect(
            lambda: self.pages.setCurrentWidget(self.pages.findChild(page_class))
        )
        layout.addWidget(button)

        page = page_class()
        self.pages.addWidget(page)


def open_settings_window():
    """Open the settings window."""
    app = QApplication(sys.argv)
    window = SettingsWindow()
    window.show()
    app.exec()
