import hashlib
from pathlib import Path


def md5(input_file: Path):
    block_size = 65_536
    hasher = hashlib.md5()
    with input_file.open('rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()
