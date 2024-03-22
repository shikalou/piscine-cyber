import argparse
import string
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import binascii

def check(key: str):
    assert all([c in string.hexdigits for c in key]), "key must be in hexa"
    assert len(key) == 64, "key must be 64 char long"


def open_file(path) -> str:
    f = open(path, "+r")
    ret = f.read()
    return (ret.strip("\n, "))


def encript(key):
    password = bytes.fromhex(key)
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
    algorithm=hashes.SHA1(),
    length=32,
    salt=salt,
    iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    with open("ft_opt.key", 'wb') as file:
        file.write(key)
    new = str(key)[2:33]
    n = bin(int(binascii.hexlify(bytes(new, encoding='utf8')),16))[2:]
    nint = int(str(n), 2)
    print(nint % 10**123)



def optionK(args):
    print("lol2")


def main(args):
    if args.key: # -g
        if os.path.isfile(args.key):
            key = open_file(args.key)
        else:
            key = args.key
        check(key)
        encript(key)
    else: # -k
        check(args.base)
        optionK(args)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-g", dest="key", type=str, help="64 long hexadecimal key to store in encrypted file")
        group.add_argument("-k", dest="base", type=str, help="generate new temporary password based on the given key")
        args = parser.parse_args()
        main(args)
    except AssertionError as msg:
        print("ft_opt.py: error:", msg)
