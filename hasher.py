import random

LENGTH = 6


def create_hash(url):
    ''' creates a random string of length LENGTH. Could be better '''
    # isn't really a hash function
    LETTERS = '0123456789qwertyuiopasdfghjklzxcvbnm'
    return ''.join(random.choice(LETTERS) for i in range(LENGTH))
