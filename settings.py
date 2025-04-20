from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtGui import QFont, QColor
from custom_widgets import ModernSlider

class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        
        # Content area with shadow and rounded corners
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            #contentFrame {
                background-color: #1A2133;
                border-radius: 10px;
            }
        """)
        
        # Add drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 3)
        content_frame.setGraphicsEffect(shadow)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        settings_message = QLabel("Settings options will be available in future updates.")
        settings_message.setStyleSheet("color: #8A98AC; font-size: 14px;")
        
        # Sample settings slider
        theme_label = QLabel("Dark Theme")
        theme_label.setStyleSheet("color: white; font-weight: bold; font-size: 14px;")
        
        theme_slider = ModernSlider()
        theme_slider.setValue(100)  # Set to 100% for dark theme
        
        slider_layout = QHBoxLayout()
        slider_layout.addWidget(theme_label)
        slider_layout.addStretch(1)
        slider_layout.addWidget(theme_slider)
        
        content_layout.addWidget(settings_message)
        content_layout.addSpacing(20)
        content_layout.addLayout(slider_layout)
        content_layout.addStretch(1)
        
        layout.addWidget(title_label)
        layout.addWidget(content_frame, 1)
        
        self.setLayout(layout)