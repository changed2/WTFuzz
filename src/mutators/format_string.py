import random

def format_string_attack() -> bytearray:
    format_strings = [b'%s', b'%x', b'%n', b'%d', b'%p']
    result = b""
    while len(result) < 30:
        result += random.choice(format_strings)
    return result