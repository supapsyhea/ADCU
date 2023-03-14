import random
import string


def password() -> str:
    password: str = ''.join(random.choice(
        string.ascii_letters + string.digits
        ) for i in range(10))
    return password