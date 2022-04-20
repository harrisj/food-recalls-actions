#!/usr/bin/env python3
# Python program to find MD5 hash value of a file
import hashlib
import sys

def checksum_file(filename:str) -> str:
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def checksum_str(contents:bytes) -> str:
    return hashlib.md5(contents).hexdigest()


if __name__ == '__main__':
    filename = sys.argv[1]
    print(checksum_file(filename))
