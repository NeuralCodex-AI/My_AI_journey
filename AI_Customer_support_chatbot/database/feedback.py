class FeedbackManager:
    def __init__(self, db_manager):
        self.db = db_manager
    # Save Feedback
    def save_feedback(self, chat_id, feedback):
        query = """
            INSERT INTO feedback(chat_id, feedback)
            VALUES (?, ?)
         """
        self.db.cursor.execute(
        query,
        (chat_id, feedback)
        )
        self.db.connection.commit()
        self.db.cursor.execute("SELECT COUNT(*) FROM feedback")
        print("Feedback Rows:", self.db.cursor.fetchone()[0])
        return True
    # Get All Feedback
    def get_feedback(self):
        query = """
        SELECT
            feedback.id,
            feedback.chat_id,
            feedback.feedback,
            feedback.created_at,
            chat_history.user_message,
            chat_history.bot_response
        FROM feedback
        INNER JOIN chat_history
        ON feedback.chat_id = chat_history.id
        ORDER BY feedback.created_at DESC
        """
        self.db.cursor.execute(query)
        feedbacks = self.db.cursor.fetchall()
        return feedbacks
    # Delete Feedback
    def delete_feedback(self, feedback_id):
        query = """
        DELETE FROM feedback
        WHERE id = ?
        """
        self.db.cursor.execute(
            query,
            (feedback_id,)
        )
        self.db.connection.commit()
        return True