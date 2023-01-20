import hashlib


def checksum(filename, hash_factory=hashlib.md5, chunk_num_blocks=128) -> str:
    filename = str(filename)
    h = hash_factory()
    with open(filename, 'rb') as f:
        while chunk := f.read(chunk_num_blocks * h.block_size):
            h.update(chunk)
    return h.hexdigest()
