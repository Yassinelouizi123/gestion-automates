from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
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
        
        self.content_button = ModernTabButton("Content")
        self.content_button.setChecked(True)
        self.content_button.clicked.connect(lambda: self.set_active_tab(0))
        
        self.settings_button = ModernTabButton("Settings")
        self.settings_button.clicked.connect(lambda: self.set_active_tab(1))
        
        tab_bar_layout.addWidget(self.content_button)
        tab_bar_layout.addWidget(self.settings_button)
        tab_bar_layout.addStretch(1)
        
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
        self.content_widget = ContentWidget()
        self.settings_widget = SettingsWidget()
        
        self.content_stack.addWidget(self.content_widget)
        self.content_stack.addWidget(self.settings_widget)
        
        # Add widgets to the content layout
        content_layout.addWidget(self.sidebar)
        content_layout.addWidget(self.content_stack, 1)
        
        # Add everything to the main layout
        layout.addWidget(tab_bar)
        layout.addWidget(content_area, 1)
        
        self.setLayout(layout)
        
        # Connect signals
        self.sidebar.item_clicked.connect(self.handle_sidebar_click)

        if self.current_user['role'] == 'admin':
            self.add_admin_features()
    
    def set_active_tab(self, index):
        self.content_stack.setCurrentIndex(index)
        
        # Update button states
        self.content_button.setChecked(index == 0)
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.user_manager = UserManager()
        self.current_user = None
        self.initUI()

    def initUI(self):
        self.stacked_widget = QStackedWidget()
        self.login_widget = LoginWidget(self.user_manager)
        self.login_widget.login_successful.connect(self.handle_login_success)
        self.stacked_widget.addWidget(self.login_widget)
        self.setCentralWidget(self.stacked_widget)
        self.setMinimumSize(1100, 700)

    def handle_login_success(self, user_data):
        self.current_user = user_data
        self.main_widget = MainWidget(self.current_user, self.user_manager)
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.setCurrentWidget(self.main_widget)
        self.apply_user_permissions()

    def apply_user_permissions(self):
        if self.current_user['role'] != 'admin':
            # Disable admin-only features
            self.main_widget.sidebar.delete_btn.setVisible(False)
            self.main_widget.sidebar.user_mgmt_btn.setVisible(False)
            self.main_widget.content_widget.user_management_tab.setVisible(False)