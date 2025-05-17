from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout, 
                            QGraphicsDropShadowEffect, QGroupBox, QFormLayout, QLineEdit, 
                            QComboBox, QCheckBox, QPushButton, QMessageBox, QTableWidget, 
                            QTableWidgetItem, QDialog, QHeaderView)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from custom_widgets import ModernSlider

class ResetPasswordDialog(QDialog):
    def __init__(self, user_manager, username, parent=None):
        super().__init__(parent)
        self.user_manager = user_manager
        self.username = username
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle(f"Reset Password for {self.username}")
        self.setFixedWidth(400)
        layout = QVBoxLayout()
        
        # Password fields
        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)
        
        # Style for labels
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setStyleSheet("""
            QDialog {
                background-color: #1A2133;
            }
            QLabel {
                background: transparent;
                color: white;
                border: none;
            }
        """)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        self.confirm_password = QLineEdit()
        self.confirm_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password.setStyleSheet("""
            QLineEdit {
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        form_layout.addRow("New Password:", self.new_password)
        form_layout.addRow("Confirm Password:", self.confirm_password)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("Reset Password")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
        """)
        save_btn.clicked.connect(self.reset_password)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #1A2133;
                color: white;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #242E48;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        # Add layouts to main layout
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def reset_password(self):
        new_pwd = self.new_password.text()
        confirm_pwd = self.confirm_password.text()
        
        if not new_pwd or not confirm_pwd:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        if new_pwd != confirm_pwd:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return
            
        if len(new_pwd) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
            
        if self.user_manager.update_password(self.username, new_pwd):
            QMessageBox.information(self, "Success", "Password has been reset successfully")
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to reset password")

class UserManagementTab(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header
        title_label = QLabel("User Management")
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
        
        # User List section
        user_list_group = QGroupBox("User Accounts")
        user_list_group.setStyleSheet("""
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
        
        user_list_layout = QVBoxLayout()
        
        # Add search and filter controls
        filter_layout = QHBoxLayout()
        
        # Search bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by username...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        self.search_input.textChanged.connect(self.filter_users)
        
        # Role filter
        self.role_filter = QComboBox()
        self.role_filter.addItems(['All Roles', 'admin', 'user'])
        self.role_filter.setStyleSheet("""
            QComboBox {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
        """)
        self.role_filter.currentTextChanged.connect(self.filter_users)

        # Status filter
        self.status_filter = QComboBox()
        self.status_filter.addItems(['All Status', 'Active', 'Inactive'])
        self.status_filter.setStyleSheet("""
            QComboBox {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 120px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
        """)
        self.status_filter.currentTextChanged.connect(self.filter_users)
        
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(QLabel("Role:"))
        filter_layout.addWidget(self.role_filter)
        filter_layout.addWidget(QLabel("Status:"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        
        user_list_layout.addLayout(filter_layout)
        
        # Create table for user list
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(5)
        self.user_table.setHorizontalHeaderLabels(['Username', 'Role', 'Status', 'Created At','Actions'])
        
        # Set minimum row height and vertical header width
        self.user_table.verticalHeader().setDefaultSectionSize(40)
        self.user_table.verticalHeader().setMinimumSectionSize(35)
        self.user_table.verticalHeader().setFixedWidth(30)  # Fix the width of row numbers
        
        # Set column widths
        header = self.user_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Interactive)
        
        # Set minimum widths for columns
        self.user_table.setColumnWidth(0, 80)
        self.user_table.setColumnWidth(1, 70)
        self.user_table.setColumnWidth(2, 70)
        self.user_table.setColumnWidth(3, 130)
        self.user_table.setColumnWidth(4, 300)
        
        self.user_table.setStyleSheet("""
            QTableWidget {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                color: white;
                gridline-color: #2A3344;
            }
            QHeaderView::section {
                background-color: #1A2133;
                color: white;
                border: 1px solid #2A3344;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QHeaderView::section:vertical {
                width: 30px;
            }
        """)
        
        # Refresh button for user list
        refresh_btn = QPushButton("Refresh User List")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_user_list)
        
        user_list_layout.addWidget(self.user_table)
        user_list_layout.addWidget(refresh_btn)
        user_list_group.setLayout(user_list_layout)
        content_layout.addWidget(user_list_group)
        
        # Create new user section
        user_mgmt_group = QGroupBox("Create New User")
        user_mgmt_group.setStyleSheet("""
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
        
        user_mgmt_layout = QFormLayout()
        
        # New user fields
        self.new_username = QLineEdit()
        self.new_username.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        self.new_password = QLineEdit()
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        self.role_combo = QComboBox()
        self.role_combo.addItems(['user', 'admin'])
        self.role_combo.setStyleSheet("""
            QComboBox {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid white;
                margin-right: 8px;
            }
        """)
        
        self.active_checkbox = QCheckBox()
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setStyleSheet("QCheckBox { color: white; }")
        
        user_mgmt_layout.addRow("Username:", self.new_username)
        user_mgmt_layout.addRow("Password:", self.new_password)
        user_mgmt_layout.addRow("Role:", self.role_combo)
        user_mgmt_layout.addRow("Active:", self.active_checkbox)
        
        # Create user button
        self.create_user_btn = QPushButton("Create User")
        self.create_user_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
        """)
        self.create_user_btn.clicked.connect(self.create_new_user)
        
        user_mgmt_layout.addRow("", self.create_user_btn)
        user_mgmt_group.setLayout(user_mgmt_layout)
        content_layout.addWidget(user_mgmt_group)
        
        layout.addWidget(title_label)
        layout.addWidget(content_frame, 1)
        
        self.setLayout(layout)
        
        # Load initial user list
        self.refresh_user_list()

    def refresh_user_list(self):
        if not self.user_manager:
            return
            
        users = self.user_manager.get_all_users()
        self.user_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            # Username
            username_item = QTableWidgetItem(user['username'])
            username_item.setFlags(username_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 0, username_item)
            
            # Role
            role_item = QTableWidgetItem(user['role'])
            role_item.setFlags(role_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 1, role_item)
            
            # Status
            status = "Active" if user['is_active'] else "Inactive"
            status_item = QTableWidgetItem(status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 2, status_item)
            
            # Created At
            created_at_item = QTableWidgetItem(str(user['created_at']))
            created_at_item.setFlags(created_at_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 3, created_at_item)
            
            # Actions column with multiple buttons
            if user['username'] != self.user_manager.current_user['username']:
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(2, 2, 2, 2)
                actions_layout.setSpacing(4)
                
                # Toggle active button
                toggle_btn = QPushButton("Deactivate" if user['is_active'] else "Activate")
                toggle_btn.setFixedHeight(28)
                toggle_btn.setMinimumWidth(85)
                toggle_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {("#FF4757" if user['is_active'] else "#2ED573")};
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }}
                    QPushButton:hover {{
                        background-color: {("#FF6B81" if user['is_active'] else "#7BED9F")};
                    }}
                """)
                toggle_btn.clicked.connect(lambda checked, u=user: self.toggle_user_active(u))
                
                # Reset password button
                reset_pwd_btn = QPushButton("Reset Password")
                reset_pwd_btn.setFixedHeight(28)
                reset_pwd_btn.setMinimumWidth(95)
                reset_pwd_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #7B42F6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #6935D8;
                    }
                """)
                reset_pwd_btn.clicked.connect(lambda checked, u=user: self.show_reset_password_dialog(u))
                
                # Delete account button
                delete_btn = QPushButton("Delete Account")
                delete_btn.setFixedHeight(28)
                delete_btn.setMinimumWidth(90)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #DC3545;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #C82333;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, u=user: self.delete_user_account(u))
                
                actions_layout.addWidget(toggle_btn)
                actions_layout.addWidget(reset_pwd_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.addStretch()
                
                actions_widget.setMinimumWidth(290)
                self.user_table.setCellWidget(row, 4, actions_widget)
            else:
                current_user_item = QTableWidgetItem("Current User")
                current_user_item.setFlags(current_user_item.flags() & ~(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable))
                current_user_item.setForeground(QColor("#8A98AC"))
                self.user_table.setItem(row, 4, current_user_item)

    def toggle_user_active(self, user):
        new_state = not user['is_active']
        if self.user_manager.set_user_active(user['username'], new_state):
            status = "activated" if new_state else "deactivated"
            QMessageBox.information(self, "Success", f"User {user['username']} has been {status}")
            self.refresh_user_list()
        else:
            QMessageBox.warning(self, "Error", f"Failed to update status for user {user['username']}")
    
    def create_new_user(self):
        if not self.user_manager:
            return
            
        username = self.new_username.text().strip()
        password = self.new_password.text().strip()
        
        if not username or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return
            
        if len(password) < 8:
            QMessageBox.warning(self, "Error", "Password must be at least 8 characters")
            return
            
        success = self.user_manager.create_user(
            username=username,
            password=password,
            role=self.role_combo.currentText(),
            active=self.active_checkbox.isChecked()
        )
        
        if success:
            QMessageBox.information(self, "Success", "User created successfully")
            self.new_username.clear()
            self.new_password.clear()
            self.refresh_user_list()
        else:
            QMessageBox.warning(self, "Error", "Failed to create user. Username might already exist.")
    
    def show_reset_password_dialog(self, user):
        dialog = ResetPasswordDialog(self.user_manager, user['username'], self)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #1A2133;
                color: white;
            }
            QLabel {
                color: white;
            }
        """)
        dialog.exec()
    
    def delete_user_account(self, user):
        reply = QMessageBox.question(
            self,
            'Confirm Deletion',
            f'Are you sure you want to delete the account for {user["username"]}?\nThis action cannot be undone.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.user_manager.delete_user(user['username'], self.user_manager.current_user):
                QMessageBox.information(self, "Success", f"User account {user['username']} has been deleted")
                self.refresh_user_list()
            else:
                QMessageBox.warning(self, "Error", f"Failed to delete user account {user['username']}")

    def filter_users(self):
        search_text = self.search_input.text().lower()
        role_filter = self.role_filter.currentText()
        status_filter = self.status_filter.currentText()
        
        # Store current column widths before filtering
        column_widths = []
        for i in range(self.user_table.columnCount()):
            column_widths.append(self.user_table.columnWidth(i))
        
        # Get all users and filter them
        users = self.user_manager.get_all_users()
        filtered_users = []
        
        for user in users:
            matches_search = (search_text == "" or 
                            search_text in user['username'].lower())
            matches_role = (role_filter == 'All Roles' or 
                          role_filter.lower() == user['role'].lower())
            matches_status = (status_filter == 'All Status' or 
                            (status_filter == 'Active' and user['is_active']) or 
                            (status_filter == 'Inactive' and not user['is_active']))
            
            if matches_search and matches_role and matches_status:
                filtered_users.append(user)
        
        # Update table with filtered users
        self.user_table.setRowCount(len(filtered_users))
        for row, user in enumerate(filtered_users):
            # Username
            username_item = QTableWidgetItem(user['username'])
            username_item.setFlags(username_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 0, username_item)
            
            # Role
            role_item = QTableWidgetItem(user['role'])
            role_item.setFlags(role_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 1, role_item)
            
            # Status
            status = "Active" if user['is_active'] else "Inactive"
            status_item = QTableWidgetItem(status)
            status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 2, status_item)
            
            # Created At
            created_at_item = QTableWidgetItem(str(user['created_at']))
            created_at_item.setFlags(created_at_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.user_table.setItem(row, 3, created_at_item)
            
            # Re-add action buttons
            if user['username'] != self.user_manager.current_user['username']:
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(2, 2, 2, 2)
                actions_layout.setSpacing(4)
                
                # Toggle active button
                toggle_btn = QPushButton("Deactivate" if user['is_active'] else "Activate")
                toggle_btn.setFixedHeight(28)
                toggle_btn.setMinimumWidth(85)
                toggle_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {("#FF4757" if user['is_active'] else "#2ED573")};
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }}
                    QPushButton:hover {{
                        background-color: {("#FF6B81" if user['is_active'] else "#7BED9F")};
                    }}
                """)
                toggle_btn.clicked.connect(lambda checked, u=user: self.toggle_user_active(u))
                
                # Reset password button
                reset_pwd_btn = QPushButton("Reset Password")
                reset_pwd_btn.setFixedHeight(28)
                reset_pwd_btn.setMinimumWidth(95)
                reset_pwd_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #7B42F6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #6935D8;
                    }
                """)
                reset_pwd_btn.clicked.connect(lambda checked, u=user: self.show_reset_password_dialog(u))
                
                # Delete account button
                delete_btn = QPushButton("Delete Account")
                delete_btn.setFixedHeight(28)
                delete_btn.setMinimumWidth(90)
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #DC3545;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 3px 8px;
                        font-weight: bold;
                        font-size: 11px;
                    }
                    QPushButton:hover {
                        background-color: #C82333;
                    }
                """)
                delete_btn.clicked.connect(lambda checked, u=user: self.delete_user_account(u))
                
                actions_layout.addWidget(toggle_btn)
                actions_layout.addWidget(reset_pwd_btn)
                actions_layout.addWidget(delete_btn)
                actions_layout.addStretch()
                
                actions_widget.setMinimumWidth(290)
                self.user_table.setCellWidget(row, 4, actions_widget)
            else:
                current_user_item = QTableWidgetItem("Current User")
                current_user_item.setFlags(current_user_item.flags() & ~(Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsSelectable))
                current_user_item.setForeground(QColor("#8A98AC"))
                self.user_table.setItem(row, 4, current_user_item)
        
        # Restore column widths after filtering
        for i, width in enumerate(column_widths):
            self.user_table.setColumnWidth(i, width)