# #!/usr/bin/env python3

import random

def remove_random_segment(data):
    segments = [b'\xff\xe0', b'\xff\xe1', b'\xff\xdb']
    segment_to_remove = random.choice(segments)
    return data.replace(segment_to_remove, b'')
