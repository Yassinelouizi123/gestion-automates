# user_management.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QHeaderView, QPushButton, QTableWidgetItem

class UserManagementTab(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # User table
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(4)
        self.user_table.setHorizontalHeaderLabels(['Username', 'Role', 'Active', 'Actions'])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.load_users)
        
        layout.addWidget(self.user_table)
        layout.addWidget(self.refresh_btn)
        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        users = self.user_manager.get_all_users()
        self.user_table.setRowCount(len(users))
        
        for row, user in enumerate(users):
            self.user_table.setItem(row, 0, QTableWidgetItem(user['username']))
            self.user_table.setItem(row, 1, QTableWidgetItem(user['role']))
            self.user_table.setItem(row, 2, QTableWidgetItem(str(user['is_active'])))
            
            # Add action buttons
            toggle_btn = QPushButton("Toggle Active")
            toggle_btn.clicked.connect(lambda _, u=user: self.toggle_user_active(u))
            self.user_table.setCellWidget(row, 3, toggle_btn)

    def toggle_user_active(self, user):
        new_state = not user['is_active']
        self.user_manager.set_user_active(user['username'], new_state)
        self.load_users()