import argparse
import string

def check(key):
    # check if its a file !!!!!!!!!!!
    assert all(c in string.hexdigits for c in key), "key must be in hexa"
    assert len(key) == 64, "key must be 64 char long"
    return(key)


def main(args):
    print(args.__dict__)


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("-g", dest="key", type=check, help="key to encrypt")
        group.add_argument("-k", dest="base", type=check, help="base key to encrypt from")
        args = parser.parse_args()
        main(args)
    except AssertionError as msg:
        print("error:", msg)
