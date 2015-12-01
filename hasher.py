import random

LENGTH = 6


def create_hash(url):
    LETTERS = '0123456789qwertyuiopasdfghjklzxcvbnm'
    return ''.join(random.choice(LETTERS) for i in range(LENGTH))
