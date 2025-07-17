from PySide6 import QtWidgets

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setFixedSize(300, 150)

        # Widgets
        self.label_user = QtWidgets.QLabel("Usuario:")
        self.input_user = QtWidgets.QLineEdit()
        self.label_pass = QtWidgets.QLabel("Contraseña:")
        self.input_pass = QtWidgets.QLineEdit()
        self.input_pass.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.button_login = QtWidgets.QPushButton("Iniciar Sesión")
        self.button_cancel = QtWidgets.QPushButton("Cancelar")
        self.message = QtWidgets.QLabel("")
        self.message.setStyleSheet("color: red;")

        # Layout
        form = QtWidgets.QFormLayout()
        form.addRow(self.label_user, self.input_user)
        form.addRow(self.label_pass, self.input_pass)

        buttons = QtWidgets.QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self.button_login)
        buttons.addWidget(self.button_cancel)

        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.message)
        vbox.addLayout(buttons)
        self.setLayout(vbox)

        # Connections
        self.button_login.clicked.connect(self.handle_login)
        self.button_cancel.clicked.connect(self.reject)

    def handle_login(self):
        user = self.input_user.text().strip()
        password = self.input_pass.text()
        # Validación simple
        if user == "admin" and password == "1234":
            self.accept()
        else:
            self.message.setText("Usuario o contraseña incorrectos")