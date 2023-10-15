import random
import string

def random_string(n: int) -> str:
    """Generate a random string of length n"""
    return "".join(random.choice(string.ascii_letters) for i in range(n))