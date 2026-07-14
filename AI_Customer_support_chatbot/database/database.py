import sqlite3
import os
class DatabaseManager:
    def __init__(self):
        self.db_name="chatbot.db"
        self.connection=None
        self.cursor=None
    
    def connect(self):
        self.connection=sqlite3.connect(self.db_name,check_same_thread=False)
        self.cursor=self.connection.cursor()
        print("Database Path:", os.path.abspath(self.db_name))
    def create_tables(self):

        # ================= USERS TABLE =================
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # ================= KNOWLEDGE BASE TABLE =================
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_base(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT,
            uploaded_by INTEGER,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(uploaded_by) REFERENCES users(id)
        )
        """)

        # ================= CHAT HISTORY TABLE =================
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            knowledge_base_id INTEGER,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(knowledge_base_id) REFERENCES knowledge_base(id)
        )
        """)

        # ================= FEEDBACK TABLE =================
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            feedback TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(chat_id) REFERENCES chat_history(id)
        )
        """)

        self.connection.commit()
    def close(self):
        if self.connection:
            self.connection.close()