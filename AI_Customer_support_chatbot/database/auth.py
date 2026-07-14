import bcrypt

class Authentication:
    def __init__(self, db_manager):
        self.db = db_manager
    # Check if email already exists
    def email_exists(self, email):
        query = "SELECT * FROM users WHERE email = ?"
        self.db.cursor.execute(query, (email,))
        user = self.db.cursor.fetchone()
        return user is not None
    # Hash Password
    def hash_password(self, password):
        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        )
        return hashed.decode()
    # Verify Password
    def verify_password(self, password, hashed_password):
        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode()
        )
    # Register User
    def register_user(self, name, email, password):
        if self.email_exists(email):
            return False, "Email already exists."
        hashed_password = self.hash_password(password)
        query = """
        INSERT INTO users(name, email, password)
        VALUES (?, ?, ?)
        """
        self.db.cursor.execute(
            query,
            (name, email, hashed_password)
        )
        self.db.connection.commit()
        return True, "Registration Successful."
    # Login User
    def login_user(self, email, password):
        query = "SELECT * FROM users WHERE email = ?"
        self.db.cursor.execute(query, (email,))
        user = self.db.cursor.fetchone()
        if user is None:
            return False, "User not found."
        stored_password = user[3]
        if self.verify_password(password, stored_password):
            return True, user
        return False, "Incorrect Password."