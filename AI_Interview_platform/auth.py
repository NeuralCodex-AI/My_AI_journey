import hashlib
from database import (
    create_user,
    get_user_by_email,
    get_user_by_id
)
def hash_password(
    password
):
    """
    Convert plain password into
    secure hashed password.
    Password is never stored
    directly in database.
    """
    hashed_password = hashlib.sha256(
        password.encode()
    ).hexdigest()
    return hashed_password
def verify_password(
    password,
    hashed_password
):
    """
    Check whether entered password
    matches stored hashed password.
    """
    entered_password_hash = hash_password(
        password
    )
    return (
        entered_password_hash
        == hashed_password
    )
def register_user(
    name,
    email,
    password
):
    """
    Register a new user.
    Steps:
    1. Check if email already exists
    2. Hash password
    3. Save user
    4. Return user ID
    """
    existing_user = get_user_by_email(
        email
    )
    if existing_user:
        return {
            "success": False,
            "message":
                "Email already registered."
        }
    if len(password) < 6:
        return {
            "success": False,
            "message":
                "Password must contain at least 6 characters."
        }
    hashed_password = hash_password(
        password
    )
    user_id = create_user(
        name,
        email,
        hashed_password
    )
    if user_id is None:
        return {
            "success": False,

            "message":
                "Could not create account."
        }
    return {
        "success": True,
        "message":
            "Account created successfully.",
        "user_id":
            user_id
    }
def login_user(
    email,
    password
):
    """
    Authenticate user.
    Steps:
    1. Find user by email
    2. Verify password
    3. Return user information
    """
    user = get_user_by_email(
        email
    )
    if user is None:
        return {
            "success": False,
            "message":
                "Invalid email or password."
        }
    password_correct = verify_password(
        password,
        user["password"]
    )
    if not password_correct:
        return {
            "success": False,
            "message":
                "Invalid email or password."
        }

    return {
        "success": True,
        "message":
            "Login successful.",
        "user_id":
            user["id"],
        "name":
            user["name"],
        "email":
            user["email"]
    }
def get_current_user(
    user_id
):
    """
    Get logged-in user's information.
    """
    user = get_user_by_id(
        user_id
    )
    return user
def is_authenticated(
    user_id
):
    """
    Check whether user exists
    and is authenticated.
    """
    if user_id is None:
        return False
    user = get_user_by_id(
        user_id
    )
    if user is None:
        return False
    return True