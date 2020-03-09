import math


def convert_file_size_to_mb(size_bytes):
    return math.ceil(size_bytes / math.pow(1024, 2))
