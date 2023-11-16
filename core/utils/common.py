import random
import string


def generate_random_string(n: int) -> str:
    return "".join(random.choice(string.hexdigits) for i in range(n))

def try_catch(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
    except Exception as e:
        print(f"Exception: {e}")