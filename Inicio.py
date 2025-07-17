from Login import LoginDialog
import random
from PySide6 import QtWidgets, QtCore, QtGui

class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.login_dialog = LoginDialog()

        # --- Messages and indices ---
        self.hello = [
            "Hello", "Bonjour", "Hallo", "Ciao", "Olá", "Привет", "你好",
            "こんにちは", "안녕하세요", "السلام عليكم", "नमस्ते", "Hoi", "Γεια σου",
            "Jambo", "Shalom", "Salam", "Hej", "Sveiki", "Merhaba"
        ]
        self.goodbye = [
            "Goodbye", "Au revoir", "Auf Wiedersehen", "Arrivederci", "Adeus",
            "До свидания", "再见", "さようなら", "안녕히 가세요", "مع السلامة", "अलविदा",
            "Tot ziens", "Αντίο", "Kwaheri"
        ]
        self.hello_index = 0
        self.goodbye_index = 0
        self.mode = "hello"

        # --- Load background pixmap ---
        self.bg_pix = QtGui.QPixmap("fondo.jpg")
        self.setFixedSize(564, 504)

        # --- Widgets: label and buttons ---
        self.text = QtWidgets.QLabel(random.choice(self.hello), alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
        self.button_hello = QtWidgets.QPushButton("Iniciar Sesión")
        self.button_goodbye = QtWidgets.QPushButton("Salir")
        self.text2 = QtWidgets.QLabel("Hola", alignment=QtCore.Qt.AlignmentFlag.AlignCenter)

        self.text2.setStyleSheet("color: white; font-size: 15px;")
        self.text.setFixedHeight(100)
        self.text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # --- Layout for controls ---
        vbox = QtWidgets.QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.text2)
        vbox.addWidget(self.text)
        vbox.addSpacing(20)
        vbox.addWidget(self.button_hello)
        vbox.addWidget(self.button_goodbye)
        vbox.addStretch()
        self.setLayout(vbox)

        # --- Styling for widgets ---
        self.text.setStyleSheet("color: white;")
        self.button_hello.setStyleSheet("font-size: 18px; padding: 10px;")
        self.button_goodbye.setStyleSheet("font-size: 18px; padding: 10px;")

        # --- Font for the main label ---
        font = QtGui.QFont()
        font.setPointSize(25)
        self.text.setFont(font)

        # --- Timer to auto-cycle greetings ---
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_text)
        self.timer.start(2000)

        # --- Button signals ---
        self.button_hello.clicked.connect(self.highlight_current)
        self.button_hello.clicked.connect(self.close_app)
        self.button_hello.clicked.connect(self.login_dialog.exec)
        self.button_goodbye.clicked.connect(self.close_app)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        # draw scaled background to fill widget
        painter.drawPixmap(self.rect(), self.bg_pix)
        super().paintEvent(event)

    @QtCore.Slot()
    def update_text(self):
        self.text.setStyleSheet("font-weight: normal; font-size: 34px; color: white;")

        if self.mode == "hello":
            current = self.hello[self.hello_index]
            self.hello_index = (self.hello_index + 1) % len(self.hello)
            self.text.setText(current)
            self.text2.setText("Hola")
        else:
            current = self.goodbye[self.goodbye_index]
            self.goodbye_index = (self.goodbye_index + 1) % len(self.goodbye)
            self.text.setText(current)
            self.text2.setText("Adiós")

    @QtCore.Slot()
    def highlight_current(self):
        # Highlight the current greeting in green
        self.mode = "hello"
        self.text.setStyleSheet("color: lightgreen; font-weight: bold; font-size: 70px;")
        self.timer.start(2000)  # Speed up the timer for highlighting

    @QtCore.Slot()
    def close_app(self):
        # Show a random farewell, highlight in red, then quit after 1s
        self.mode = "goodbye"
        farewell = random.choice(self.goodbye)
        self.text2.setText("Adiós")
        self.text.setText(farewell)
        self.text.setStyleSheet("color: salmon; font-weight: bold; font-size: 70px;")
        self.timer.timeout.disconnect(self.update_text)
        self.timer.start(1000)  # Speed up the timer for goodbye
        QtCore.QTimer.singleShot(1000, self.close)
