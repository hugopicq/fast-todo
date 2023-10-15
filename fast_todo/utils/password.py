import re
import bcrypt

def is_password_complex(password: str) -> bool:
    """
    Function to check password complexity. A password is complex if:
    - It has at least 12 characters
    - It contains lowercase, uppercase and numbers
    """

    if len(password) < 12:
        return False
    if re.search(r"\d", password) is None:
        return False
    if re.search(r"[A-Z]", password) is None:
        return False
    if re.search(r"[a-z]", password) is None:
        return False
    
    return True

def hash_password(password: str) -> str:
    """
    Function to hash a password
    """
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes(password, encoding='utf-8'), salt=salt)

    return hash.decode('utf-8')

def chech_password(password: str, hash: str) -> bool:
    """
    Function to check whether a password matches a hash
    """

    return bcrypt.checkpw(bytes(password, encoding='utf-8'), bytes(hash, encoding='utf-8'))