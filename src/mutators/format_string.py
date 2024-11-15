import random

def format_string_attack(data) -> bytearray:
    format_strings = [b'%s', b'%x', b'%n', b'%d', b'%p']
    result = b""
    while len(result) < 15:
        result += random.choice(format_strings)
    return result