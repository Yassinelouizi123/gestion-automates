from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QGraphicsDropShadowEffect, 
                            QGridLayout, QGroupBox)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class SettingsWidget(QWidget):
    def __init__(self, user_manager=None, current_user=None):
        super().__init__()
        self.user_manager = user_manager
        self.current_user = current_user
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        title_label = QLabel("Account Settings")
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
        content_layout.setSpacing(20)
        
        # Account Information Section
        account_group = QGroupBox("Account Information")
        account_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #2A3344;
                border-radius: 5px;
                margin-top: 1ex;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        account_layout = QGridLayout()
        account_layout.setSpacing(15)
        
        # Style for labels
        label_style = """
            QLabel {
                color: #8A98AC;
                font-size: 13px;
            }
        """
        value_style = """
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: bold;
            }
        """
        
        # Username
        username_label = QLabel("Username:")
        username_label.setStyleSheet(label_style)
        username_value = QLabel(self.current_user['username'] if self.current_user else "N/A")
        username_value.setStyleSheet(value_style)
        
        # Role
        role_label = QLabel("Account Type:")
        role_label.setStyleSheet(label_style)
        role_value = QLabel(self.current_user['role'].title() if self.current_user else "N/A")
        role_value.setStyleSheet(value_style)
        
        # Status
        status_label = QLabel("Account Status:")
        status_label.setStyleSheet(label_style)
        status_value = QLabel("Active" if self.current_user and self.current_user['is_active'] else "Inactive")
        status_value.setStyleSheet(value_style)
        
        # Created At
        created_label = QLabel("Created On:")
        created_label.setStyleSheet(label_style)
        created_value = QLabel(str(self.current_user['created_at']) if self.current_user else "N/A")
        created_value.setStyleSheet(value_style)
        
        # Add fields to layout
        account_layout.addWidget(username_label, 0, 0)
        account_layout.addWidget(username_value, 0, 1)
        account_layout.addWidget(role_label, 1, 0)
        account_layout.addWidget(role_value, 1, 1)
        account_layout.addWidget(status_label, 2, 0)
        account_layout.addWidget(status_value, 2, 1)
        account_layout.addWidget(created_label, 3, 0)
        account_layout.addWidget(created_value, 3, 1)
        
        account_group.setLayout(account_layout)
        
        # Privileges Section
        privileges_group = QGroupBox("Account Privileges")
        privileges_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #2A3344;
                border-radius: 5px;
                margin-top: 1ex;
                padding: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        privileges_layout = QVBoxLayout()
        
        # Different privileges based on role
        privileges_text = QLabel()
        if self.current_user and self.current_user['role'] == 'admin':
            privileges_text.setText("""
                As an Administrator, you have access to:
                • User Management (create, modify, and delete user accounts)
                • System Settings and Configuration
                • All Automata Operations and Features
                • Full Access to All System Functions
            """)
        else:
            privileges_text.setText("""
                As a Regular User, you have access to:
                • Basic Automata Operations
                • Create and Manage Your Own Automata
                • Execute Standard Operations
                • View and Modify Your Account Settings
            """)
        
        privileges_text.setStyleSheet("""
            QLabel {
                color: #D0D7E3;
                font-size: 13px;
                padding: 10px;
            }
        """)
        privileges_text.setWordWrap(True)
        privileges_layout.addWidget(privileges_text)
        privileges_group.setLayout(privileges_layout)
        
        # Add everything to layouts
        content_layout.addWidget(account_group)
        content_layout.addWidget(privileges_group)
        content_layout.addStretch(1)
        
        layout.addWidget(title_label)
        layout.addWidget(content_frame, 1)
        
        self.setLayout(layout)

