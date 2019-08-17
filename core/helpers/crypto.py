import os
import hashlib


def new_secret_key():
    return os.urandom(16)


def hash_key(blob):
    """ Make a hash key """

    return hashlib.md5(str(blob).encode()).digest().hex()
