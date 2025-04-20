from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QStackedWidget, QTextEdit,
                            QFrame, QGraphicsDropShadowEffect, QGroupBox, QLineEdit,
                            QFormLayout, QHBoxLayout, QTextEdit)
from PyQt6.QtGui import QFont, QColor
from custom_widgets import ModernButton 
from PyQt6.QtCore import Qt


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