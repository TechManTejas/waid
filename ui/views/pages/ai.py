from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QRadioButton,
    QButtonGroup,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
)
from services.ai.ai_manager import AIManager


class AIPage(QWidget):
    """AI Settings Page"""

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.radio_group = QButtonGroup(self)
        self.config_layout = QFormLayout()
        self.config_inputs = {}

        self.load_providers()
        self.load_configuration_fields()

        self.save_button = QPushButton("Save Configuration")
        self.save_button.setFixedHeight(50)
        self.save_button.clicked.connect(self.save_configuration)

        self.layout.addLayout(self.config_layout)
        self.layout.addWidget(self.save_button)

    def load_providers(self):
        """Load AI providers and set the active one."""
        providers = AIManager.get_available_providers()
        current_provider = AIManager.get_provider()

        for provider in providers:
            radio = QRadioButton(provider)
            self.radio_group.addButton(radio)
            self.layout.addWidget(radio)

            if provider == current_provider:
                radio.setChecked(True)

        self.radio_group.buttonClicked.connect(self.load_configuration_fields)

    def load_configuration_fields(self):
        """Load the configuration fields for the selected provider."""
        selected_button = self.radio_group.checkedButton()
        if not selected_button:
            return

        provider = selected_button.text()
        AIManager.set_provider(provider)

        try:
            config_keys = AIManager.get_required_configuration()
            config_values = AIManager.get_configuration()
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
            return

        for i in reversed(range(self.config_layout.count())):
            self.config_layout.itemAt(i).widget().deleteLater()
        self.config_inputs.clear()

        for key in config_keys:
            label = QLabel(key)
            input_field = QLineEdit()
            input_field.setText(config_values.get(key, ""))
            self.config_inputs[key] = input_field
            self.config_layout.addRow(label, input_field)

    def save_configuration(self):
        """Save the current AI provider's configuration."""
        selected_button = self.radio_group.checkedButton()
        if not selected_button:
            QMessageBox.warning(self, "Warning", "No AI provider selected!")
            return

        provider = selected_button.text()
        config_data = {
            key: field.text().strip() for key, field in self.config_inputs.items()
        }

        try:
            AIManager.set_configuration(config_data)
            QMessageBox.information(
                self, "Success", "Configuration saved successfully!"
            )
        except ValueError as e:
            QMessageBox.critical(self, "Error", str(e))
