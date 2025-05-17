from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QStackedWidget, QTextEdit,
                            QFrame, QGraphicsDropShadowEffect, QGroupBox, QLineEdit,
                            QFormLayout, QHBoxLayout, QTextEdit, QMessageBox, QComboBox,
                            QFileDialog, QInputDialog,QListWidget)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QFont, QColor, QPixmap
from custom_widgets import ModernButton 
from automata_operations import AutomataManager, Visualizer, AutomataAnalyzer
import os


class ContentWidget(QWidget):
    def __init__(self, user_manager=None, current_user=None):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.automata_manager = AutomataManager()
        self.user_manager = user_manager
        self.current_user = current_user
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
        self.create_completeness_check_page()        
        self.create_visualization_page()
        self.create_load_automaton_page()
        self.create_delete_automaton_page()
        self.create_check_equivalence_page()
        self.create_make_complete_page()
        self.create_convert_nfa_to_dfa_page()
        self.create_minimality_check_page()
        self.create_minimize_automaton_page()
        self.create_test_word_acceptance_page()
        self.create_generate_accepted_words_page()
        self.create_generate_rejected_words_page()
        self.create_compute_union_page()
        self.create_compute_intersection_page()
        self.create_compute_complement_page()

        
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
        
        group = QGroupBox("Create New Finite Automaton")
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
        
        # Create form labels with white text
        label_style = "QLabel { color: white; background: transparent; }" 
        name_label = QLabel("Automaton Name:")
        states_label = QLabel("States (Q):")
        alphabet_label = QLabel("Input alphabet (Σ):")
        transitions_label = QLabel("Transition function (δ):")
        initial_state_label = QLabel("Initial state (q₀):")
        final_states_label = QLabel("Final states (F):")
        
        for label in [name_label, states_label, alphabet_label, transitions_label, 
                     initial_state_label, final_states_label]:
            label.setStyleSheet(label_style)
        
        # Automaton Name Input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter automaton name")
        
        # States Input
        self.states_input = QLineEdit()
        self.states_input.setPlaceholderText("Enter states separated by commas (q0, q1, ...)")
        
        # Alphabet Input
        self.alphabet_input = QLineEdit()
        self.alphabet_input.setPlaceholderText("Enter alphabet symbols separated by commas (a, b, ...)")
        
        # Transitions Input
        self.transitions_input = QTextEdit()
        self.transitions_input.setPlaceholderText("Enter transitions in format: q0,a→q1 (one per line)")
        self.transitions_input.setMinimumHeight(100)
        
        # Initial State Input
        self.initial_state = QLineEdit()
        self.initial_state.setPlaceholderText("Enter initial state (e.g., q0)")
        
        # Final States Input
        self.final_states = QLineEdit()
        self.final_states.setPlaceholderText("Enter final states separated by commas (q1, q2, ...)")
        
        # Style all input fields
        input_style = """
            QLineEdit, QTextEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 1px solid #00C2FF;
            }
        """
        
        for widget in [self.name_input, self.states_input, self.alphabet_input, 
                      self.transitions_input, self.initial_state, self.final_states]:
            widget.setStyleSheet(input_style)
        
        # Add all form rows
        form_layout.addRow(name_label, self.name_input)
        form_layout.addRow(states_label, self.states_input)
        form_layout.addRow(alphabet_label, self.alphabet_input)
        form_layout.addRow(transitions_label, self.transitions_input)
        form_layout.addRow(initial_state_label, self.initial_state)
        form_layout.addRow(final_states_label, self.final_states)
        
        # Add buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)  # Add spacing between buttons
        
        self.create_btn = ModernButton("Create and Save Automaton", accent_color="#2ED573")
        self.create_btn.setFixedSize(200, 35)  # Reduce button size
        self.create_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        
        self.clear_btn = ModernButton("Clear Fields", accent_color="#FF4757")
        self.clear_btn.setFixedSize(120, 35)  # Reduce button size
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #FF6B81;
            }
            QPushButton:pressed {
                background-color: #FF4D67;
            }
        """)
        
        button_layout.addStretch(1)  # Add space on the left
        button_layout.addWidget(self.clear_btn)
        button_layout.addWidget(self.create_btn)
        button_layout.addStretch(1)  # Add space on the right
        
        # Connect button signals
        self.create_btn.clicked.connect(self.create_automaton)
        self.clear_btn.clicked.connect(self.clear_automaton_form)
        
        form_layout.addRow(button_layout)
        
        group.setLayout(form_layout)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def create_automaton(self):
        # Get automaton name
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter an automaton name")
            return
        
        # Parse states
        states_text = self.states_input.text().strip()
        if not states_text:
            QMessageBox.warning(self, "Error", "Please enter at least one state")
            return
        states = {s.strip() for s in states_text.split(',')}
        
        # Parse alphabet
        alphabet_text = self.alphabet_input.text().strip()
        if not alphabet_text:
            QMessageBox.warning(self, "Error", "Please enter at least one alphabet symbol")
            return
        alphabet = {s.strip() for s in alphabet_text.split(',')}
        
        # Parse transitions
        transitions = {}
        transitions_text = self.transitions_input.toPlainText().strip()
        if not transitions_text:
            QMessageBox.warning(self, "Error", "Please enter at least one transition")
            return
            
        try:
            for line in transitions_text.split('\n'):
                if not line.strip():
                    continue
                # Parse transition in format "q0,a→q1" or "q0,a->q1"
                source_state, rest = line.split(',', 1)
                symbol, target_state = rest.replace('→', '->').split('->', 1)
                source_state = source_state.strip()
                symbol = symbol.strip()
                target_state = target_state.strip()
                
                if source_state not in states:
                    raise ValueError(f"Invalid source state: {source_state}")
                if symbol not in alphabet:
                    raise ValueError(f"Invalid symbol: {symbol}")
                if target_state not in states:
                    raise ValueError(f"Invalid target state: {target_state}")
                
                # Add to transitions dictionary
                key = (source_state, symbol)
                if key not in transitions:
                    transitions[key] = set()
                transitions[key].add(target_state)
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Invalid transition format: {str(e)}")
            return
        
        # Parse initial state
        initial_state = self.initial_state.text().strip()
        if not initial_state:
            QMessageBox.warning(self, "Error", "Please specify an initial state")
            return
        if initial_state not in states:
            QMessageBox.warning(self, "Error", "Initial state must be one of the defined states")
            return
        
        # Parse final states
        final_states_text = self.final_states.text().strip()
        if not final_states_text:
            QMessageBox.warning(self, "Error", "Please specify at least one final state")
            return
        final_states = {s.strip() for s in final_states_text.split(',')}
        if not final_states.issubset(states):
            QMessageBox.warning(self, "Error", "All final states must be in the set of states")
            return
        
        try:
            # Create the automaton with the specified name
            automaton = self.automata_manager.create_automaton(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=initial_state,
                final_states=final_states,
                name=name
            )
            
            # Save the automaton to a JSON file
            if self.automata_manager.save_automaton(f"{name}.json"):
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Automaton '{name}' has been created and saved to saved_automatas/{name}.json"
                )
                self.clear_automaton_form()
                self.refresh_visualization()  # Add visualization refresh
            else:
                QMessageBox.warning(
                    self, 
                    "Warning", 
                    f"Automaton created but could not be saved to file"
                )
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to create automaton: {str(e)}")
    
    def clear_automaton_form(self):
        """Clear all input fields in the automaton creation form"""
        self.name_input.clear()
        self.states_input.clear()
        self.alphabet_input.clear()
        self.transitions_input.clear()
        self.initial_state.clear()
        self.final_states.clear()

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
        
        self.check_btn = ModernButton("Check Determinism", accent_color="#7B42F6")
        self.check_btn.setFixedWidth(200)
        self.check_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.check_btn.clicked.connect(self.check_determinism_status)
        
        content.addWidget(self.check_result)
        content.addWidget(self.check_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def update_determinism_status(self):
        if self.automata_manager.current_automaton:
            self.check_result.setText("Automaton loaded. Status: Ready.")
        else:
            self.check_result.setText("No automaton loaded. Please create or load an automaton first.")

    def check_determinism_status(self):
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.check_result.setText("No automaton loaded. Please create or load an automaton first.")
            return
        # Build a detailed result message
        summary = f"""
        <div style='color: white;'>
            <h3 style='color:#00C2FF; margin-top:0;'>Determinism Check Result</h3>
            <p><b>Automaton:</b> {automaton.name}</p>
            <p><b>States:</b> {len(automaton.states)} &nbsp; <b>Alphabet Size:</b> {len(automaton.alphabet)}</p>
            <p><b>Criteria for DFA:</b></p>
            <ul style='color:#8A98AC;'>
                <li>Exactly <b>one initial state</b></li>
                <li>For every state and symbol, <b>exactly one transition</b></li>
                <li><b>No ε-transitions</b> (empty string transitions)</li>
            </ul>
        """
        # Check determinism and find first issue if any
        is_dfa = True
        first_issue = None
        for state in automaton.states:
            for symbol in automaton.alphabet:
                targets = automaton.transitions.get((state, symbol), set())
                if len(targets) != 1:
                    is_dfa = False
                    first_issue = (state, symbol, targets)
                    break
            if not is_dfa:
                break
        if is_dfa:
            summary += """
            <div style='margin-top:15px; color:#2ED573; font-size:16px;'><b>✅ The loaded automaton is <u>Deterministic (DFA)</u>.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>All states and symbols have exactly one transition. The automaton meets all DFA criteria.</p>
            """
        else:
            state, symbol, targets = first_issue
            summary += f"""
            <div style='margin-top:15px; color:#FF4757; font-size:16px;'><b>❌ The loaded automaton is <u>Non-Deterministic (NFA)</u>.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>
                <b>First issue found:</b><br>
                State <b>{state}</b> with symbol <b>{symbol}</b> has {len(targets)} transition(s):
                <span style='color:white;'>{{{', '.join(sorted(targets))}}}</span>.<br>
                Each state-symbol pair must have exactly one target state for a DFA.
            </p>
            """
        summary += "</div>"
        self.check_result.setText(summary)

    def create_completeness_check_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Completeness Check")
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

        self.completeness_result = QLabel()
        self.completeness_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.completeness_result.setText("No automaton loaded. Please create or load an automaton first.")

        self.completeness_btn = ModernButton("Check Completeness", accent_color="#00C2FF")
        self.completeness_btn.setFixedWidth(200)
        self.completeness_btn.setStyleSheet("""
            QPushButton {
                background-color: #00C2FF;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #0099CC;
            }
            QPushButton:pressed {
                background-color: #0077AA;
            }
        """)
        self.completeness_btn.clicked.connect(self.check_completeness_status)

        content.addWidget(self.completeness_result)
        content.addWidget(self.completeness_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)

        layout.addWidget(group)
        self.stacked_widget.addWidget(page)

    def update_completeness_status(self):
        if self.automata_manager.current_automaton:
            self.completeness_result.setText("Automaton loaded. Status: Ready.")
        else:
            self.completeness_result.setText("No automaton loaded. Please create or load an automaton first.")

    def check_completeness_status(self):
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.completeness_result.setText("No automaton loaded. Please create or load an automaton first.")
            return
        # Build a detailed result message
        summary = f"""
        <div style='color: white;'>
            <h3 style='color:#00C2FF; margin-top:0;'>Completeness Check Result</h3>
            <p><b>Automaton:</b> {automaton.name}</p>
            <p><b>States:</b> {len(automaton.states)} &nbsp; <b>Alphabet Size:</b> {len(automaton.alphabet)}</p>
            <p><b>Criteria for Complete Automaton:</b></p>
            <ul style='color:#8A98AC;'>
                <li>For every state and every symbol, there is at least one transition defined</li>
            </ul>
        """
        is_complete = True
        first_missing = None
        for state in automaton.states:
            for symbol in automaton.alphabet:
                if not automaton.transitions.get((state, symbol)):
                    is_complete = False
                    first_missing = (state, symbol)
                    break
            if not is_complete:
                break
        if is_complete:
            summary += """
            <div style='
            <p style='color:#8A98AC; margin-top:10px;'>All states and symbols have at least one transition defined. The automaton is complete.</p>
            """
        else:
            state, symbol = first_missing
            summary += f"""
            <div style='margin-top:15px; color:#FF4757; font-size:16px;'><b>❌ The loaded automaton is <u>Incomplete</u>.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>
                <b>First missing transition:</b><br>
                State <b>{state}</b> with symbol <b>{symbol}</b> has <span style='color:white;'>no transition defined</span>.<br>
                Every state-symbol pair must have at least one transition for completeness.
            </p>
            """
        summary += "</div>"
        self.completeness_result.setText(summary)

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
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)
        content.setSpacing(15)
        
        # Info box at the top
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)
        
        info_title = QLabel("ℹ️ Automaton Visualization")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)
        
        info_text = QLabel(
            "This page shows a graphical representation of your automaton. "
            "The visualization updates automatically when you load or modify an automaton."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)
        
        # Visualization area
        self.visualization_area = QWebEngineView()
        self.visualization_area.setMinimumSize(550, 400)
        self.visualization_area.setMaximumSize(16777215, 16777215)  # Allow it to grow if needed
        self.visualization_area.setStyleSheet("""
            QWebEngineView {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.visualization_area.setUrl(QUrl("about:blank"))
        
        # Button area
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Zoom Out button
        self.zoom_out_btn = ModernButton("+", accent_color="#8A98AC")
        self.zoom_out_btn.setFixedSize(35, 35)
        self.zoom_out_btn.setStyleSheet("""
            QPushButton {
                background-color: #8A98AC;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6C7A89;
            }
        """)
        self.zoom_out_btn.clicked.connect(lambda: self.set_graph_zoom(-0.1))
        
        # Zoom In button
        self.zoom_in_btn = ModernButton("-", accent_color="#8A98AC")
        self.zoom_in_btn.setFixedSize(35, 35)
        self.zoom_in_btn.setStyleSheet("""
            QPushButton {
                background-color: #8A98AC;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #6C7A89;
            }
        """)
        self.zoom_in_btn.clicked.connect(lambda: self.set_graph_zoom(0.1))
        
        self.refresh_btn = ModernButton("Refresh View", accent_color="#2ED573")
        self.refresh_btn.setFixedSize(120, 35)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        self.refresh_btn.clicked.connect(self.refresh_visualization)
        
        self.export_btn = ModernButton("Export as PNG", accent_color="#7B42F6")
        self.export_btn.setFixedSize(120, 35)
        self.export_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.export_btn.clicked.connect(self.export_visualization)
        
        # Add buttons to layout
        button_layout.addWidget(self.zoom_out_btn)
        button_layout.addSpacing(5)
        button_layout.addWidget(self.zoom_in_btn)
        button_layout.addSpacing(20)
        button_layout.addWidget(self.refresh_btn)
        button_layout.addSpacing(10)
        button_layout.addWidget(self.export_btn)
        
        # Add everything to the main layout
        content.addWidget(self.visualization_area)
        content.addLayout(button_layout)
        group.setLayout(content)
        
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        
    def set_graph_zoom(self, delta):
        current_zoom = self.visualization_area.zoomFactor()
        new_zoom = max(0.2, min(3.0, current_zoom + delta))  # Clamp between 0.2x and 3x
        self.visualization_area.setZoomFactor(new_zoom)

    def refresh_visualization(self):
        """Update the automaton visualization"""
        if not self.automata_manager.current_automaton:
            error_html = """
                <div style='display: flex; justify-content: center; align-items: center; height: 100%; color: #8A98AC; text-align: center; background: #fff;'>
                    <div>
                        <h3 style='color: #00C2FF;'>No Automaton Loaded</h3>
                        <p>Create a new automaton or load an existing one to see its visualization.</p>
                    </div>
                </div>
            """
            self.visualization_area.setHtml(error_html)
            self.export_btn.setEnabled(False)
            return
            
        try:
            # Get SVG content
            svg_content = Visualizer.get_svg_content(self.automata_manager.current_automaton)
            
            # Wrap SVG in HTML with proper styling
            html_content = f"""
                <html>
                <head>
                    <style>
                        body {{ 
                            margin: 0;
                            padding: 20px;
                            display: flex;
                            justify-content: flex-start;
                            /* Removed align-items: center to pull SVG to top */
                            background-color: #fff;
                        }}
                        svg {{
                            width: 100%;
                            height: 100%;
                            max-width: 850px;
                            max-height: 400px;
                            display: block;
                            margin-left: 140px; /* Pull SVG a bit to the left */
                            margin-right: 150px;
                            margin-top: 0px;      /* Add space above the SVG */
                            margin-bottom: 150px;
                        }}
                    </style>
                </head>
                <body>
                    {svg_content}
                </body>
                </html>
            """
            
            # Display the wrapped SVG content
            self.visualization_area.setHtml(html_content)
            self.export_btn.setEnabled(True)
        except Exception as e:
            error_message = str(e)
            if "graphviz" in error_message.lower():
                error_html = f"""
                    <div style='display: flex; justify-content: center; align-items: center; height: 100%; color: #FF4757; text-align: center; background: #fff;'>
                        <div>
                            <h3>Graphviz Error</h3>
                            <p>Please make sure Graphviz is installed on your system.</p>
                            <p>You can install it from: <a href='https://graphviz.org/download/' style='color: #00C2FF;'>https://graphviz.org/download/</a></p>
                            <p style='color: #8A98AC; font-size: 12px;'>Error details: {error_message}</p>
                        </div>
                    </div>
                """
            else:
                error_html = f"""
                    <div style='display: flex; justify-content: center; align-items: center; height: 100%; color: #FF4757; text-align: center; background: #fff;'>
                        <div>
                            <h3>Visualization Error</h3>
                            <p>An error occurred while generating the visualization.</p>
                            <p style='color: #8A98AC; font-size: 12px;'>Error details: {error_message}</p>
                        </div>
                    </div>
                """
            self.visualization_area.setHtml(error_html)
            self.export_btn.setEnabled(False)
    
    def export_visualization(self):
        """Export the current visualization as a PNG file"""
        if not self.automata_manager.current_automaton:
            QMessageBox.warning(self, "Error", "No automaton loaded to export")
            return
            
        try:
            # Get default filename
            default_name = f"automaton_{self.automata_manager.current_automaton.name}"
            
            # Get save location from user
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Visualization",
                default_name,
                "PNG Files (*.png)"
            )
            
            if file_path:
                # Ensure .png extension
                if not file_path.lower().endswith('.png'):
                    file_path += '.png'
                    
                # Render the automaton
                rendered_path = Visualizer.render_automaton(
                    self.automata_manager.current_automaton,
                    output_path=file_path[:-4],  # Remove .png extension
                    format='png'
                )
                
                QMessageBox.information(
                    self,
                    "Success",
                    f"Visualization exported successfully to:\n{rendered_path}"
                )
        except Exception as e:
            QMessageBox.warning(
                self,
                "Error",
                f"Failed to export visualization: {str(e)}"
            )

    def create_load_automaton_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        group = QGroupBox("Load Automaton from File")
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
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)
        
        # File selection area
        file_group = QGroupBox("Select Automaton File")
        file_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        file_layout = QVBoxLayout()
        
        # Combo box for saved automata
        self.automata_files_combo = QComboBox()
        self.automata_files_combo.setStyleSheet("""
            QComboBox {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 200px;
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
        self.refresh_automata_list()
        
        # Load button
        load_btn = ModernButton("Load Selected Automaton", accent_color="#7B42F6")
        load_btn.setFixedSize(200, 35)
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        load_btn.clicked.connect(self.load_selected_automaton)
        
        # Refresh button
        refresh_btn = ModernButton("Refresh File List", accent_color="#2ED573")
        refresh_btn.setFixedSize(150, 35)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_automata_list)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(load_btn)
        button_layout.addStretch(1)
        
        # Create label with transparent background
        available_label = QLabel("Available Automata:")
        available_label.setStyleSheet("QLabel { color: white; background: transparent; }")
        
        file_layout.addWidget(available_label)
        file_layout.addWidget(self.automata_files_combo)
        file_layout.addLayout(button_layout)
        file_group.setLayout(file_layout)
        
        # Current automaton display area
        current_group = QGroupBox("Currently Loaded Automaton")
        current_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        current_layout = QVBoxLayout()
        
        # Add text display for current automaton details
        self.current_automaton_display = QTextEdit()
        self.current_automaton_display.setReadOnly(True)
        self.current_automaton_display.setStyleSheet("""
            QTextEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 10px;
                color: white;
                font-family: monospace;
            }
        """)
        self.current_automaton_display.setMinimumHeight(200)
        
        # Add Edit button
        self.edit_automaton_btn = ModernButton("Edit Current Automaton", accent_color="#7B42F6")
        self.edit_automaton_btn.setFixedSize(200, 35)
        self.edit_automaton_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
            QPushButton:disabled {
                background-color: #2A3344;
                color: #8A98AC;
            }
        """)
        self.edit_automaton_btn.clicked.connect(self.edit_loaded_automaton)
        self.edit_automaton_btn.setEnabled(False)  # Initially disabled
        
        current_layout.addWidget(self.current_automaton_display)
        current_layout.addWidget(self.edit_automaton_btn, 0, Qt.AlignmentFlag.AlignCenter)
        current_group.setLayout(current_layout)
        
        content_layout.addWidget(file_group)
        content_layout.addWidget(current_group)
        
        group.setLayout(content_layout)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
    
    def refresh_automata_list(self):
        """Refresh the list of available automata files"""
        self.automata_files_combo.clear()
        automata_files = self.automata_manager.list_saved_automata()
        self.automata_files_combo.addItems(automata_files)
    
    def load_selected_automaton(self):
        selected_file = self.automata_files_combo.currentText()
        if not selected_file:
            QMessageBox.warning(self, "Error", "Please select an automaton file to load")
            return
        try:
            self.automata_manager.load_automaton(selected_file)
            self.update_current_automaton_display()
            self.edit_automaton_btn.setEnabled(True)
            self.refresh_visualization()
            self.update_determinism_status()
            self.update_completeness_status()
            self.update_make_complete_status()
            self.update_nfa_to_dfa_status()
            self.update_minimality_status()
            self.update_minimize_status()  # <-- Add this line
            QMessageBox.information(self, "Success", f"Successfully loaded automaton from {selected_file}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load automaton: {str(e)}")
            self.edit_automaton_btn.setEnabled(False)
            self.update_determinism_status()
            self.update_completeness_status()
            self.update_make_complete_status()
            self.update_nfa_to_dfa_status()
            self.update_minimality_status()
            self.update_minimize_status()  # <-- Add this line
    
    def edit_loaded_automaton(self):
        """Open the loaded automaton in the creation page for editing"""
        if not self.automata_manager.current_automaton:
            QMessageBox.warning(self, "Error", "No automaton currently loaded")
            return
            
        # Fill the creation form with current automaton data
        automaton = self.automata_manager.current_automaton
        self.name_input.setText(automaton.name)
        self.states_input.setText(", ".join(sorted(automaton.states)))
        self.alphabet_input.setText(", ".join(sorted(automaton.alphabet)))
        
        # Format transitions
        transitions_text = []
        for (state, symbol), targets in sorted(automaton.transitions.items()):
            for target in sorted(targets):
                transitions_text.append(f"{state},{symbol}→{target}")
        self.transitions_input.setPlainText("\n".join(transitions_text))
        
        self.initial_state.setText(automaton.initial_state)
        self.final_states.setText(", ".join(sorted(automaton.final_states)))
        
        # Switch to creation page for editing
        self.stacked_widget.setCurrentIndex(1)  # Index 1 is the creation page
        self.title_label.setText("Edit Automaton")
        
        # Show information message
        QMessageBox.information(
            self,
            "Edit Mode",
            f"Now editing automaton '{automaton.name}'. Make your changes and click 'Create and Save' to update the automaton."
        )
    
    def update_current_automaton_display(self):
        """Update the display of the currently loaded automaton"""
        if not self.automata_manager.current_automaton:
            self.current_automaton_display.setHtml("""
                <div style='color: #8A98AC;'>
                    No automaton currently loaded.<br>
                    Select a file above and click "Load Selected Automaton" to load one.
                </div>
            """)
            return
            
        automaton = self.automata_manager.current_automaton
        display_text = f"""
            <div style='color: white;'>
                <h3 style='color: #00C2FF;'>{automaton.name}</h3>
                <p><b>States (Q):</b> {', '.join(sorted(automaton.states))}</p>
                <p><b>Alphabet (Σ):</b> {', '.join(sorted(automaton.alphabet))}</p>
                <p><b>Initial State (q₀):</b> {automaton.initial_state}</p>
                <p><b>Final States (F):</b> {', '.join(sorted(automaton.final_states))}</p>
                <p><b>Transitions (δ):</b></p>
                <ul>
        """
        
        # Add transitions in a sorted, readable format
        transitions = []
        for (state, symbol), targets in automaton.transitions.items():
            targets_str = ', '.join(sorted(targets))
            transitions.append(f"    <li>δ({state}, {symbol}) → {{{targets_str}}}</li>")
        
        display_text += '\n'.join(sorted(transitions))
        display_text += """
                </ul>
            </div>
        """
        
        self.current_automaton_display.setHtml(display_text)

    def create_delete_automaton_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        group = QGroupBox("Delete Saved Automaton File")
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
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(20)

        # Info box
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)
        
        info_title = QLabel("ℹ️ Delete Automaton")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)
        
        info_text = QLabel(
            "Deleting an automaton will permanently remove it from the saved files. "
            "This action cannot be undone."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content_layout.addWidget(info_box)

        # File selection area
        file_group = QGroupBox("Select Automaton to Delete")
        file_group.setStyleSheet("""
            QGroupBox {
                color: white;
                font-weight: bold;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        file_layout = QVBoxLayout()

        # Search box
        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setStyleSheet("QLabel { color: white; background: transparent; }")
        
        self.delete_search_input = QLineEdit()
        self.delete_search_input.setPlaceholderText("Search automata by name...")
        self.delete_search_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 200px;
            }
            QLineEdit:focus {
                border: 1px solid #00C2FF;
            }
        """)
        self.delete_search_input.textChanged.connect(self.filter_delete_automata_list)
        
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.delete_search_input)
        search_layout.addStretch()
        
        # File count label
        self.file_count_label = QLabel()
        self.file_count_label.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
                font-size: 12px;
            }
        """)
        
        # Combo box for automata selection
        select_file_label = QLabel("Select a file to delete:")
        select_file_label.setStyleSheet("QLabel { color: white; background: transparent; }")
        
        self.delete_automata_combo = QComboBox()
        self.delete_automata_combo.setStyleSheet("""
            QComboBox {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 200px;
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

        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_btn = ModernButton("Refresh List", accent_color="#2ED573")
        refresh_btn.setFixedSize(120, 35)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_delete_automata_list)
        
        delete_btn = ModernButton("Delete Selected Automaton", accent_color="#FF4757")
        delete_btn.setFixedSize(200, 35)
        delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #FF6B81;
            }
            QPushButton:pressed {
                background-color: #FF4D67;
            }
        """)
        delete_btn.clicked.connect(self.delete_selected_automaton)
        
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(delete_btn)
        button_layout.addStretch()

        # Status label
        self.delete_status_label = QLabel()
        self.delete_status_label.setStyleSheet("color: #8A98AC; background: transparent; font-size: 13px;")

        # Add all widgets to file layout
        file_layout.addLayout(search_layout)
        file_layout.addWidget(self.file_count_label)
        file_layout.addWidget(select_file_label)
        file_layout.addWidget(self.delete_automata_combo)
        file_layout.addLayout(button_layout)
        file_layout.addWidget(self.delete_status_label)
        
        file_group.setLayout(file_layout)
        content_layout.addWidget(file_group)
        
        group.setLayout(content_layout)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        
        # Initialize the list
        self.refresh_delete_automata_list()
    def refresh_delete_automata_list(self):
        self.delete_automata_combo.clear()
        automata_files = self.automata_manager.list_saved_automata()
        self.delete_automata_combo.addItems(automata_files)
        self.update_file_count_label()
    
    def filter_delete_automata_list(self):
        search_text = self.delete_search_input.text().strip().lower()
        automata_files = self.automata_manager.list_saved_automata()
        filtered_files = [f for f in automata_files if search_text in f.lower()]
        self.delete_automata_combo.clear()
        self.delete_automata_combo.addItems(filtered_files)
        self.update_file_count_label()
    
    def update_file_count_label(self):
        count = self.delete_automata_combo.count()
        self.file_count_label.setText(f"Total files: {count}")
    
    def delete_selected_automaton(self):
        selected_file = self.delete_automata_combo.currentText()
        if not selected_file:
            self.delete_status_label.setText("Please select a file to delete.")
            return

        # Check if user is admin
        if not self.current_user or self.current_user['role'] != 'admin':
            self.delete_status_label.setText("Only administrators can delete automata. Please contact an admin for assistance.")
            QMessageBox.warning(
                self,
                "Permission Denied",
                "You do not have permission to delete automata.\nThis action requires administrator privileges.\nPlease contact an administrator for assistance."
            )
            return
            
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete '{selected_file}'? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            self.delete_status_label.setText("Deletion cancelled.")
            return
            
        success = self.automata_manager.delete_automaton(selected_file)
        if success:
            self.delete_status_label.setText(f"Deleted '{selected_file}'.")
            self.refresh_delete_automata_list()
        else:
            self.delete_status_label.setText(f"Failed to delete '{selected_file}'.")

    def create_make_complete_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Make Automaton Complete")
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

        self.make_complete_result = QLabel()
        self.make_complete_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.make_complete_result.setText("No automaton loaded. Please create or load an automaton first.")        
        self.make_complete_btn = ModernButton("Make Automaton Complete", accent_color="#7B42F6")
        self.make_complete_btn.setFixedWidth(220)
        self.make_complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.make_complete_btn.clicked.connect(self.make_automaton_complete)

        # Save button (appears after making complete)
        self.save_complete_btn = ModernButton("Save Completed Automaton", accent_color="#2ED573")
        self.save_complete_btn.setFixedWidth(220)
        self.save_complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        self.save_complete_btn.clicked.connect(self.save_completed_automaton)
        self.save_complete_btn.setVisible(False)

        content.addWidget(self.make_complete_result)
        content.addWidget(self.make_complete_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.save_complete_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)

        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        # Store index for navigation
        self.make_complete_page_index = self.stacked_widget.count() - 1
        self.completed_automaton = None  # To store the new automaton

    def update_make_complete_status(self):
        from automata_operations import AutomataAnalyzer
        automaton = self.automata_manager.current_automaton
        if automaton:
            is_complete = AutomataAnalyzer.is_complete(automaton)
            if is_complete:
                self.make_complete_result.setText("""
                    <div style='color:#2ED573; font-size:15px;'>
                        <b>The automaton is already <u>complete</u>. No need to perform this operation.</b>
                    </div>
                """)
                self.make_complete_btn.setEnabled(False)
                self.save_complete_btn.setVisible(False)
            else:
                self.make_complete_result.setText("Automaton loaded. Status: Ready.")
                self.make_complete_btn.setEnabled(True)
                self.save_complete_btn.setVisible(False)
        else:
            self.make_complete_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.make_complete_btn.setEnabled(False)
            self.save_complete_btn.setVisible(False)

    def make_automaton_complete(self):
        from automata_operations import AutomataAnalyzer
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.make_complete_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.save_complete_btn.setVisible(False)
            return
        # Check if already complete
        if AutomataAnalyzer.is_complete(automaton):
            self.make_complete_result.setText("<span style='color:#2ED573;'>The automaton is already complete. No changes needed.</span>")
            self.save_complete_btn.setVisible(False)
            self.make_complete_btn.setEnabled(False)
            return
        # ...existing code for making complete...
        try:
            completed = AutomataAnalyzer.make_complete(automaton)
            self.completed_automaton = completed
            # Find what was changed
            added_trap = set(completed.states) - set(automaton.states)
            trap_state = next(iter(added_trap)) if added_trap else None
            filled = []
            for state in completed.states:
                for symbol in completed.alphabet:
                    orig_targets = automaton.transitions.get((state, symbol), set())
                    comp_targets = completed.transitions.get((state, symbol), set())
                    if not orig_targets and comp_targets:
                        filled.append((state, symbol, comp_targets))
            summary = f"""
            <div style='color: white;'>
                <h3 style='color:#00C2FF; margin-top:0;'>Make Automaton Complete</h3>
                <p><b>Automaton:</b> {automaton.name}</p>
                <p><b>States:</b> {len(automaton.states)} → {len(completed.states)} &nbsp; <b>Alphabet Size:</b> {len(completed.alphabet)}</p>
                <p><b>Trap state added:</b> {trap_state if trap_state else 'None (already complete)'}</p>
                <p><b>Filled transitions:</b> {len(filled)}</p>
            """
            if filled:
                summary += "<ul style='color:#8A98AC;'>"
                for i, (state, symbol, targets) in enumerate(filled[:5]):
                    summary += f"<li>δ({state}, {symbol}) → {{{', '.join(sorted(targets))}}}</li>"
                if len(filled) > 5:
                    summary += f"<li>...and {len(filled)-5} more</li>"
                summary += "</ul>"
            summary += """
                <div style='margin-top:15px; color:#2ED573; font-size:16px;'><b>✅ Completed automaton is ready. Click 'Save Completed Automaton' to save it.</b></div>
            </div>
            """
            self.make_complete_result.setText(summary)
            self.save_complete_btn.setVisible(True)
        except Exception as e:
            self.make_complete_result.setText(f"<span style='color:#FF4757;'>Error: {str(e)}</span>")
            self.save_complete_btn.setVisible(False)

    def save_completed_automaton(self):
        if not self.completed_automaton:
            QMessageBox.warning(self, "Error", "No completed automaton to save.")
            return
        orig_name = self.completed_automaton.name
        if orig_name.endswith("_complete"):
            default_name = orig_name + ".json"
        else:
            default_name = orig_name + "_complete.json"
        name, ok = QInputDialog.getText(self, "Save Completed Automaton", "Enter name for the completed automaton:", QLineEdit.EchoMode.Normal, default_name)
        if not ok or not name.strip():
            return
        base_name = name.strip()
        if base_name.lower().endswith('.json'):
            base_name = base_name[:-5]
        self.completed_automaton.name = base_name
        # Save by temporarily setting as current_automaton
        original = self.automata_manager.current_automaton
        self.automata_manager.current_automaton = self.completed_automaton
        try:
            success = self.automata_manager.save_automaton(f"{base_name}.json")
            if success:
                QMessageBox.information(self, "Success", f"Completed automaton saved as saved_automatas/{base_name}.json")
                self.save_complete_btn.setVisible(False)
                self.refresh_automata_list()
            else:
                QMessageBox.warning(self, "Error", f"Failed to save completed automaton: Unknown error.")
                self.save_complete_btn.setVisible(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save completed automaton: {str(e)}")
            self.save_complete_btn.setVisible(True)
        finally:
            self.automata_manager.current_automaton = original

    def create_convert_nfa_to_dfa_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Convert NFA to DFA")
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

        self.nfa_to_dfa_result = QLabel()
        self.nfa_to_dfa_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.nfa_to_dfa_result.setText("No automaton loaded. Please create or load an automaton first.")

        self.nfa_to_dfa_btn = ModernButton("Convert NFA to DFA", accent_color="#7B42F6")
        self.nfa_to_dfa_btn.setFixedWidth(220)
        self.nfa_to_dfa_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.nfa_to_dfa_btn.clicked.connect(self.convert_nfa_to_dfa)

        self.save_dfa_btn = ModernButton("Save DFA", accent_color="#2ED573")
        self.save_dfa_btn.setFixedWidth(220)
        self.save_dfa_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
        """)
        self.save_dfa_btn.clicked.connect(self.save_dfa_automaton)
        self.save_dfa_btn.setVisible(False)

        content.addWidget(self.nfa_to_dfa_result)
        content.addWidget(self.nfa_to_dfa_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.save_dfa_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)

        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.nfa_to_dfa_page_index = self.stacked_widget.count() - 1
        self.dfa_automaton = None

    def update_nfa_to_dfa_status(self):
        from automata_operations import AutomataAnalyzer
        automaton = self.automata_manager.current_automaton
        if automaton:
            if AutomataAnalyzer.is_deterministic(automaton):
                self.nfa_to_dfa_result.setText(
                    """
                    <div style='color:#2ED573; font-size:15px;'>
                        <b>The automaton is already <u>deterministic (DFA)</u>. No conversion needed.</b>
                    </div>
                    """
                )
                self.nfa_to_dfa_btn.setEnabled(False)
                self.save_dfa_btn.setVisible(False)
            else:
                self.nfa_to_dfa_result.setText("Automaton loaded. Status: Ready.")
                self.nfa_to_dfa_btn.setEnabled(True)
                self.save_dfa_btn.setVisible(False)
        else:
            self.nfa_to_dfa_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.nfa_to_dfa_btn.setEnabled(False)
            self.save_dfa_btn.setVisible(False)

    def convert_nfa_to_dfa(self):
        from automata_operations import AutomataAnalyzer
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.nfa_to_dfa_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.save_dfa_btn.setVisible(False)
            return
        try:
            dfa = AutomataAnalyzer.nfa_to_dfa(automaton)
            self.dfa_automaton = dfa
            summary = f"""
            <div style='color: white;'>
                <h3 style='color:#7B42F6; margin-top:0;'>NFA to DFA Conversion Result</h3>
                <p><b>Original Automaton:</b> {automaton.name}</p>
                <p><b>DFA States:</b> {len(dfa.states)} &nbsp; <b>Alphabet Size:</b> {len(dfa.alphabet)}</p>
                <p><b>Initial State:</b> {dfa.initial_state}</p>
                <p><b>Final States:</b> {len(dfa.final_states)}</p>
                <p><b>Transitions:</b> {len(dfa.transitions)}</p>
                <div style='margin-top:15px; color:#2ED573; font-size:16px;'><b>✅ DFA is ready. Click 'Save DFA' to save it.</b></div>
            </div>
            """
            self.nfa_to_dfa_result.setText(summary)
            self.save_dfa_btn.setVisible(True)
        except Exception as e:
            self.nfa_to_dfa_result.setText(f"<span style='color:#FF4757;'>Error: {str(e)}</span>")
            self.save_dfa_btn.setVisible(False)

    def save_dfa_automaton(self):
        if not self.dfa_automaton:
            QMessageBox.warning(self, "Error", "No DFA to save.")
            return
        name, ok = QInputDialog.getText(self, "Save DFA", "Enter name for the DFA:", QLineEdit.EchoMode.Normal, self.dfa_automaton.name)
        if not ok or not name.strip():
            return
        base_name = name.strip()
        if base_name.lower().endswith('.json'):
            base_name = base_name[:-5]
        self.dfa_automaton.name = base_name
        original = self.automata_manager.current_automaton
        self.automata_manager.current_automaton = self.dfa_automaton
        try:
            success = self.automata_manager.save_automaton(f"{base_name}.json")
            if success:
                QMessageBox.information(self, "Success", f"DFA saved as saved_automatas/{base_name}.json")
                self.save_dfa_btn.setVisible(False)
                self.refresh_automata_list()
            else:
                QMessageBox.warning(self, "Error", f"Failed to save DFA: Unknown error.")
                self.save_dfa_btn.setVisible(True)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save DFA: {str(e)}")
            self.save_dfa_btn.setVisible(True)
        finally:
            self.automata_manager.current_automaton = original

    def create_minimality_check_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Minimality Check")
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

        self.minimality_result = QLabel()
        self.minimality_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.minimality_result.setText("No automaton loaded. Please create or load an automaton first.")

        self.minimality_btn = ModernButton("Check Minimality", accent_color="#FFB300")
        self.minimality_btn.setFixedWidth(200)
        self.minimality_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFB300;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #E09E00;
            }
            QPushButton:pressed {
                background-color: #B37C00;
            }
        """)
        self.minimality_btn.clicked.connect(self.check_minimality_status)

        content.addWidget(self.minimality_result)
        content.addWidget(self.minimality_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)

        layout.addWidget(group)
        self.stacked_widget.addWidget(page)      
    def update_minimality_status(self):
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.minimality_result.setText("No automaton loaded. Please create or load an automaton first.")
            return
            
        # If we haven't done a check yet, show the initial state
        if not hasattr(self, '_last_minimality_check'):
            from automata_operations import AutomataAnalyzer
            is_dfa = AutomataAnalyzer.is_deterministic(automaton)
            if not is_dfa:
                self.minimality_result.setText("""
                    <div style='color:#FF4757; font-size:15px;'>
                        <b>The automaton is not a DFA. Minimality check requires a DFA.</b>
                    </div>
                """)
            else:
                self.minimality_result.setText("Automaton loaded. Status: Ready.")
        else:
            # Restore the last check result if we have one
            self.minimality_result.setText(self._last_minimality_check)

    def check_minimality_status(self):        
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.minimality_result.setText("No automaton loaded. Please create or load an automaton first.")
            return
            
        # Store check result in QLabel to persist between page switches
        from automata_operations import AutomataAnalyzer
        summary = f"""
        <div style='color: white;'>
            <h3 style='color:#FFB300; margin-top:0;'>Minimality Check Result</h3>
            <p><b>Automaton:</b> {automaton.name}</p>
            <p><b>States:</b> {len(automaton.states)} &nbsp; <b>Alphabet Size:</b> {len(automaton.alphabet)}</p>
            <p><b>Criteria for Minimal DFA:</b></p>
            <ul style='color:#8A98AC;'>
                <li>Deterministic and complete</li>
                <li>No two distinct states are equivalent (cannot be merged)</li>
            </ul>
        """
        is_dfa = AutomataAnalyzer.is_deterministic(automaton)
        if not is_dfa:
            summary += """
            <div style='margin-top:15px; color:#FF4757; font-size:16px;'><b>❌ The loaded automaton is not a DFA.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>Minimality check only applies to deterministic finite automata (DFA).</p>
            """
            self.minimality_result.setText(summary)
            return
        is_minimal, partition = AutomataAnalyzer.is_minimal_dfa(automaton)
        if is_minimal:
            summary += """
            <div style='margin-top:15px; color:#2ED573; font-size:16px;'><b>✅ The loaded DFA is <u>Minimal</u>.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>No two states are equivalent. The DFA is already minimal.</p>
            """
        else:
            summary += """
            <div style='margin-top:15px; color:#FF4757; font-size:16px;'><b>❌ The loaded DFA is <u>Not Minimal</u>.</b></div>
            <p style='color:#8A98AC; margin-top:10px;'>
                <b>Some states are equivalent and can be merged. The DFA can be minimized further.</b>
            </p>
            """
        # Show partition info
        if partition:
            summary += "<p style='color:#8A98AC; margin-top:10px;'><b>State Partition:</b></p><ul>"
            for group in sorted(partition, key=lambda g: sorted(g)):
                summary += f"<li>{{{', '.join(sorted(group))}}}</li>"
            summary += "</ul>"        
            summary += "</div>"
        # Store the check result and update the display
        self._last_minimality_check = summary
        self.minimality_result.setText(summary)

    def create_minimize_automaton_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Minimize Automaton (DFA)")
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

        self.minimize_result = QLabel()
        self.minimize_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 100px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.minimize_result.setText("No automaton loaded. Please create or load an automaton first.")

        self.minimize_btn = ModernButton("Minimize DFA", accent_color="#FF4757")
        self.minimize_btn.setFixedWidth(200)
        self.minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #FF6B81;
            }
            QPushButton:pressed {
                background-color: #FF4D67;
            }
        """)
        self.minimize_btn.clicked.connect(self.minimize_automaton)

        self.save_minimized_btn = ModernButton("Save Minimized DFA", accent_color="#2ED573")
        self.save_minimized_btn.setFixedWidth(220)
        self.save_minimized_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
            QPushButton:disabled {
                background-color: #1A2133;
                color: #8A98AC;
            }
        """)
        self.save_minimized_btn.clicked.connect(self.save_minimized_automaton)
        self.save_minimized_btn.setVisible(False)

        content.addWidget(self.minimize_result)
        content.addWidget(self.minimize_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.save_minimized_btn, 0, Qt.AlignmentFlag.AlignCenter)
        group.setLayout(content)

        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.minimize_page_index = self.stacked_widget.count() - 1
        self.minimized_automaton = None

    def update_minimize_status(self):
        if self.automata_manager.current_automaton:
            self.minimize_result.setText("Automaton loaded. Status: Ready.")
            self.save_minimized_btn.setVisible(False)
        else:
            self.minimize_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.save_minimized_btn.setVisible(False)

    def minimize_automaton(self):
        from automata_operations import AutomataAnalyzer
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.minimize_result.setText("No automaton loaded. Please create or load an automaton first.")
            self.save_minimized_btn.setVisible(False)
            return
        if not AutomataAnalyzer.is_deterministic(automaton):
            self.minimize_result.setText("""
                <div style='color:#FF4757; font-size:15px;'>
                    <b>The automaton is not deterministic (DFA). Minimization requires a DFA.</b>
                </div>
            """)
            self.save_minimized_btn.setVisible(False)
            return
        try:
            minimized = AutomataAnalyzer.minimize_dfa(automaton)
            self.minimized_automaton = minimized
            if len(minimized.states) == len(automaton.states):
                self.minimize_result.setText("""
                    <div style='color:#2ED573; font-size:15px;'>
                        <b>The DFA is already minimal. No further minimization possible.</b>
                    </div>
                """)
                self.save_minimized_btn.setVisible(False)
            else:
                summary = f"""
                    <div style='color:white;'>
                        <h3 style='color:#FF4757; margin-top:0;'>DFA Minimization Result</h3>
                        <p><b>Original DFA:</b> {automaton.name}</p>
                        <p><b>States before:</b> {len(automaton.states)} &nbsp; <b>States after:</b> {len(minimized.states)}</p>
                        <p><b>Minimized DFA name:</b> {minimized.name}</p>
                        <div style='margin-top:15px; color:#2ED573; font-size:16px;'><b>✅ Successfully minimized the DFA.</b></div>
                        <p style='color:#8A98AC; margin-top:10px;'>You can save the minimized DFA for further use.</p>
                    </div>
                """
                self.minimize_result.setText(summary)
                self.save_minimized_btn.setVisible(True)
        except Exception as e:
            self.minimize_result.setText(f"<div style='color:#FF4757;'>Error: {str(e)}</div>")
            self.save_minimized_btn.setVisible(False)

    def save_minimized_automaton(self):
        if not self.minimized_automaton:
            QMessageBox.warning(self, "Error", "No minimized DFA to save.")
            return
        name = self.minimized_automaton.name
        filename = f"{name}.json"
        try:
            # Save using AutomataManager
            manager = self.automata_manager
            prev = manager.current_automaton
            manager.current_automaton = self.minimized_automaton
            success = manager.save_automaton(filename)
            manager.current_automaton = prev
            if success:
                QMessageBox.information(self, "Success", f"Minimized DFA saved as saved_automatas/{filename}")
            else:
                QMessageBox.warning(self, "Error", f"Failed to save minimized DFA to file.")
        
        except Exception as e:    QMessageBox.warning(self, "Error", f"Failed to save minimized DFA: {str(e)}")

           
    def create_test_word_acceptance_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Test Word Acceptance")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box at the top
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Test Word Acceptance")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Enter a word using symbols from the automaton's alphabet to test if it is accepted by the current automaton."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Word input field with label
        input_label = QLabel("Enter word to test:")
        input_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.word_input = QLineEdit()
        self.word_input.setPlaceholderText("Enter word using automaton's alphabet...")
        self.word_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 300px;
            }
            QLineEdit:focus {
                border: 1px solid #00C2FF;
            }
        """)

        # Test button
        self.test_btn = ModernButton("Test Word", accent_color="#7B42F6")
        self.test_btn.setFixedWidth(200)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.test_btn.clicked.connect(self.test_word_acceptance)

        # Result label
        result_label = QLabel("Result:")
        result_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.test_result = QLabel()
        self.test_result.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                font-size: 14px;
                min-height: 80px;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        self.test_result.setText("No test performed yet. Enter a word and click 'Test Word'.")
        self.test_result.setWordWrap(True)

        # Add widgets to layout
        content.addWidget(input_label)
        content.addWidget(self.word_input)
        content.addWidget(self.test_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(result_label)
        content.addWidget(self.test_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.test_word_acceptance_page_index = self.stacked_widget.count() - 1    
    def test_word_acceptance(self):
        """Test if a given word is accepted by the current automaton"""
        from automata_operations import WordProcessor
        
        automaton = self.automata_manager.current_automaton
        word = self.word_input.text().strip()
        
        if not automaton:
            result = """
                <div style='color:#FF4757;'>
                    No automaton loaded. Please create or load an automaton first.
                </div>
            """
        elif not word:
            result = """
                <div style='color:#FF4757;'>
                    Please enter a word to test.
                </div>
            """
        else:
            try:
                # Test if the word is accepted
                is_accepted = WordProcessor.accepts_word(automaton, word)
                if is_accepted:
                    result = f"""
                        <div style='color:#2ED573; font-size:16px;'>
                            <b>✅ The word <span style='font-family: monospace;'>"{word}"</span> is accepted by the automaton.</b>
                        </div>
                    """
                else:
                    result = f"""
                        <div style='color:#FF4757; font-size:16px;'>
                            <b>❌ The word <span style='font-family: monospace;'>"{word}"</span> is not accepted by the automaton.</b>
                        </div>
                    """
            except Exception as e:
                result = f"""
                    <div style='color:#FF4757;'>
                        Error: {str(e)}
                    </div>
                """
        # Store result for persistence
        self._last_acceptance_test = result
        self.test_result.setText(result)

    def create_generate_accepted_words_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Generate Accepted Words")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box at the top
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Generate Accepted Words")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Generate all words up to a specified length that are accepted by the current automaton."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)
        
        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Max length input field with label
        input_label = QLabel("Maximum word length:")
        input_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.max_length_input = QLineEdit()
        self.max_length_input.setPlaceholderText("Enter maximum length (e.g., 5)")
        self.max_length_input.setText("5")  # Default value
        self.max_length_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 100px;
                max-width: 150px;
            }
            QLineEdit:focus {
                border: 1px solid #00C2FF;
            }
        """)

        # Generate button
        self.generate_btn = ModernButton("Generate Words", accent_color="#7B42F6")
        self.generate_btn.setFixedWidth(200)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.generate_btn.clicked.connect(self.generate_accepted_words)

        # Result display
        self.generated_words_result = QTextEdit()
        self.generated_words_result.setReadOnly(True)
        self.generated_words_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
                min-height: 200px;
            }
        """)
        self.generated_words_result.setText("No words generated yet. Select a maximum length and click 'Generate Words'.")

        # Add widgets to layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.max_length_input)
        input_layout.addStretch()

        content.addLayout(input_layout)
        content.addWidget(self.generate_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.generated_words_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.generate_accepted_words_page_index = self.stacked_widget.count() - 1    
    def generate_accepted_words(self):
        """Generate words accepted by the current automaton"""
        from automata_operations import WordProcessor
        
        automaton = self.automata_manager.current_automaton
        word = self.word_input.text().strip()
        
        if not automaton:
            result = """
                <div style='color:#FF4757;'>
                    No automaton loaded. Please create or load an automaton first.
                </div>
            """
            self._last_accepted_words = result
            self.generated_words_result.setHtml(result)
            return

        try:
            max_length = int(self.max_length_input.text().strip())
            if max_length <= 0:
                raise ValueError("Maximum length must be positive")
            if max_length > 10:
                if QMessageBox.question(
                    self, 
                    "Warning", 
                    "Generating words with length > 10 may take a long time. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.No:
                    return
        except ValueError as e:
            result = """
                <div style='color:#FF4757;'>
                    Please enter a valid positive number for maximum length.
                </div>
            """
            self._last_accepted_words = result
            self.generated_words_result.setHtml(result)
            return

        try:
            accepted_words = WordProcessor.generate_words(automaton, max_length)
            if accepted_words:
                words_by_length = {}
                for word in accepted_words:
                    length = len(word)
                    if length not in words_by_length:
                        words_by_length[length] = []
                    words_by_length[length].append(word)
                
                result = f"""
                    <div style='color:#2ED573; font-size:16px;'>
                        <b>✅ Found {len(accepted_words)} accepted word(s):</b>
                    </div>
                    <div style='color:#8A98AC; margin-top:10px;'>
                """
                
                for length in sorted(words_by_length.keys()):
                    words = sorted(words_by_length[length])
                    result += f"""
                        <p><b>Length {length}:</b></p>
                        <div style='color:white; font-family:monospace; margin-left:20px;'>
                            {', '.join(f'"{w}"' for w in words)}
                        </div>
                    """
                result += "</div>"
            else:
                result = """
                    <div style='color:#FF4757; font-size:16px;'>
                        <b>No words are accepted by this automaton up to the specified length.</b>
                    </div>
                """
        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error: {str(e)}
                </div>
            """
        # Store result for persistence
        self._last_accepted_words = result
        self.generated_words_result.setHtml(result)

    def create_generate_rejected_words_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Generate Rejected Words")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box at the top
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Generate Rejected Words")
        info_title.setStyleSheet("""
            QLabel {
                color: #FF4757;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Generate all words up to a specified length that are rejected by the current automaton."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Max length input field with label
        input_label = QLabel("Maximum word length:")
        input_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.rejected_max_length_input = QLineEdit()
        self.rejected_max_length_input.setPlaceholderText("Enter maximum length (e.g., 5)")
        self.rejected_max_length_input.setText("5")  # Default value
        self.rejected_max_length_input.setStyleSheet("""
            QLineEdit {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 8px;
                color: white;
                min-width: 100px;
                max-width: 150px;
            }
            QLineEdit:focus {
                border: 1px solid #FF4757;
            }
        """)

        # Generate button
        self.generate_rejected_btn = ModernButton("Generate Words", accent_color="#FF4757")
        self.generate_rejected_btn.setFixedWidth(200)
        self.generate_rejected_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF4757;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #FF6B81;
            }
            QPushButton:pressed {
                background-color: #FF4D67;
            }
        """)
        self.generate_rejected_btn.clicked.connect(self.generate_rejected_words)

        # Result display
        self.rejected_words_result = QTextEdit()
        self.rejected_words_result.setReadOnly(True)
        self.rejected_words_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 15px;
                min-height: 200px;            }
        """)
        self.rejected_words_result.setHtml("""<div style='color:#8A98AC;'>No words generated yet. Select a maximum length and click 'Generate Words'.</div>""")

        # Add widgets to layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.rejected_max_length_input)
        input_layout.addStretch()

        content.addLayout(input_layout)
        content.addWidget(self.generate_rejected_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.rejected_words_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.generate_rejected_words_page_index = self.stacked_widget.count() - 1    
    def generate_rejected_words(self):
        """Generate words rejected by the current automaton"""
        from automata_operations import WordProcessor
        
        automaton = self.automata_manager.current_automaton
        if not automaton:
            result = """
                <div style='color:#FF4757;'>
                    No automaton loaded. Please create or load an automaton first.
                </div>
            """
            self._last_rejected_words = result
            self.rejected_words_result.setHtml(result)
            return

        try:
            max_length = int(self.rejected_max_length_input.text().strip())
            if max_length <= 0:
                raise ValueError("Maximum length must be positive")
            if max_length > 10:
                if QMessageBox.question(
                    self, 
                    "Warning", 
                    "Generating words with length > 10 may take a long time. Continue?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                ) == QMessageBox.StandardButton.No:
                    return
        except ValueError as e:
            result = """
                <div style='color:#FF4757;'>
                    Please enter a valid positive number for maximum length.
                </div>
            """
            self._last_rejected_words = result
            self.rejected_words_result.setHtml(result)
            return

        try:
            # Generate all possible words up to max_length
            all_words = set()
            for length in range(max_length + 1):
                for word in WordProcessor.generate_all_words(automaton.alphabet, length):
                    all_words.add(word)
            
            # Get accepted words and convert to set
            accepted_words = set(WordProcessor.generate_words(automaton, max_length))
            
            # Find rejected words by set difference
            rejected_words = all_words - accepted_words
            
            if rejected_words:
                words_by_length = {}
                for word in rejected_words:
                    length = len(word)
                    if length not in words_by_length:
                        words_by_length[length] = []
                    words_by_length[length].append(word)
                
                result = f"""
                    <div style='color:#FF4757; font-size:16px;'>
                        <b>✅ Found {len(rejected_words)} rejected word(s):</b>
                    </div>
                    <div style='color:#8A98AC; margin-top:10px;'>
                """
                
                for length in sorted(words_by_length.keys()):
                    words = sorted(words_by_length[length])
                    result += f"""
                        <p><b>Length {length}:</b></p>
                        <div style='color:white; font-family:monospace; margin-left:20px;'>
                            {', '.join(f'"{w}"' for w in words)}
                        </div>
                    """
                result += "</div>"
            else:
                result = """
                    <div style='color:#FF4757; font-size:16px;'>
                        <b>No words are rejected by this automaton up to the specified length.</b>
                    </div>
                """
        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error: {str(e)}
                </div>
            """
        # Store result for persistence
        self._last_rejected_words = result
        self.rejected_words_result.setHtml(result)    
    def create_check_equivalence_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Check Equivalence")
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
        content.setContentsMargins(20, 20, 20, 20)        # Info box at the top
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Check Automata Equivalence")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Compare the current automaton with another saved automaton to check if they accept exactly the same language."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Automaton selector
        selector_label = QLabel("Select automaton to compare with:")
        selector_label.setStyleSheet("QLabel { color: white; background: transparent; }")        
        self.equivalence_automaton_list = QListWidget()
        self.equivalence_automaton_list.setStyleSheet("""
            QListWidget {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 5px;
                color: white;
                min-height: 160px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #7B42F6;
            }
            QListWidget::item:hover {
                background-color: #1E273D;
            }
        """)

        # Check button
        self.check_equivalence_btn = ModernButton("Check Equivalence", accent_color="#7B42F6")
        self.check_equivalence_btn.setFixedWidth(200)
        self.check_equivalence_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 8px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.check_equivalence_btn.clicked.connect(self.check_equivalence)

        # Result display        
        self.equivalence_result = QTextEdit()
        self.equivalence_result.setReadOnly(True)
        self.equivalence_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 5px;
                margin: 0px;             
                min-height: 35px;
                max-height: 35px;
            }
        """)
        self.equivalence_result.setHtml("Select an automaton to compare with and click 'Check Equivalence'.")

        # Add widgets to layout
        content.addWidget(selector_label)
        content.addWidget(self.equivalence_automaton_list)
        content.addWidget(self.check_equivalence_btn, 0, Qt.AlignmentFlag.AlignCenter)
        content.addWidget(self.equivalence_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.check_equivalence_page_index = self.stacked_widget.count() - 1

    def update_equivalence_automata_list(self):
        """Update the list of automata available for equivalence checking"""
        self.equivalence_automaton_list.clear()
        automata_files = []
        saved_automata_dir = os.path.join(os.getcwd(), "saved_automatas")
        if os.path.exists(saved_automata_dir):
            for file in os.listdir(saved_automata_dir):
                if file.endswith(".json"):
                    automata_files.append(file)
        self.equivalence_automaton_list.addItems(sorted(automata_files))

    def check_equivalence(self):
        """Check if the current automaton is equivalent to the selected automaton"""
        from automata_operations import AutomataAnalyzer
        
        # Get current automaton
        automaton1 = self.automata_manager.current_automaton
        if not automaton1:
            result = """
                <div style='color:#FF4757;'>
                    No automaton loaded. Please create or load an automaton first.
                </div>
            """
            self._last_equivalence_check = result
            self.equivalence_result.setHtml(result)
            return

        # Get selected automaton for comparison
        selected_items = self.equivalence_automaton_list.selectedItems()
        if not selected_items:
            result = """
                <div style='color:#FF4757;'>
                    Please select an automaton to compare with.
                </div>
            """
            self._last_equivalence_check = result
            self.equivalence_result.setHtml(result)
            return

        try:
            # Load the second automaton
            filename = selected_items[0].text()
            automaton2 = self.automata_manager.load_automaton(filename)            # Convert and minimize both automata
            if not AutomataAnalyzer.is_deterministic(automaton1):
                automaton1 = AutomataAnalyzer.nfa_to_dfa(automaton1)
            if not AutomataAnalyzer.is_deterministic(automaton2):
                automaton2 = AutomataAnalyzer.nfa_to_dfa(automaton2)
            min1 = AutomataAnalyzer.minimize_dfa(automaton1)
            min2 = AutomataAnalyzer.minimize_dfa(automaton2)
            
            # Compare number of states
            if len(min1.states) != len(min2.states):                result = """
                    <div style='margin-top:15px; color:#FF4757; font-size:16px;'>
                        <b>❌ The automata are not equivalent</b>
                    </div>
                """
            else:
                # Compare transitions
                transitions_match = True
                for state in min1.states:
                    for symbol in min1.alphabet:                        
                        trans1 = min1.transitions.get((state, symbol), set())
                        trans2 = min2.transitions.get((state, symbol), set())
                        if trans1 != trans2:
                            transitions_match = False
                            break
                    if not transitions_match:
                        break

                # Compare final states
                final_states_match = set(min1.final_states) == set(min2.final_states)               
                if transitions_match and final_states_match:
                    result = """
                        <div style='margin-top:15px; color:#2ED573; font-size:16px;'>
                            <b>✅ The automata are equivalent</b>
                        </div>
                    """
                else:
                    result = """
                        <div style='margin-top:15px; color:#FF4757; font-size:16px;'>
                            <b>❌ The automata are not equivalent</b>
                        </div>
                    """

        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error checking equivalence: {str(e)}
                </div>
            """

        # Store result for persistence
        self._last_equivalence_check = result
        self.equivalence_result.setHtml(result)

    def create_compute_union_page(self):
        """Create the page for computing union of automata"""
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Compute Union")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Compute Union")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Compute the union of the current automaton with another saved automaton. "
            "The resulting automaton will accept any string that is accepted by either automaton."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Automaton selector
        selector_label = QLabel("Select second automaton:")
        selector_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.union_automaton_list = QListWidget()
        self.union_automaton_list.setStyleSheet("""
            QListWidget {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 5px;
                color: white;
                min-height: 160px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #7B42F6;
            }
            QListWidget::item:hover {
                background-color: #1E273D;
            }
        """)

        # Button container for side-by-side buttons
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Compute button
        self.compute_union_btn = ModernButton("Compute Union", accent_color="#7B42F6")
        self.compute_union_btn.setFixedWidth(220)
        self.compute_union_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.compute_union_btn.clicked.connect(self.compute_union)

        # Save union button
        self.save_union_btn = ModernButton("Save Union Automaton", accent_color="#2ED573")
        self.save_union_btn.setFixedWidth(240)
        self.save_union_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
            QPushButton:disabled {
                background-color: #1A2133;
                color: #8A98AC;
            }
        """)
        self.save_union_btn.clicked.connect(self.save_union_automaton)
        self.save_union_btn.setEnabled(False)  # Initially disabled

        # Add buttons to container
        button_container.addWidget(self.compute_union_btn)
        button_container.addWidget(self.save_union_btn)

        # Result display
        self.union_result = QTextEdit()
        self.union_result.setReadOnly(True)
        self.union_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 5px;
                margin: 0px;             
                min-height: 35px;
                max-height: 35px;
            }
        """)
        self.union_result.setHtml("Select an automaton and click 'Compute Union' to create their union automaton.")

        # Add widgets to layout
        content.addWidget(selector_label)
        content.addWidget(self.union_automaton_list)
        content.addLayout(button_container)  # Add the button container
        content.addWidget(self.union_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.compute_union_page_index = self.stacked_widget.count() - 1
        self.union_automaton = None

    
    def update_union_automata_list(self):
        """Update the list of automata available for union computation"""
        self.union_automaton_list.clear()
        automata_files = []
        saved_automata_dir = os.path.join(os.getcwd(), "saved_automatas")
        if os.path.exists(saved_automata_dir):
            for file in os.listdir(saved_automata_dir):
                if file.endswith(".json"):
                    automata_files.append(file)
        self.union_automaton_list.addItems(sorted(automata_files))


    
    def compute_union(self):
        """Compute the union of the current automaton with the selected automaton"""        
        if not self.union_automaton_list.currentItem():
            self.union_result.setHtml('<span style="color: #FF3E3E;">Please select an automaton first.</span>')
            self.save_union_btn.setEnabled(False)
            return

        selected_name = self.union_automaton_list.currentItem().text()
        try:
            # Store the current automaton
            first_automaton = self.automata_manager.current_automaton
            
            # Load the second automaton        
            success = self.automata_manager.load_automaton(selected_name)
            if not success:
                self.union_result.setHtml('<span style="color: #FF3E3E;">Failed to load the selected automaton.</span>')
                self.save_union_btn.setEnabled(False)
                return
            
            second_automaton = self.automata_manager.current_automaton
        
            # Restore the first automaton
            self.automata_manager.current_automaton = first_automaton

            if not first_automaton:
                self.union_result.setHtml('<span style="color: #FF3E3E;">No current automaton loaded. Please load or create an automaton first.</span>')
                self.save_union_btn.setEnabled(False)
                return
            
            if not second_automaton:
                self.union_result.setHtml('<span style="color: #FF3E3E;">Failed to load second automaton.</span>')
                self.save_union_btn.setEnabled(False)
                return
            
            # Compute the union using AutomataAnalyzer
            from automata_operations import AutomataAnalyzer
            self.union_automaton = AutomataAnalyzer.compute_union(first_automaton, second_automaton)
            
            # Give the union automaton a descriptive name
            self.union_automaton.name = f"union_{first_automaton.name}_{second_automaton.name}"
            success_message = f'Union computed successfully with "{selected_name}"'
            self.union_result.setHtml(f'<span style="color: #2ED573;">{success_message}</span>')
            self.save_union_btn.setEnabled(True)  # Enable save button on successful computation
    
        except Exception as e:
            error_message = f'Error computing union: {str(e)}'
            self.union_result.setHtml(f'<span style="color: #FF3E3E;">{error_message}</span>')
            self.save_union_btn.setEnabled(False)  # Disable save button on error

    def save_union_automaton(self):
        """Save the computed union automaton"""
        if not self.union_automaton:
            return

        # Save by temporarily setting as current_automaton
        original = self.automata_manager.current_automaton
        self.automata_manager.current_automaton = self.union_automaton
        try:
            success = self.automata_manager.save_automaton(f"{self.union_automaton.name}.json")
            if success:
                result = f"""
                    <div style='color:#2ED573;'>
                        Union automaton saved successfully.
                    </div>
                """
                self.update_union_automata_list()
            else:
                result = f"""
                    <div style='color:#FF4757;'>
                        Error saving union automaton: Unknown error
                    </div>
                """
        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error saving union automaton: {str(e)}
                </div>
            """
        finally:
            self.automata_manager.current_automaton = original

        self._last_union_result = result
        self.union_result.setHtml(result)

    def create_compute_intersection_page(self):
        """Create the page for computing intersection of automata"""
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Compute Intersection")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Compute Intersection")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Compute the intersection of the current automaton with another saved automaton. "
            "The resulting automaton will accept only strings that are accepted by both automata."
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Automaton selector
        selector_label = QLabel("Select second automaton:")
        selector_label.setStyleSheet("QLabel { color: white; background: transparent; }")

        self.intersection_automaton_list = QListWidget()
        self.intersection_automaton_list.setStyleSheet("""
            QListWidget {
                background-color: #121B2E;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 5px;
                color: white;
                min-height: 160px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #7B42F6;
            }
            QListWidget::item:hover {
                background-color: #1E273D;
            }
        """)

        # Button container for side-by-side buttons
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Compute button
        self.compute_intersection_btn = ModernButton("Compute Intersection", accent_color="#7B42F6")
        self.compute_intersection_btn.setFixedWidth(220)
        self.compute_intersection_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.compute_intersection_btn.clicked.connect(self.compute_intersection)

        # Save intersection button
        self.save_intersection_btn = ModernButton("Save Intersection Automaton", accent_color="#2ED573")
        self.save_intersection_btn.setFixedWidth(240)
        self.save_intersection_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
            QPushButton:disabled {
                background-color: #1A2133;
                color: #8A98AC;
            }
        """)
        self.save_intersection_btn.clicked.connect(self.save_intersection_automaton)
        self.save_intersection_btn.setEnabled(False)  # Initially disabled

        # Add buttons to container
        button_container.addWidget(self.compute_intersection_btn)
        button_container.addWidget(self.save_intersection_btn)

        # Result display
        self.intersection_result = QTextEdit()
        self.intersection_result.setReadOnly(True)
        self.intersection_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 5px;
                margin: 0px;             
                min-height: 35px;
                max-height: 35px;
            }
        """)
        self.intersection_result.setHtml("Select an automaton and click 'Compute Intersection' to create their intersection automaton.")

        # Add widgets to layout
        content.addWidget(selector_label)
        content.addWidget(self.intersection_automaton_list)
        content.addLayout(button_container)
        content.addWidget(self.intersection_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.compute_intersection_page_index = self.stacked_widget.count() - 1
        self.intersection_automaton = None

    def compute_intersection(self):
        """Compute the intersection of the current automaton with the selected automaton"""        
        if not self.intersection_automaton_list.currentItem():
            self.intersection_result.setHtml('<span style="color: #FF3E3E;">Please select an automaton first.</span>')
            self.save_intersection_btn.setEnabled(False)
            return

        selected_name = self.intersection_automaton_list.currentItem().text()
        try:
            # Store the current automaton
            first_automaton = self.automata_manager.current_automaton
            
            # Load the second automaton        
            success = self.automata_manager.load_automaton(selected_name)
            if not success:
                self.intersection_result.setHtml('<span style="color: #FF3E3E;">Failed to load the selected automaton.</span>')
                self.save_intersection_btn.setEnabled(False)
                return
            
            second_automaton = self.automata_manager.current_automaton
        
            # Restore the first automaton
            self.automata_manager.current_automaton = first_automaton

            if not first_automaton:
                self.intersection_result.setHtml('<span style="color: #FF3E3E;">No current automaton loaded. Please load or create an automaton first.</span>')
                self.save_intersection_btn.setEnabled(False)
                return
            
            if not second_automaton:
                self.intersection_result.setHtml('<span style="color: #FF3E3E;">Failed to load second automaton.</span>')
                self.save_intersection_btn.setEnabled(False)
                return
            
            # Compute the intersection using AutomataAnalyzer
            from automata_operations import AutomataAnalyzer
            self.intersection_automaton = AutomataAnalyzer.compute_intersection(first_automaton, second_automaton)
            
            # Give the intersection automaton a descriptive name
            self.intersection_automaton.name = f"intersection_{first_automaton.name}_{second_automaton.name}"
            success_message = f'Intersection computed successfully with "{selected_name}"'
            self.intersection_result.setHtml(f'<span style="color: #2ED573;">{success_message}</span>')
            self.save_intersection_btn.setEnabled(True)  # Enable save button on successful computation
    
        except Exception as e:
            error_message = f'Error computing intersection: {str(e)}'
            self.intersection_result.setHtml(f'<span style="color: #FF3E3E;">{error_message}</span>')
            self.save_intersection_btn.setEnabled(False)  # Disable save button on error

    def save_intersection_automaton(self):
        """Save the computed intersection automaton"""
        if not self.intersection_automaton:
            return

        # Save by temporarily setting as current_automaton
        original = self.automata_manager.current_automaton
        self.automata_manager.current_automaton = self.intersection_automaton
        try:
            success = self.automata_manager.save_automaton(f"{self.intersection_automaton.name}.json")
            if success:
                result = f"""
                    <div style='color:#2ED573;'>
                        Intersection automaton saved successfully.
                    </div>
                """
                self.update_intersection_automata_list()
            else:
                result = f"""
                    <div style='color:#FF4757;'>
                        Error saving intersection automaton: Unknown error
                    </div>
                """
        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error saving intersection automaton: {str(e)}
                </div>
            """
        finally:
            self.automata_manager.current_automaton = original

        self._last_intersection_result = result
        self.intersection_result.setHtml(result)

    def create_compute_complement_page(self):
        """Create the page for computing complement of automata"""
        page = QWidget()
        layout = QVBoxLayout(page)

        group = QGroupBox("Compute Complement")
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

        content = QVBoxLayout()
        content.setContentsMargins(20, 20, 20, 20)

        # Info box with requirements
        info_box = QFrame()
        info_box.setStyleSheet("""
            QFrame {
                background-color: #1E273D;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_box)

        info_title = QLabel("ℹ️ Compute Complement")
        info_title.setStyleSheet("""
            QLabel {
                color: #00C2FF;
                font-weight: bold;
                font-size: 14px;
                background: transparent;
            }
        """)

        info_text = QLabel(
            "Create a complement automaton that accepts exactly the words that the current automaton rejects, "
            "and rejects the words it accepts. Requirements:\n\n"
            "• The automaton must be deterministic (DFA)\n"
            "• The automaton must be complete\n"
            "• Final states will become non-final, and non-final states will become final"
        )
        info_text.setWordWrap(True)
        info_text.setStyleSheet("""
            QLabel {
                color: #8A98AC;
                background: transparent;
            }
        """)

        info_layout.addWidget(info_title)
        info_layout.addWidget(info_text)
        content.addWidget(info_box)

        # Button container for side-by-side buttons
        button_container = QHBoxLayout()
        button_container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Compute button
        self.compute_complement_btn = ModernButton("Compute Complement", accent_color="#7B42F6")
        self.compute_complement_btn.setFixedWidth(220)
        self.compute_complement_btn.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
        """)
        self.compute_complement_btn.clicked.connect(self.compute_complement)

        # Save complement button
        self.save_complement_btn = ModernButton("Save Complement Automaton", accent_color="#2ED573")
        self.save_complement_btn.setFixedWidth(240)
        self.save_complement_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ED573;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 14px 15px;
                text-align: center;
                font-weight: bold;
                outline: none;
            }
            QPushButton:hover {
                background-color: #26AE60;
            }
            QPushButton:pressed {
                background-color: #1E8449;
            }
            QPushButton:disabled {
                background-color: #1A2133;
                color: #8A98AC;
            }
        """)
        self.save_complement_btn.clicked.connect(self.save_complement_automaton)
        self.save_complement_btn.setEnabled(False)  # Initially disabled

        # Add buttons to container
        button_container.addWidget(self.compute_complement_btn)
        button_container.addWidget(self.save_complement_btn)

        # Result display
        self.complement_result = QTextEdit()
        self.complement_result.setReadOnly(True)
        self.complement_result.setStyleSheet("""
            QTextEdit {
                color: #8A98AC;
                font-size: 14px;
                background-color: #121B2E;
                border: 1px dashed #2A3344;
                border-radius: 5px;
                padding: 5px;
                margin: 0px;             
                min-height: 35px;
                max-height: 35px;
            }
        """)
        self.complement_result.setHtml("Click 'Compute Complement' to create the complement automaton.")

        # Add widgets to layout
        content.addLayout(button_container)
        content.addWidget(self.complement_result)

        group.setLayout(content)
        layout.addWidget(group)
        self.stacked_widget.addWidget(page)
        self.compute_complement_page_index = self.stacked_widget.count() - 1
        self.complement_automaton = None

    def compute_complement(self):
        """Compute the complement of the current automaton"""
        from automata_operations import AutomataAnalyzer
        
        automaton = self.automata_manager.current_automaton
        if not automaton:
            self.complement_result.setHtml('<span style="color: #FF3E3E;">No automaton loaded. Please create or load an automaton first.</span>')
            self.save_complement_btn.setEnabled(False)
            return
            
        try:
            # Check if automaton is deterministic
            if not AutomataAnalyzer.is_deterministic(automaton):
                self.complement_result.setHtml('<span style="color: #FF3E3E;">The automaton must be deterministic. Convert to DFA first.</span>')
                self.save_complement_btn.setEnabled(False)
                return
            
            # Check if automaton is complete
            if not AutomataAnalyzer.is_complete(automaton):
                self.complement_result.setHtml('<span style="color: #FF3E3E;">The automaton must be complete. Make it complete first.</span>')
                self.save_complement_btn.setEnabled(False)
                return
            
            # Compute complement
            self.complement_automaton = AutomataAnalyzer.compute_complement(automaton)
            
            # Give the complement automaton a descriptive name
            self.complement_automaton.name = f"complement_{automaton.name}"
            success_message = 'Complement computed successfully'
            self.complement_result.setHtml(f'<span style="color: #2ED573;">{success_message}</span>')
            self.save_complement_btn.setEnabled(True)  # Enable save button on successful computation
    
        except Exception as e:
            error_message = f'Error computing complement: {str(e)}'
            self.complement_result.setHtml(f'<span style="color: #FF3E3E;">{error_message}</span>')
            self.save_complement_btn.setEnabled(False)  # Disable save button on error

    def save_complement_automaton(self):
        """Save the computed complement automaton"""
        if not self.complement_automaton:
            return

        # Save by temporarily setting as current_automaton
        original = self.automata_manager.current_automaton
        self.automata_manager.current_automaton = self.complement_automaton
        try:
            success = self.automata_manager.save_automaton(f"{self.complement_automaton.name}.json")
            if success:
                result = f"""
                    <div style='color:#2ED573;'>
                        Complement automaton saved successfully.
                    </div>
                """
                self.update_complement_automata_list()
            else:
                result = f"""
                    <div style='color:#FF4757;'>
                        Error saving complement automaton: Unknown error
                    </div>
                """
        except Exception as e:
            result = f"""
                <div style='color:#FF4757;'>
                    Error saving complement automaton: {str(e)}
                </div>
            """
        finally:
            self.automata_manager.current_automaton = original

        self._last_complement_result = result
        self.complement_result.setHtml(result)    
        
    def update_complement_automata_list(self):
        """Update the list of automata available for complement computation"""
        automata_files = []
        saved_automata_dir = os.path.join(os.getcwd(), "saved_automatas")
        if os.path.exists(saved_automata_dir):
            for file in os.listdir(saved_automata_dir):
                if file.endswith(".json"):
                    automata_files.append(file)

    def update_intersection_automata_list(self):
        """Update the list of automata available for intersection computation"""
        self.intersection_automaton_list.clear()
        automata_files = []
        saved_automata_dir = os.path.join(os.getcwd(), "saved_automatas")
        if os.path.exists(saved_automata_dir):
            for file in os.listdir(saved_automata_dir):
                if file.endswith(".json"):
                    automata_files.append(file)
        self.intersection_automaton_list.addItems(sorted(automata_files))

    def update_content(self, category, action):        
        page_map = {
            "Create New Automaton": 1,
            "Check Determinism": 2,
            "Check Completeness": 3,
            "Visualize Current Automaton": 4,
            "Load Automaton from File": 5,
            "Delete Saved Automaton File": 6,
            "Check Equivalence": 7,
            "Make Automaton Complete": self.make_complete_page_index,
            "Convert NFA to DFA": self.nfa_to_dfa_page_index,
            "Check Minimality": self.stacked_widget.count() - 8,
            "Minimize Automaton": self.stacked_widget.count() - 7,
            "Test Word Acceptance": self.test_word_acceptance_page_index,
            "Generate Accepted Words": self.generate_accepted_words_page_index,
            "Generate Rejected Words": self.generate_rejected_words_page_index,
            "Compute Union": self.compute_union_page_index,
            "Compute Intersection": self.compute_intersection_page_index,
            "Compute Complement": self.compute_complement_page_index
        }
        
        if action in page_map:
            self.stacked_widget.setCurrentIndex(page_map[action])
            self.title_label.setText(action)
            if action == "Delete Saved Automaton File":
                self.refresh_delete_automata_list()
            elif action == "Visualize Current Automaton":
                self.refresh_visualization()
            elif action == "Make Automaton Complete":
                self.update_make_complete_status()
            elif action == "Convert NFA to DFA":
                self.update_nfa_to_dfa_status()
            elif action == "Check Minimality":
                self.update_minimality_status()
            elif action == "Minimize Automaton":
                self.update_minimize_status()            
            elif action == "Test Word Acceptance":
                if hasattr(self, '_last_acceptance_test'):
                    self.test_result.setText(self._last_acceptance_test)
                else:
                    self.test_result.setText("No test performed yet. Enter a word and click 'Test Word'.")
            elif action == "Generate Accepted Words":
                if hasattr(self, '_last_accepted_words'):
                    self.generated_words_result.setHtml(self._last_accepted_words)
                else:
                    self.generated_words_result.setHtml("No words generated yet. Select a maximum length and click 'Generate Words'.")
            elif action == "Generate Rejected Words":
                if hasattr(self, '_last_rejected_words'):
                    self.rejected_words_result.setHtml(self._last_rejected_words)
                else:
                    self.rejected_words_result.setHtml("No words generated yet. Select a maximum length and click 'Generate Words'.")
            elif action == "Check Equivalence":
                self.update_equivalence_automata_list()
                if hasattr(self, '_last_equivalence_check'):
                    self.equivalence_result.setHtml(self._last_equivalence_check)
                else:
                    self.equivalence_result.setHtml("Select an automaton to compare with and click 'Check Equivalence'.")
            elif action == "Compute Union":
                self.update_union_automata_list()
                if hasattr(self, '_last_union_result'):
                    self.union_result.setHtml(self._last_union_result)
                else:
                    self.union_result.setHtml("Select an automaton and click 'Compute Union' to create their union automaton.")
            elif action == "Compute Intersection":
                self.update_intersection_automata_list()
                if hasattr(self, '_last_intersection_result'):
                    self.intersection_result.setHtml(self._last_intersection_result)
                else:
                    self.intersection_result.setHtml("Select an automaton and click 'Compute Intersection' to create their intersection automaton.")
            elif action == "Compute Complement":
                if hasattr(self, '_last_complement_result'):
                    self.complement_result.setHtml(self._last_complement_result)
                else:
                    self.complement_result.setHtml("Click 'Compute Complement' to create the complement of the current automaton.")
        else:
            self.stacked_widget.setCurrentIndex(0)
            self.title_label.setText("Welcome to Finite Automata Manager")

