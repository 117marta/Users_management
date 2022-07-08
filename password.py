import string
import random
import hashlib


ALPHABET = string.ascii_uppercase + string.ascii_lowercase + string.digits
"""
Global variable that keeps all uppercase and lower letter and all digits
"""


def generate_salt():
    """
    Generates a 16-character random salt.

    :rtype: str
    :return: str with generated salt
    """
    salt = ""
    for i in range(0, 16):
        salt += random.choice(ALPHABET)
    return salt


def hash_password(password, salt=None):
    """
    Hashes the password with salt (as an optional parameter).
    :param str password: password to hash
    :param str salt: salt to hash
    :return: hashed password
    """
    if salt is None:
        salt = generate_salt()

    if len(salt) < 16:
        salt += ("z" * (16 - len(salt)))

    if len(salt) > 16:
        salt = salt[:16]

    sha = hashlib.sha256()  # algorytm haszujący SHA256
    sha.update(salt.encode('utf-8') + password.encode('utf-8'))  # encode is required by hashlib library
    return salt + sha.hexdigest()


def check_password(pass_to_check, pass_hashed):
    """
    Checks the password.
    :param str pass_to_check: not hashed password
    :param str pass_hashed: hashed password
    :rtype: bool
    :return: True (password correct) or False (elsewhere)
    """
    old_salt = pass_hashed[:16]
    old_hash = pass_hashed[16:]
    new_pass = hash_password(pass_to_check, old_salt)
    return new_pass[16:] == old_hash
