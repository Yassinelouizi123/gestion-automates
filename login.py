from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, 
                            QPushButton, QMessageBox, QGraphicsDropShadowEffect, QMainWindow,
                            QFrame, QApplication)
from PyQt6.QtCore import (pyqtSignal, Qt, QTimer, QPropertyAnimation, QEasingCurve, 
                         QPointF, QRectF, pyqtProperty)
from PyQt6.QtGui import QFont, QColor, QPainter, QLinearGradient, QPen, QBrush
from user_manager import UserManager
import math
import random
import sys


class Particle:
    def __init__(self, x, y, size, speed, color, direction, opacity=1.0):
        self.x = x
        self.y = y
        self.size = max(3, min(size, 6))  # Clamp size between 3 and 6
        self.speed = max(0.1, min(speed, 0.5))  # Clamp speed between 0.1 and 0.5
        self.color = color
        self.direction = direction  # angle in radians
        self.opacity = opacity
        self.life = 1.0  # Life decreases over time
        self.life_reduction = random.uniform(0.0005, 0.001)  # Slower life reduction

    def update(self):
        # Move the particle
        self.x += math.cos(self.direction) * self.speed
        self.y += math.sin(self.direction) * self.speed
        
        # Reduce life
        self.life -= self.life_reduction
        self.opacity = self.life

    def is_alive(self):
        return self.life > 0


class ParticleSystem:
    def __init__(self, width, height):
        self.width = width if width > 0 else 900  # Default minimum width
        self.height = height if height > 0 else 600  # Default minimum height
        self.particles = []
        self.colors = [
            QColor(123, 104, 238, 150),  # Medium slate blue
            QColor(106, 90, 205, 150),   # Slate blue
            QColor(138, 43, 226, 150),   # Blue violet
            QColor(148, 0, 211, 150),    # Dark violet
            QColor(153, 50, 204, 150),   # Dark orchid
        ]
        
    def generate_particles(self, count):
        # Clear existing particles when regenerating
        self.particles.clear()
        
        # Create random clusters of particles
        for _ in range(count):
            # Pick a random point as cluster center
            center_x = random.uniform(0, self.width)
            center_y = random.uniform(0, self.height)
            
            # Add some randomness to position around the center
            spread = 50  # How far particles can spread from center
            x = max(0, min(self.width, center_x + random.uniform(-spread, spread)))
            y = max(0, min(self.height, center_y + random.uniform(-spread, spread)))
            
            size = random.randint(3, 5)  # More controlled size range
            speed = random.uniform(0.2, 0.4)  # More controlled speed range
            color = random.choice(self.colors)
            direction = random.uniform(0, 2 * math.pi)
            opacity = random.uniform(0.5, 0.8)  # Higher minimum opacity
            
            self.particles.append(Particle(x, y, size, speed, color, direction, opacity))
            
    def update(self):
        # Update existing particles
        for particle in self.particles[:]:
            particle.update()
            
            # Remove dead particles
            if not particle.is_alive():
                self.particles.remove(particle)
                
                # Create a new particle at a random edge of the screen
                edge = random.randint(0, 3)  # 0: top, 1: right, 2: bottom, 3: left
                if edge == 0:  # top
                    x = random.uniform(0, self.width)
                    y = 0
                    direction = random.uniform(math.pi/4, 3*math.pi/4)  # Move downward
                elif edge == 1:  # right
                    x = self.width
                    y = random.uniform(0, self.height)
                    direction = random.uniform(3*math.pi/4, 5*math.pi/4)  # Move leftward
                elif edge == 2:  # bottom
                    x = random.uniform(0, self.width)
                    y = self.height
                    direction = random.uniform(5*math.pi/4, 7*math.pi/4)  # Move upward
                else:  # left
                    x = 0
                    y = random.uniform(0, self.height)
                    direction = random.uniform(-math.pi/4, math.pi/4)  # Move rightward
                
                size = random.randint(3, 5)
                speed = random.uniform(0.2, 0.4)
                color = random.choice(self.colors)
                opacity = random.uniform(0.5, 0.8)
                
                self.particles.append(Particle(x, y, size, speed, color, direction, opacity))
            else:
                # Wrap particles around the screen
                if particle.x < 0:
                    particle.x = self.width
                elif particle.x > self.width:
                    particle.x = 0
                
                if particle.y < 0:
                    particle.y = self.height
                elif particle.y > self.height:
                    particle.y = 0


class PulsatingButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self._size_factor = 1.0
        
        # Style the button
        self.setStyleSheet("""
            QPushButton {
                background-color: #7B42F6;
                color: white;
                border-radius: 20px;
                font-size: 16px;
                font-weight: bold;
                padding: 12px;
                outline: none;
            }
            QPushButton:hover {
                background-color: #6935D8;
            }
            QPushButton:pressed {
                background-color: #5D2EC2;
            }
            QPushButton:focus {
                outline: none;
            }
        """)
        
        # Setup animation
        self.animation = QPropertyAnimation(self, b"sizeFactor", self)  # Set parent to self
        self.animation.setDuration(1500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(1.05)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setLoopCount(-1)  # Infinite loop
        
        # Add drop shadow
        shadow = QGraphicsDropShadowEffect(self)  # Set parent to self
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(123, 66, 246, 100))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
        
        # Start the animation after everything is set up
        self.animation.finished.connect(self.restart_animation)
        self.animation.start()
    
    def restart_animation(self):
        if self.animation and not self.animation.targetObject().isNull():
            # Reverse the animation
            start_val = self.animation.startValue()
            end_val = self.animation.endValue()
            self.animation.setStartValue(end_val)
            self.animation.setEndValue(start_val)
            self.animation.start()
    
    def get_size_factor(self):
        return self._size_factor
        
    def set_size_factor(self, factor):
        self._size_factor = factor
        self.style().polish(self)
        self.update()
        
    sizeFactor = pyqtProperty(float, get_size_factor, set_size_factor)


class FloatingInput(QWidget):
    def __init__(self, placeholder, is_password=False, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(2)
        
        self.placeholder = placeholder
        
        # Create label that's always visible
        self.label = QLabel(placeholder)
        self.label.setStyleSheet("color: #7B42F6; font-size: 12px; font-weight: bold;")
        
        # Create input field
        self.input = QLineEdit()
        if is_password:
            self.input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Style the input
        self.input.setStyleSheet("""
            QLineEdit {
                background-color: #1A2133;
                border: 1px solid #2A3344;
                border-radius: 5px;
                padding: 12px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #7B42F6;
            }
        """)
        
        # Add widgets to layout
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        
    def text(self):
        return self.input.text()
    
    def setText(self, text):
        self.input.setText(text)
        
    def returnPressed(self):
        return self.input.returnPressed
    
    def setFocus(self):
        self.input.setFocus()
    
    def clear(self):
        self.input.clear()


class LoginWidget(QWidget):
    login_successful = pyqtSignal(dict)  # Emit user data on success

    def __init__(self, user_manager: UserManager):
        super().__init__()
        self.user_manager = user_manager
        
        # Create particle system with minimum dimensions
        self.particle_system = ParticleSystem(900, 600)  # Use minimum window size
        self.particle_system.generate_particles(100)  # Generate initial particles
        
        # Set up animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(16)  # ~60 FPS
        
        self.initUI()
        
    def initUI(self):
        # Set up the layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Create left panel (dark blue with logo)
        left_panel = QWidget()
        left_panel.setStyleSheet("background-color: transparent;")
        left_panel.setFixedWidth(360)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(40, 40, 40, 40)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Logo placeholder
        logo_label = QLabel("FA Manager")
        logo_label.setFont(QFont("Arial", 36, QFont.Weight.Bold))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_label.setStyleSheet("color: #7B42F6; margin-bottom: 20px;")
        
        # Description
        desc_label = QLabel("Advanced Finite Automata\nManagement Tool")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet("color: #8A98AC; font-size: 16px; margin-bottom: 30px;")
        
        left_layout.addStretch(1)
        left_layout.addWidget(logo_label)
        left_layout.addWidget(desc_label)
        left_layout.addStretch(1)
        
        # Create right panel (login form)
        right_panel = QWidget()
        right_panel.setStyleSheet("background-color: transparent;")
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(50, 40, 50, 40)
        right_layout.setSpacing(20)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Login title
        login_title = QLabel("Sign In")
        login_title.setFont(QFont("Arial", 32, QFont.Weight.Bold))
        login_title.setStyleSheet("color: white; margin-bottom: 20px;")
        login_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Form container
        form_container = QWidget()
        form_layout = QVBoxLayout(form_container)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(15)
        
        # Username field
        self.username_edit = FloatingInput("Username")
        
        # Password field
        self.password_edit = FloatingInput("Password", is_password=True)
        
        # Error message label
        self.error_label = QLabel("")
        self.error_label.setStyleSheet("""
            QLabel {
                color: #FF4757;
                font-size: 13px;
                padding: 0px;
                min-height: 20px;
                qproperty-alignment: AlignCenter;
            }
        """)
        self.error_label.hide()
        
        # Login button
        self.login_button = PulsatingButton("Sign In")
        self.login_button.setFixedHeight(50)
        self.login_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.login_button.clicked.connect(self.attempt_login)
        
        # Add widgets to form layout
        form_layout.addWidget(self.username_edit)
        form_layout.addWidget(self.password_edit)
        form_layout.addWidget(self.error_label)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.login_button)
        
        # Add widgets to right layout
        right_layout.addStretch(1)
        right_layout.addWidget(login_title)
        right_layout.addWidget(form_container)
        right_layout.addStretch(1)
        
        # Add both panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        # Connect enter key to login button
        self.password_edit.returnPressed().connect(self.login_button.click)
        self.username_edit.returnPressed().connect(lambda: self.password_edit.setFocus())
    
    def attempt_login(self):
        self.error_label.hide()
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        
        if not username or not password:
            self.error_label.setText("Please enter both username and password")
            self.error_label.show()
            return
            
        valid, user = self.user_manager.authenticate(username, password)
        if valid and user:
            self.user_manager.current_user = user  # Set current user in UserManager
            self.login_successful.emit(user)
        else:
            self.error_label.setText("Invalid username or password")
            self.error_label.show()
            self.password_edit.clear()  # Clear password field for security
            
    def update_animation(self):
        self.particle_system.update()
        self.update()  # Trigger a repaint
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw a dark background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(14, 21, 37))  # Dark navy blue
        gradient.setColorAt(1, QColor(18, 27, 46))  # Darker navy blue
        painter.fillRect(0, 0, self.width(), self.height(), gradient)
        
        # Draw particles
        for particle in self.particle_system.particles:
            if particle.is_alive():
                color = particle.color
                color.setAlphaF(particle.opacity)
                painter.setBrush(QBrush(color))
                painter.setPen(Qt.PenStyle.NoPen)
                
                # Draw glowing circle
                glow_radius = particle.size * 3
                center = QPointF(particle.x, particle.y)
                
                # Create radial gradient for glow effect
                glow_color = QColor(particle.color)
                glow_color.setAlphaF(0.1 * particle.opacity)
                painter.setBrush(QBrush(glow_color))
                painter.drawEllipse(center, glow_radius, glow_radius)
                
                # Draw the particle itself
                painter.setBrush(QBrush(color))
                painter.drawEllipse(center, particle.size, particle.size)
        
        # Draw a subtle connection between nearby particles
        painter.setPen(QPen(QColor(123, 66, 246, 30), 0.5))
        
        for i, p1 in enumerate(self.particle_system.particles):
            for p2 in self.particle_system.particles[i+1:]:
                # Calculate distance between particles
                dx = p1.x - p2.x
                dy = p1.y - p2.y
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Draw line if particles are close enough
                if distance < 100:
                    # Make line more transparent with distance
                    alpha = 30 * (1 - distance/100) * min(p1.opacity, p2.opacity)
                    pen = QPen(QColor(123, 66, 246, int(alpha)), 0.5)
                    painter.setPen(pen)
                    painter.drawLine(int(p1.x), int(p1.y), int(p2.x), int(p2.y))
    
    def resizeEvent(self, event):
        # Update particle system dimensions when window is resized
        self.particle_system.width = self.width()
        self.particle_system.height = self.height()
        self.particle_system.generate_particles(100)  # Regenerate particles with new dimensions
        super().resizeEvent(event)


# For testing purposes
if __name__ == "__main__":
    class MockUserManager:
        def __init__(self):
            self.current_user = None
            
        def authenticate(self, username, password):
            # Mock authentication - always succeeds with test data
            if username and password:
                return True, {"username": username, "role": "admin"}
            return False, None
    
    app = QApplication(sys.argv)
    user_manager = MockUserManager()
    login_widget = LoginWidget(user_manager)
    
    # Create main window to hold the login widget
    main_window = QMainWindow()
    main_window.setCentralWidget(login_widget)
    main_window.setWindowTitle("Finite Automata Manager")
    main_window.setMinimumSize(900, 600)
    main_window.show()
    
    sys.exit(app.exec())