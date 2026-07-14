class HistoryManager:
    def __init__(self, db_manager):
        self.db = db_manager
    def save_chat(self, user_id, knowledge_base_id, user_message, bot_response):
        query = """
        INSERT INTO chat_history
        (user_id, knowledge_base_id, user_message, bot_response)
        VALUES (?, ?, ?, ?)
        """
        self.db.cursor.execute(
            query,
            (
                user_id,
                knowledge_base_id,
                user_message,
                bot_response
            )
        )
        self.db.connection.commit()
        return self.db.cursor.lastrowid
    # Get All Chats of a User
    def get_chat_history(self, user_id):
        query = """
        SELECT *
        FROM chat_history
        WHERE user_id = ?
        ORDER BY created_at ASC
        """
        self.db.cursor.execute(query, (user_id,))
        chats = self.db.cursor.fetchall()
        return chats
    # Delete One Chat
    def delete_chat(self, chat_id):
        query = """
        DELETE FROM chat_history
        WHERE id = ?
        """
        self.db.cursor.execute(query, (chat_id,))
        self.db.connection.commit()
        return True
    # Delete All Chats of a User
    def clear_chat_history(self, user_id):
        query = """
        DELETE FROM chat_history
        WHERE user_id = ?
        """
        self.db.cursor.execute(query, (user_id,))
        self.db.connection.commit()
        return True