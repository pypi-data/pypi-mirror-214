import string
import random

def random_integer(n):
    characters = string.digits
    password = ''.join(random.choice(characters) for i in range(n))
    return password

def random_string(n):
    characters = string.ascii_uppercase
    password = ''.join(random.choice(characters) for i in range(n))
    return str(password)

def random_serial(n):
    characters = string.digits + string.ascii_uppercase
    password = ''.join(random.choice(characters) for i in range(n))
    return str(password)