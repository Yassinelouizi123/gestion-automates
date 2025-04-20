from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import pyqtSignal
from custom_widgets import MenuCategory,QGraphicsDropShadowEffect, QColor, ModernButton
from PyQt6.QtCore import Qt

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
        menu_container.setObjectName("menu_container")  # Add this line
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
        
        # Base button map
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
        
        # Add admin buttons if they exist
        if hasattr(self, 'user_mgmt_btn'):
            button_map["User Management"] = self.user_mgmt_btn
        
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
        elif button_name == "User Management":
            return "administration"
        else:
            return "other"
    
    def add_admin_menu_items(self):
        # Create admin section
        admin_section = MenuCategory("ADMINISTRATION")
        self.user_mgmt_btn = admin_section.add_menu_item("User Management", 
            action=lambda: self.set_active_button("User Management"))
        
        # Add to menu layout after OTHER section
        menu_layout = self.findChild(QWidget, "menu_container").layout()
        menu_layout.insertWidget(menu_layout.count()-1, admin_section)  # Insert before stretch