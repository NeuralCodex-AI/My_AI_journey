import bcrypt
import streamlit as st

from utils.mongo import MongoDB
from utils.helper import current_time


class Auth:

    def __init__(self):

        self.db = MongoDB()
        self.users = "users"

        if "logged_in" not in st.session_state:
            st.session_state.logged_in = False

        if "user" not in st.session_state:
            st.session_state.user = None


    def hash_password(self, password):

        return bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()


    def verify_password(
        self,
        password,
        hashed_password
    ):

        return bcrypt.checkpw(
            password.encode(),
            hashed_password.encode()
        )


    def signup(
        self,
        name,
        email,
        password
    ):

        if self.db.find_one(
            self.users,
            {
                "email": email
            }
        ):
            return False, "Email already exists."

        user = {
            "name": name,
            "email": email,
            "password": self.hash_password(password),
            "created_at": current_time()
        }

        self.db.insert_one(
            self.users,
            user
        )

        return True, "Account created successfully."


    def login(
        self,
        email,
        password
    ):

        user = self.db.find_one(
            self.users,
            {
                "email": email
            }
        )

        if not user:
            return False, "Invalid email."

        if not self.verify_password(
            password,
            user["password"]
        ):
            return False, "Invalid password."

        st.session_state.logged_in = True
        st.session_state.user = {
            "name": user["name"],
            "email": user["email"]
        }

        return True, "Login successful."


    def logout(self):

        st.session_state.logged_in = False
        st.session_state.user = None