# user_manager.py
import sqlite3
from passlib.hash import pbkdf2_sha256
from typing import Optional, Tuple

class UserManager:
    def __init__(self, db_path='users.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users
                         (username TEXT PRIMARY KEY,
                          password_hash TEXT NOT NULL,
                          role TEXT NOT NULL,
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                          is_active BOOLEAN DEFAULT TRUE)''')
            conn.commit()

            # Create default admin user if none exists
            if not self.get_user('admin'):
                self.create_user(
                    username='admin',
                    password='admin123',
                    role='admin',
                    active=True
                )

    def create_user(self, username: str, password: str, role: str = 'user', active: bool = True) -> bool:
        if self.get_user(username):
            return False
            
        hashed = pbkdf2_sha256.hash(password)
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('INSERT INTO users (username, password_hash, role, is_active) '
                         'VALUES (?, ?, ?, ?)',
                         (username, hashed, role, active))
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