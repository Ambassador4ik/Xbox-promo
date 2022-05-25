import random
import string


def gen(n):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(n))


def gen_email():
    return gen(16) + '@hotmail.com'
