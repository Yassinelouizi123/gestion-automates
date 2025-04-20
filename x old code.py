import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QStackedWidget, QScrollArea, QTreeWidget, QTreeWidgetItem,
                            QMessageBox, QFrame, QSplitter, QTextEdit, QFileDialog,
                            QGraphicsDropShadowEffect, QToolButton, QProgressBar,
                            QFormLayout, QGroupBox, QSpacerItem, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QPainter, QPen, QBrush, QLinearGradient

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


class LoginWidget(QWidget):
    login_successful = pyqtSignal()
    
    def __init__(self):
        super().__init__()
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
    
    def attempt_login(self):
        # For demo purposes, accept any non-empty username/password
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if username and password:
            self.login_successful.emit()
        else:
            QMessageBox.warning(self, "Login Failed", "Please enter both username and password.")


class SidebarWidget(QWidget):
    item_clicked = pyqtSignal(str, str)
    
    def __init__(self):
        super().__init__()
        self.current_button = None
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 8, 10)  # Reduced right margin to account for scrollbar spacing
        layout.setSpacing(0)
        
        # Create a scroll area for the menu
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
                border: none;
                padding-right: 12px;  /* Increased from 3mm */
            }
            QScrollBar:vertical {
                background-color: transparent;
                width: 8px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #2A3344;
                min-height: 20px;
                border-radius: 4px;
                margin: 2px;
            }
            QScrollBar::add-line:vertical, 
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
        """)
        
        # Container for menu items
        menu_container = QWidget()
        menu_layout = QVBoxLayout(menu_container)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(10)
        
        # Automata Management Section
        automata_management = MenuCategory("AUTOMATA MANAGEMENT")
        self.create_btn = automata_management.add_menu_item("Create New Automaton", 
            action=lambda: self.set_active_button("Create New Automaton"))
        self.load_btn = automata_management.add_menu_item("Load Automaton from File", 
            action=lambda: self.set_active_button("Load Automaton from File"))
        self.save_btn = automata_management.add_menu_item("Save Current Automaton", 
            action=lambda: self.set_active_button("Save Current Automaton"))
        self.list_btn = automata_management.add_menu_item("List Saved Automata", 
            action=lambda: self.set_active_button("List Saved Automata"))
        self.modify_btn = automata_management.add_menu_item("Modify Current Automaton", 
            action=lambda: self.set_active_button("Modify Current Automaton"))
        self.delete_btn = automata_management.add_menu_item("Delete Saved Automaton File", 
            action=lambda: self.set_active_button("Delete Saved Automaton File"))
        menu_layout.addWidget(automata_management)
        
        # Automata Analysis Section
        automata_analysis = MenuCategory("AUTOMATA ANALYSIS")
        self.check_det_btn = automata_analysis.add_menu_item("Check Determinism", 
            action=lambda: self.set_active_button("Check Determinism"))
        self.check_comp_btn = automata_analysis.add_menu_item("Check Completeness", 
            action=lambda: self.set_active_button("Check Completeness"))
        self.make_comp_btn = automata_analysis.add_menu_item("Make Automaton Complete", 
            action=lambda: self.set_active_button("Make Automaton Complete"))
        self.convert_btn = automata_analysis.add_menu_item("Convert NFA to DFA", 
            action=lambda: self.set_active_button("Convert NFA to DFA"))
        self.check_min_btn = automata_analysis.add_menu_item("Check Minimality", 
            action=lambda: self.set_active_button("Check Minimality"))
        self.min_btn = automata_analysis.add_menu_item("Minimize Automaton", 
            action=lambda: self.set_active_button("Minimize Automaton"))
        menu_layout.addWidget(automata_analysis)
        
        # Word/Language Operations Section
        word_operations = MenuCategory("WORD/LANGUAGE OPERATIONS")
        self.test_btn = word_operations.add_menu_item("Test Word Acceptance", 
            action=lambda: self.set_active_button("Test Word Acceptance"))
        self.gen_acc_btn = word_operations.add_menu_item("Generate Accepted Words", 
            action=lambda: self.set_active_button("Generate Accepted Words"))
        self.gen_rej_btn = word_operations.add_menu_item("Generate Rejected Words", 
            action=lambda: self.set_active_button("Generate Rejected Words"))
        self.check_eq_btn = word_operations.add_menu_item("Check Equivalence", 
            action=lambda: self.set_active_button("Check Equivalence"))
        self.union_btn = word_operations.add_menu_item("Compute Union", 
            action=lambda: self.set_active_button("Compute Union"))
        self.intersect_btn = word_operations.add_menu_item("Compute Intersection", 
            action=lambda: self.set_active_button("Compute Intersection"))
        self.complement_btn = word_operations.add_menu_item("Compute Complement", 
            action=lambda: self.set_active_button("Compute Complement"))
        menu_layout.addWidget(word_operations)
        
        # Other Section
        other_section = MenuCategory("OTHER")
        self.visualize_btn = other_section.add_menu_item("Visualize Current Automaton", 
            action=lambda: self.set_active_button("Visualize Current Automaton"))
        menu_layout.addWidget(other_section)
        
        menu_layout.addStretch(1)
        scroll_area.setWidget(menu_container)
        layout.addWidget(scroll_area)
        
        self.setLayout(layout)
        self.set_active_button("Create New Automaton")
    
    def set_active_button(self, button_name):
        # Reset previous button style
        if self.current_button:
            self.current_button.setStyleSheet("""
                QPushButton {
                    background-color: #1A2133;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    text-align: left;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #242E48;
                }
                QPushButton:pressed {
                    background-color: #192235;
                }
            """)
            self.current_button.setGraphicsEffect(None)
        
        # Find and style the new active button
        button_map = {
            "Create New Automaton": self.create_btn,
            "Load Automaton from File": self.load_btn,
            "Save Current Automaton": self.save_btn,
            "List Saved Automata": self.list_btn,
            "Modify Current Automaton": self.modify_btn,
            "Delete Saved Automaton File": self.delete_btn,
            "Check Determinism": self.check_det_btn,
            "Check Completeness": self.check_comp_btn,
            "Make Automaton Complete": self.make_comp_btn,
            "Convert NFA to DFA": self.convert_btn,
            "Check Minimality": self.check_min_btn,
            "Minimize Automaton": self.min_btn,
            "Test Word Acceptance": self.test_btn,
            "Generate Accepted Words": self.gen_acc_btn,
            "Generate Rejected Words": self.gen_rej_btn,
            "Check Equivalence": self.check_eq_btn,
            "Compute Union": self.union_btn,
            "Compute Intersection": self.intersect_btn,
            "Compute Complement": self.complement_btn,
            "Visualize Current Automaton": self.visualize_btn
        }
        
        if button_name in button_map:
            self.current_button = button_map[button_name]
            self.current_button.setStyleSheet("""
                QPushButton {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #7B42F6, stop:1 #00C2FF
                    );
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 8px 15px;
                    text-align: left;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6935D8, stop:1 #00A8E0
                    );
                }
                QPushButton:pressed {
                    background-color: qlineargradient(
                        x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5D2EC2, stop:1 #0095C7
                    );
                }
            """)
            
            # Add glow effect
            glow = QGraphicsDropShadowEffect()
            glow.setBlurRadius(15)
            glow.setColor(QColor(123, 66, 246, 150))
            glow.setOffset(0, 0)
            self.current_button.setGraphicsEffect(glow)
            
            # Emit signal with category information
            category = self.get_category_for_button(button_name)
            self.item_clicked.emit(category, button_name)
    
    def get_category_for_button(self, button_name):
        if button_name in [
            "Create New Automaton", "Load Automaton from File", 
            "Save Current Automaton", "List Saved Automata",
            "Modify Current Automaton", "Delete Saved Automaton File"
        ]:
            return "management"
        elif button_name in [
            "Check Determinism", "Check Completeness", 
            "Make Automaton Complete", "Convert NFA to DFA",
            "Check Minimality", "Minimize Automaton"
        ]:
            return "analysis"
        elif button_name in [
            "Test Word Acceptance", "Generate Accepted Words",
            "Generate Rejected Words", "Check Equivalence",
            "Compute Union", "Compute Intersection", "Compute Complement"
        ]:
            return "operations"
        else:
            return "other"

class ContentWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header area
        header_layout = QHBoxLayout()
        self.title_label = QLabel("Welcome to Finite Automata Manager")
        self.title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)
        
        # Create pages for different operations
        self.create_welcome_page()
        self.create_automaton_creation_page()
        self.create_determinism_check_page()
        self.create_visualization_page()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.stacked_widget, 1)
        
    def create_welcome_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            #contentFrame {
                background-color: #1A2133;
                border-radius: 10px;
            }
        """)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 3)
        content_frame.setGraphicsEffect(shadow)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        description = QTextEdit()
        description.setReadOnly(True)
        description.setFrameShape(QFrame.Shape.NoFrame)
        description.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #D0D7E3;
                border: none;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        description.setHtml("""
            <h3 style='color:white; margin-top:0;'>Finite Automata Manager</h3>
            <p>This advanced tool allows you to create, edit, and analyze finite automata with a modern, intuitive interface.</p>
            <p>Use the sidebar menu to:</p>
            <ul style='color:#8A98AC;'>
                <li><span style='color:#D0D7E3;'>Create and manage automata</span> - Define states, alphabet, transitions, and more</li>
                <li><span style='color:#D0D7E3;'>Analyze properties</span> - Check determinism, completeness, and minimize automata</li>
                <li><span style='color:#D0D7E3;'>Test word acceptance</span> - Verify if words are accepted by your automata</li>
                <li><span style='color:#D0D7E3;'>Perform language operations</span> - Union, intersection, and complement operations</li>
                <li><span style='color:#D0D7E3;'>Visualize automata</span> - Generate graphical representations</li>
            </ul>
            <p>Select an option from the menu to get started.</p>
        """)
        
        content_layout.addWidget(description)
        layout.addWidget(content_frame)
        self.stacked_widget.addWidget(page)

    def create_automaton_creation_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Automaton Definition")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 8px;
                margin-top: 10px;
                color: white;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        form_layout = QFormLayout()
        form_layout.setContentsMargins(20, 20, 20, 20)
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        
        # States Input
        self.states_input = QLineEdit()
        self.states_input.setPlaceholderText("Enter states separated by commas (q0, q1, ...)")
        self.states_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        # Alphabet Input
        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText("Enter alphabet symbols separated by commas (a, b, ...)")
        self.alphabet_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
        """)
        
        # Transitions Input
        self.transitions_input = QTextEdit()
        self.transitions_input.setPlaceholderText("Enter transitions in format: q0,a→q1 (one per line)")
        self.transitions_input.setStyleSheet("""
            QTextEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-height: 100px;
            }
        """)
        
        # Initial State
        self.initial_state = QLineEdit()
        self.initial_state.setPlaceholderText("Enter initial state")
        
        # Final States
        self.final_states = QLineEdit()
        self.final_states.setPlaceholderText("Enter final states separated by commas")
        
        form_layout.addRow(QLabel("States:"), self.states_input)
        form_layout.addRow(QLabel("Alphabet:"), self.alphabet_input)
        form_layout.addRow(QLabel("Transitions:"), self.transitions_input)
        form_layout.addRow(QLabel("Initial State:"), self.initial_state)
        form_layout.addRow(QLabel("Final States:"), self.final_states)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_btn = ModernButton("Create Automaton")
        self.clear_btn = ModernButton("Clear Fields", accent_color="#FF4757")
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.create_btn)
        form_layout.addRow(button_layout)
        
        group.setLayout(form_layout)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def create_determinism_check_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Determinism Check")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 8px;
                margin-top: 10px;
                color: white;
                font-weight: bold;
            }
        """)
        
        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)
        
        self.check_result = QLabel()
        self.check_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.check_result.setText("No automaton loaded. Please create or load an automaton first.")
        
        self.check_btn = ModernButton("Check Determinism")
        self.check_btn.setFixedWidth(200)
        
        content.addWidget(self.check_result)
        content.addWidget(self.check_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def create_visualization_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Visualization")
        group.setStyleSheet("""
            QGroupBox {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 8px;
                margin-top: 10px;
                color: white;
                font-weight: bold;
            }
        """)
        
        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)
        
        self.visualization_label = QLabel()
        self.visualization_label.setStyleSheet("""
            QLabel {
                background-color: #121B2E;
                border-radius: 5px;
                min-height: 300px;
            }
        """)
        self.visualization_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.visualization_label.setText("Automaton visualization will appear here")
        
        btn_layout = QHBoxLayout()
        self.export_btn = ModernButton("Export as PNG", accent_color="#2ED573")
        self.refresh_btn = ModernButton("Refresh View")
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(self.export_btn)
        
        content.addWidget(self.visualization_label)
        content.addLayout(btn_layout)
        group.setLayout(content)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def update_content(self, category, action):
        page_map = {
            "Create New Automaton": 1,
            "Check Determinism": 2,
            "Visualize Current Automaton": 3
        }
        
        if action in page_map:
            self.stacked_widget.setCurrentIndex(page_map[action])
            self.title_label.setText(action)
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.title_label.setText("Welcome to Finite Automata Manager")

            
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)
        
        # Header area
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Welcome to Finite Automata Manager")
        self.title_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: white;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)
        
        # Content area with shadow and rounded corners
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_frame.setStyleSheet("""
            #contentFrame {
                background-color: #1A2133;
                border-radius: 10px;
            }
        """)
        
        # Add drop shadow to content frame
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 3)
        content_frame.setGraphicsEffect(shadow)
        
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setFrameShape(QFrame.Shape.NoFrame)
        self.description.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #D0D7E3;
                border: none;
                font-size: 14px;
                line-height: 1.5;
            }
        """)
        self.description.setHtml("""
            <h3 style='color:white; margin-top:0;'>Finite Automata Manager</h3>
            <p>This advanced tool allows you to create, edit, and analyze finite automata with a modern, intuitive interface.</p>
            <p>Use the sidebar menu to:</p>
            <ul style='color:#8A98AC;'>
                <li><span style='color:#D0D7E3;'>Create and manage automata</span> - Define states, alphabet, transitions, and more</li>
                <li><span style='color:#D0D7E3;'>Analyze properties</span> - Check determinism, completeness, and minimize automata</li>
                <li><span style='color:#D0D7E3;'>Test word acceptance</span> - Verify if words are accepted by your automata</li>
                <li><span style='color:#D0D7E3;'>Perform language operations</span> - Union, intersection, and complement operations</li>
                <li><span style='color:#D0D7E3;'>Visualize automata</span> - Generate graphical representations</li>
            </ul>
            <p>Select an option from the menu to get started.</p>
        """)
        
        content_layout.addWidget(self.description)
        
        # Add everything to the main layout
        layout.addLayout(header_layout)
        layout.addWidget(content_frame, 1)
        
        self.setLayout(layout)
    
    def update_content(self, category, action):
        # Update the content area based on the selected operation
        if "Create New Automaton" in action:
            self.title_label.setText("Create New Automaton")
            content = """
            <h3 style='color:white; margin-top:0;'>Create New Finite Automaton</h3>
            <p>Design a new finite automaton by defining all its components.</p>
            
            <h4 style='color:#00C2FF;'>Components</h4>
            <ul style='color:#8A98AC;'>
                <li><span style='color:#D0D7E3;'>States (Q)</span> - Define all states in your automaton</li>
                <li><span style='color:#D0D7E3;'>Input alphabet (Σ)</span> - Specify the set of input symbols</li>
                <li><span style='color:#D0D7E3;'>Transition function (δ)</span> - Define transitions between states</li>
                <li><span style='color:#D0D7E3;'>Initial state (q₀)</span> - Select the starting state</li>
                <li><span style='color:#D0D7E3;'>Final states (F)</span> - Choose which states are accepting</li>
            </ul>
            
            <p>Use the form below to define your automaton's components:</p>
            """
            self.description.setHtml(content)
            
        elif "Check Determinism" in action:
            self.title_label.setText("Check Determinism")
            content = """
            <h3 style='color:white; margin-top:0;'>Check Automaton Determinism</h3>
            <p>This operation analyzes whether the current automaton is deterministic (DFA).</p>
            
            <h4 style='color:#00C2FF;'>Deterministic Finite Automaton (DFA)</h4>
            <p>An automaton is deterministic if and only if:</p>
            <ul style='color:#8A98AC;'>
                <li><span style='color:#D0D7E3;'>It has exactly one initial state</span></li>
                <li><span style='color:#D0D7E3;'>For each state and input symbol, there is exactly one transition</span></li>
                <li><span style='color:#D0D7E3;'>There are no ε-transitions (empty string transitions)</span></li>
            </ul>
            
            <div style='background-color:#1E273D; padding:15px; border-radius:5px; margin-top:20px;'>
                <p style='color:#00C2FF; font-weight:bold; margin-top:0;'>Current Automaton Status</p>
                <p>Select or create an automaton first to check its determinism.</p>
            </div>
            """
            self.description.setHtml(content)
            
        elif "Visualize" in action:
            self.title_label.setText("Visualize Current Automaton")
            content = """
            <h3 style='color:white; margin-top:0;'>Visualize Current Automaton</h3>
            <p>Generate a visual representation of your automaton using Graphviz.</p>
            
            <h4 style='color:#00C2FF;'>Visualization Features</h4>
            <ul style='color:#8A98AC;'>
                <li><span style='color:#D0D7E3;'>States</span> - Represented as circles</li>
                <li><span style='color:#D0D7E3;'>Initial state</span> - Marked with an incoming arrow</li>
                <li><span style='color:#D0D7E3;'>Final states</span> - Shown as double circles</li>
                <li><span style='color:#D0D7E3;'>Transitions</span> - Displayed as labeled arrows between states</li>
            </ul>
            
            <div style='background-color:#1E273D; padding:15px; border-radius:5px; margin-top:20px;'>
                <p style='color:#00C2FF; font-weight:bold; margin-top:0;'>Visualization Options</p>
                <p>Create or load an automaton first to enable visualization.</p>
            </div>
            """
            self.description.setHtml(content)
            
        else:
            self.title_label.setText(action)
            content = f"""
            <h3 style='color:white; margin-top:0;'>{action}</h3>
            <p>This functionality is currently in development.</p>
            
            <div style='background-color:#1E273D; padding:15px; border-radius:5px; margin-top:20px;'>
                <p style='color:#00C2FF; font-weight:bold; margin-top:0;'>Coming Soon</p>
                <p>This feature will be available in the next update.</p>
            </div>
            """
            self.description.setHtml(content)


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


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Finite Automata Manager")
        self.setMinimumSize(1100, 700)
        
        # Set the overall application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0E1525;
            }
        """)
        
        # Create a stacked widget to handle the transition between login and main interface
        self.stacked_widget = QStackedWidget()
        
        # Create the login and main widgets
        self.login_widget = LoginWidget()
        self.main_widget = MainWidget()
        
        # Add widgets to stacked widget
        self.stacked_widget.addWidget(self.login_widget)
        self.stacked_widget.addWidget(self.main_widget)
        
        # Set central widget
        self.setCentralWidget(self.stacked_widget)
        
        # Connect signals
        self.login_widget.login_successful.connect(self.show_main_interface)
    
    def show_main_interface(self):
        # Switch to the main interface
        self.stacked_widget.setCurrentWidget(self.main_widget)


# Placeholder functions for finite automata operations
def create_new_automaton():
    pass

def load_automaton_from_file():
    pass

def save_current_automaton():
    pass

def list_saved_automata():
    pass

def modify_current_automaton():
    pass

def delete_saved_automaton():
    pass

def check_determinism():
    pass

def check_completeness():
    pass

def make_automaton_complete():
    pass

def convert_nfa_to_dfa():
    pass

def check_minimality():
    pass

def minimize_automaton():
    pass

def test_word_acceptance():
    pass

def generate_accepted_words():
    pass

def generate_rejected_words():
    pass

def check_equivalence():
    pass

def compute_union():
    pass

def compute_intersection():
    pass

def compute_complement():
    pass

def visualize_automaton():
    pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Use Fusion style for consistent cross-platform look
    
    # Set dark palette for the entire application
    dark_palette = QPalette()
    dark_palette.setColor(QPalette.ColorRole.Window, QColor(14, 21, 37))
    dark_palette.setColor(QPalette.ColorRole.WindowText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Base, QColor(26, 33, 51))
    dark_palette.setColor(QPalette.ColorRole.AlternateBase, QColor(18, 27, 46))
    dark_palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(26, 33, 51))
    dark_palette.setColor(QPalette.ColorRole.ToolTipText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Text, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.Button, QColor(26, 33, 51))
    dark_palette.setColor(QPalette.ColorRole.ButtonText, Qt.GlobalColor.white)
    dark_palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)
    dark_palette.setColor(QPalette.ColorRole.Link, QColor(0, 194, 255))  # Cyan accent
    dark_palette.setColor(QPalette.ColorRole.Highlight, QColor(123, 66, 246))  # Purple accent
    dark_palette.setColor(QPalette.ColorRole.HighlightedText, Qt.GlobalColor.white)
    
    app.setPalette(dark_palette)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())