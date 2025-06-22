from aqt.qt import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QLineEdit

from .config import korean_support_config

from aqt import mw


def load_api_key():
    return korean_support_config.options["krdictApiKey"]


def save_api_key(api_key):
    korean_support_config.options["krdictApiKey"] = api_key


def showKrdictApiKey():
    dialog = QDialog(mw)
    layout = QVBoxLayout()
    
    label = QLabel("""<div>You can set a krdict Api Key to automatically fill the "Meaning" field with korean explanations of the word. <br>
                   You can apply for a API key for krdict on the korean government site <a href='https://krdict.korean.go.kr/openApi/openApiRegister'>here</a>)<br>
                   Enter your Krdict API key:
                   </div>""")
    label.setOpenExternalLinks(True)
    layout.addWidget(label)

    input_field = QLineEdit()
    input_field.setText(load_api_key())
    layout.addWidget(input_field)

    buttons = QDialogButtonBox(
        QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
    )
    layout.addWidget(buttons)

    def save():
        save_api_key(input_field.text().strip())
        dialog.accept()

    buttons.accepted.connect(save)
    buttons.rejected.connect(dialog.reject)

    dialog.setLayout(layout)
    dialog.exec()
