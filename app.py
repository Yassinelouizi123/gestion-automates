import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor, QIcon
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    app_icon = QIcon("icon.png")
    app.setWindowIcon(app_icon)
    
    # Set dark palette
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(14, 21, 37))
    # ... rest of palette setup ...
    app.setPalette(dark_palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())