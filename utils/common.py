import random
import string


def generate_random_string(n: int) -> str:
    return "".join(random.choice(string.hexdigits) for i in range(n))

