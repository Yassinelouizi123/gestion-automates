from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, 
                            QPushButton, QMessageBox, QGraphicsDropShadowEffect, QComboBox, QCheckBox)
from user_manager import UserManager  
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QColor
from custom_widgets import ModernButton

class LoginWidget(QWidget):
    login_successful = pyqtSignal(dict)  # Emit user data on success

    def __init__(self, user_manager: UserManager):
        super().__init__()
        self.user_manager = user_manager
        self.initUI()
        
        
    def initUI(self):
        # Set up the layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create left panel (dark blue with logo)
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: #0E1525;")
        left_panel.setFixedWidth(360)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo placeholder
        logo_label = QLabel("FA Manager")
        logo_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("color: #7B42F6; margin-bottom: 20px;")
        
        # Description
        desc_label = QLabel("Advanced Finite Automata Management Tool")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #8A98AC; font-size: 14px; margin-bottom: 30px;")
        
        left_layout.addStretch(1)
        left_layout.addWidget(logo_label)
        left_layout.addWidget(desc_label)
        left_layout.addStretch(1)
        
        # Create right panel (login form)
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: #121B2E;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(50, 40, 50, 40)
        right_layout.setSpacing(20)
        
        # Login title
        login_title = QLabel("Sign In")
        login_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        login_title.setStyleSheet("color: white; margin-bottom: 20px;")
        
        # Username field
        username_label = QLabel("Username")
        username_label.setStyleSheet("color: #8A98AC; font-size: 13px; font-weight: bold;")
        
        self.username_edit = QLineEdit()
        self.username_edit.setFixedHeight(45)
        self.username_edit.setStyleSheet("""
            QLineEdit {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 5px 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #7B42F6;
            }
        """)
        
        # Password field
        password_label = QLabel("Password")
        password_label.setStyleSheet("color: #8A98AC; font-size: 13px; font-weight: bold;")
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_edit.setFixedHeight(45)
        self.password_edit.setStyleSheet("""
            QLineEdit {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 5px 15px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #7B42F6;
            }
        """)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.setFixedHeight(45)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        
        # Add drop shadow to login button
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(123, 66, 246, 100))
        shadow.setOffset(0, 5)
        self.login_button.setGraphicsEffect(shadow)
        
        self.login_button.clicked.connect(self.attempt_login)
        
        # Add widgets to right layout
        right_layout.addWidget(login_title)
        right_layout.addSpacing(10)
        right_layout.addWidget(username_label)
        right_layout.addWidget(self.username_edit)
        right_layout.addSpacing(10)
        right_layout.addWidget(password_label)
        right_layout.addWidget(self.password_edit)
        right_layout.addSpacing(20)
        right_layout.addWidget(self.login_button)
        right_layout.addStretch(1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        # Connect enter key to login button
        self.password_edit.returnPressed.connect(self.login_button.click)
        self.username_edit.returnPressed.connect(self.password_edit.setFocus)

        self.role_combobox = QComboBox()
        self.role_combobox.addItems(['user', 'admin'])
        self.role_combobox.hide()
        
        # Add "Create User" toggle
        self.create_user_checkbox = QCheckBox("Create new user")
        self.create_user_checkbox.toggled.connect(self.toggle_create_user_mode)
        right_layout.insertWidget(1, self.create_user_checkbox)
        
        # Add active user checkbox
        self.active_checkbox = QCheckBox("Active user")
        self.active_checkbox.hide()
        right_layout.insertWidget(7, self.active_checkbox)
        
        # Modify login button
        self.login_button.setText("Sign In / Create User")
    
    def attempt_login(self):
        # For demo purposes, accept any non-empty username/password
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if username and password:
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")
    
    def toggle_create_user_mode(self, checked):
        if checked:
            self.login_button.setText("Create User")
            self.role_combobox.show()
            self.active_checkbox.show()
        else:
            self.login_button.setText("Sign In")
            self.role_combobox.hide()
            self.active_checkbox.hide()
        
    def attempt_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if self.create_user_checkbox.isChecked():
            if self.user_manager.get_user(username):
                QMessageBox.warning(self, "Error", "Username already exists!")
                return
                
            if len(password) < 8:
                QMessageBox.warning(self, "Error", "Password must be at least 8 characters!")
                return
                
            success = self.user_manager.create_user(
                username=username,
                password=password,
                role=self.role_combobox.currentText(),
                active=self.active_checkbox.isChecked()
            )
            
            if success:
                QMessageBox.information(self, "Success", "User created successfully!")
                self.create_user_checkbox.setChecked(False)
            return

        # Regular login
        valid, user = self.user_manager.authenticate(username, password)
        if valid:
            self.login_successful.emit(user)
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid credentials or inactive account!")
