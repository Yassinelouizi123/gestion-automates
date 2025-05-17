from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget, QPushButton
from PyQt6.QtCore import Qt
from login import LoginWidget
from sidebar import SidebarWidget
from content import ContentWidget
from settings import SettingsWidget
from custom_widgets import ModernTabButton
from user_management import UserManagementTab  # Import the missing class
from user_manager import UserManager



class MainWidget(QWidget):
    def __init__(self, current_user, user_manager):
        super().__init__()
        self.current_user = current_user
        self.user_manager = user_manager
        self.initUI()
        
    def initUI(self):
        # Main layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Tab bar
        tab_bar = QWidget()
        tab_bar.setStyleSheet("background-color: #121B2E;")
        tab_bar_layout = QHBoxLayout(tab_bar)
        tab_bar_layout.setContentsMargins(20, 0, 20, 0)
        
        # Left side - tabs
        tabs_layout = QHBoxLayout()
        self.content_button = ModernTabButton("Content")
        self.content_button.setChecked(True)
        self.content_button.clicked.connect(lambda: self.set_active_tab(0))
        
        self.settings_button = ModernTabButton("Settings")
        self.settings_button.clicked.connect(lambda: self.set_active_tab(2))  # Changed from 1 to 2

        # Add user management tab if user is admin
        self.user_mgmt_button = None
        if self.current_user['role'] == 'admin':
            self.user_mgmt_button = ModernTabButton("User Management")
            self.user_mgmt_button.clicked.connect(lambda: self.set_active_tab(1))  # This is correct at 1
        
        tabs_layout.addWidget(self.content_button)
        if self.user_mgmt_button:
            tabs_layout.addWidget(self.user_mgmt_button)
        tabs_layout.addWidget(self.settings_button)
        tabs_layout.addStretch(1)
        
        # Right side - logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #FF6B81;
            }
        """)
        self.logout_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.logout_button.clicked.connect(self.handle_logout)
        
        tab_bar_layout.addLayout(tabs_layout)
        tab_bar_layout.addWidget(self.logout_button)
        
        # Main content area with sidebar and content
        content_area = QWidget()
        content_area.setStyleSheet("background-color: #0E1525;")
        content_layout = QHBoxLayout(content_area)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Create sidebar
        self.sidebar = SidebarWidget()
        self.sidebar.setFixedWidth(260)
        
        # Create stacked widget for main content
        self.content_stack = QStackedWidget()
        self.content_widget = ContentWidget(user_manager=self.user_manager, current_user=self.current_user)
        self.settings_widget = SettingsWidget(user_manager=self.user_manager, current_user=self.current_user)
        
        # Add widgets in the correct order
        self.content_stack.addWidget(self.content_widget)  # index 0
        
        # Add user management widget if user is admin
        if self.current_user['role'] == 'admin':
            self.user_mgmt_widget = UserManagementTab(self.user_manager)
            self.content_stack.addWidget(self.user_mgmt_widget)  # index 1
            
        self.content_stack.addWidget(self.settings_widget)  # index 2 for admin, 1 for non-admin
        
        # Add widgets to the content layout
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.content_stack, 1)
        
        # Add everything to the main layout
        layout.addWidget(tab_bar)
        layout.addWidget(content_area, 1)
        
        self.setLayout(layout)
        
        # Connect signals
        self.sidebar.item_clicked.connect(self.handle_sidebar_click)
    
    def set_active_tab(self, index):
        # For non-admin users, if they click settings (index 2), we need to adjust to 1
        # since there is no user management tab
        if not self.user_mgmt_button and index == 2:
            index = 1
            
        self.content_stack.setCurrentIndex(index)
        
        # Update button states
        self.content_button.setChecked(index == 0)
        if self.user_mgmt_button:
            self.user_mgmt_button.setChecked(index == 1)
            self.settings_button.setChecked(index == 2)
        else:
            self.settings_button.setChecked(index == 1)
    
    def handle_sidebar_click(self, category, action):
        # Go to content tab
        self.set_active_tab(0)
        
        # Update content
        self.content_widget.update_content(category, action)

    def add_admin_features(self):
        # Add user management tab
        self.user_mgmt_tab = UserManagementTab(self.user_manager)
        self.content_stack.addWidget(self.user_mgmt_tab)
        
        # Add admin sidebar items
        self.sidebar.add_admin_menu_items()

    def handle_logout(self):
        # Handle logout logic here
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.current_user = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Finite Automata Manager")
        self.stacked_widget = QStackedWidget()
        self.login_widget = LoginWidget(self.user_manager)
        self.login_widget.login_successful.connect(self.handle_login_success)
        self.stacked_widget.addWidget(self.login_widget)
        self.setCentralWidget(self.stacked_widget)
        self.setMinimumSize(1100, 700)

    def handle_login_success(self, user_data):
        self.current_user = user_data
        self.main_widget = MainWidget(self.current_user, self.user_manager)
        self.main_widget.logout_button.clicked.connect(self.handle_logout)  # Connect logout signal
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.setCurrentWidget(self.main_widget)

    def handle_logout(self):
        # Reset the current user
        self.current_user = None
        self.user_manager.current_user = None  # Reset current user in UserManager
        
        # Remove the main widget and show login
        if self.main_widget:
            self.stacked_widget.removeWidget(self.main_widget)
            self.main_widget = None
            
        # Clear the login fields and show login widget
        self.login_widget.username_edit.clear()
        self.login_widget.password_edit.clear()
        self.stacked_widget.setCurrentWidget(self.login_widget)