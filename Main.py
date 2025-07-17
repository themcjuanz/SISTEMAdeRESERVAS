import sys
from Inicio import Widget
from PySide6 import QtWidgets
from MaletaMano import MaletaMano  

app = QtWidgets.QApplication(sys.argv)
widget = Widget()
widget.resize(564, 504)
widget.show()
maleta1 = MaletaMano(peso=10.0)
print(maleta1)
sys.exit(app.exec())

