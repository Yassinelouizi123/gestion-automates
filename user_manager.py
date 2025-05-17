# user_manager.py
import sqlite3
from passlib.hash import pbkdf2_sha256
from typing import Optional, Tuple

class UserManager:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self.current_user = None  # Store current logged in user
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users
                         (username TEXT PRIMARY KEY,
                          password_hash TEXT NOT NULL,
                          role TEXT NOT NULL,
                          display_name TEXT,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          is_active BOOLEAN DEFAULT TRUE,
                          theme_preference TEXT DEFAULT 'dark',
                          ui_scale INTEGER DEFAULT 100)''')
            conn.commit()

            # Create default admin user if none exists
            if not self.get_user('admin'):
                self.create_user(
                    username='admin',
                    password='admin123',
                    role='admin',
                    display_name='Administrator',
                    active=True
                )

    def create_user(self, username: str, password: str, role: str = 'user', display_name: str = None, active: bool = True) -> bool:
        if self.get_user(username):
            return False
            
        if display_name is None:
            display_name = username
            
        hashed = pbkdf2_sha256.hash(password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO users (username, password_hash, role, display_name, is_active) '
                         'VALUES (?, ?, ?, ?, ?)',
                         (username, hashed, role, display_name, active))
            conn.commit()
        return True

    def authenticate(self, username: str, password: str) -> Tuple[bool, Optional[dict]]:
        user = self.get_user(username)
        if not user or not user['is_active']:
            return False, None
            
        if pbkdf2_sha256.verify(password, user['password_hash']):
            return True, user
        return False, None

    def get_user(self, username: str) -> Optional[dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return dict(result) if result else None

    def update_password(self, username: str, new_password: str) -> bool:
        hashed = pbkdf2_sha256.hash(new_password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE users SET password_hash = ? WHERE username = ?',
                         (hashed, username))
            conn.commit()
        return True

    def set_user_active(self, username: str, active: bool) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE users SET is_active = ? WHERE username = ?',
                         (active, username))
            conn.commit()
        return True

    def get_all_users(self) -> list:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM users ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def delete_user(self, username: str, requesting_user: dict) -> bool:
        """Delete a user account. Only admins can delete users, and only superuser (admin) can delete other admins."""
        if not requesting_user or requesting_user['role'] != 'admin':
            return False
            
        user_to_delete = self.get_user(username)
        if not user_to_delete:
            return False
            
        # Only superuser (admin) can delete admin accounts
        if user_to_delete['role'] == 'admin' and requesting_user['username'] != 'admin':
            return False
            
        # Prevent self-deletion
        if username == requesting_user['username']:
            return False
            
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
        return True

    def reset_password(self, username: str, new_password: str, requesting_user: dict) -> bool:
        """Reset a user's password. Only admins can reset passwords, and only superuser (admin) can reset other admin passwords."""
        if not requesting_user or requesting_user['role'] != 'admin':
            return False
            
        user_to_reset = self.get_user(username)
        if not user_to_reset:
            return False
            
        # Only superuser (admin) can reset admin account passwords
        if user_to_reset['role'] == 'admin' and requesting_user['username'] != 'admin':
            return False
            
        # Reset the password
        return self.update_password(username, new_password)

    def update_display_name(self, username: str, display_name: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE users SET display_name = ? WHERE username = ?',
                         (display_name, username))
            conn.commit()
        return True

    def update_theme_preference(self, username: str, theme: str) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE users SET theme_preference = ? WHERE username = ?',
                         (theme, username))
            conn.commit()
        return True

    def update_ui_scale(self, username: str, scale: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('UPDATE users SET ui_scale = ? WHERE username = ?',
                         (scale, username))
            conn.commit()
        return True

    def bulk_delete_users(self, usernames: list, requesting_user: dict) -> tuple[bool, list]:
        """Delete multiple user accounts at once. Returns (success, failed_deletions)."""
        if not requesting_user or requesting_user['role'] != 'admin':
            return False, usernames
            
        failed_deletions = []
        for username in usernames:
            if not self.delete_user(username, requesting_user):
                failed_deletions.append(username)
                
        return True, failed_deletions