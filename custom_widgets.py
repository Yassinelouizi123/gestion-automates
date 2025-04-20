from PyQt6.QtWidgets import (QPushButton, QProgressBar, QWidget, QVBoxLayout, QLabel, 
                            QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QIcon


class ModernButton(QPushButton):
    def __init__(self, text, parent=None, icon=None, accent_color="#00C2FF"):
        super().__init__(text, parent)
        self.accent_color = accent_color
        self.setFixedHeight(40)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Remove focus rectangle
        
        if icon:
            self.setIcon(QIcon(icon))
            self.setIconSize(QSize(18, 18))
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: #1A2133;
                color: white;
                border: none;
                border-radius: 10px;  /* Reduced from 20px to 10px */
                padding: 8px 20px;
                text-align: left;
                font-weight: bold;
                outline: none;  /* Remove focus outline */
            }}
            QPushButton:hover {{
                background-color: #242E48;
                border-radius: 10px;  /* Maintain rounded corners on hover */
            }}
            QPushButton:pressed {{
                background-color: #192235;
                border-radius: 10px;  /* Maintain rounded corners when pressed */
            }}
        """)


class ModernSlider(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTextVisible(False)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(50)
        self.setFixedHeight(6)
        
        self.setStyleSheet("""
            QProgressBar {
                background-color: #1A2133;
                border-radius: 3px;
                border: none;
            }
            QProgressBar::chunk {
                background-color: #00C2FF;
                border-radius: 3px;
            }
        """)


class MenuCategory(QWidget):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)
        layout.setSpacing(2)
        
        # Category header
        header = QLabel(title)
        header.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 13px;
                padding: 7px 15px;
                background-color: transparent;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(header)
        
        # Container for menu items
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setContentsMargins(10, 0, 10, 0)
        self.items_layout.setSpacing(5)
        
        layout.addWidget(self.items_container)
    
    def add_menu_item(self, text, icon=None, action=None):
        button = ModernButton(text, accent_color="#7B42F6")
        
        if action:
            button.clicked.connect(action)
            
        self.items_layout.addWidget(button)
        return button

class ModernTabButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCheckable(True)
        self.setFixedHeight(45)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)  # Prevent focus rectangle
        
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #8A98AC;
                border: none;
                border-bottom: 2px solid transparent;
                font-size: 14px;
                font-weight: bold;
                padding: 5px 15px;
                text-align: center;
                outline: none;  /* Remove focus outline */
            }
            QPushButton:checked {
                color: white;
                border-bottom: 2px solid #7B42F6;
            }
            QPushButton:hover:!checked {
                color: white;
            }
            QPushButton:focus {
                outline: none;  /* Remove focus outline */
            }
        """)
