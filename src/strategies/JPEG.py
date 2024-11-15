# #!/usr/bin/env python3

# https://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_JPEG_files
# https://docs.fileformat.com/image/jpeg/

import os
import base64
import random
from mutators.byteflip import byte_flip

class JPEGObject:
    def __init__(self, data):
        self.data = bytearray(data)

    def mutate(self, mutation):
        mutation(self.data)
        return self.data

def read_jpeg(file_path):
    with open(file_path, 'rb') as file:
        return bytearray(file.read())

def write_jpeg(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(data)

# Mutation methods
# 1: extend_sof -> extend SOF0 or S0F2 segment
def extend_sof(data):
    markers = [b'\xFF\xC0', b'\xFF\xC2']
    for marker in markers:
        start_index = data.find(marker)
        if start_index != -1:
            length_index = start_index + 2
            original_length = int.from_bytes(data[length_index:length_index+2], 'big')
            # increase the length by a random amount
            new_length = original_length + random.randint(100, 500)
            data[length_index:length_index+2] = new_length.to_bytes(2, 'big')
            # insert random bytes into the payload
            data[length_index+2:length_index+2] = bytes([random.randint(0, 255) for _ in range(new_length - original_length)])

# 2: corrupt the 'define quantization table' through invalid values
def corrupt_dqt(data):
    index = data.find(b'\xFF\xDB')
    if index != -1:
        length_index = index + 2
        length = int.from_bytes(data[length_index:length_index+2], 'big')
        corrupt_index = length_index + 2
        # corrupt 20 bytes within the DQT
        for i in range(20):
            if corrupt_index + i < len(data):
                data[corrupt_index + i] = random.randint(0, 255)

def mutate_jpeg(input_file, binary, harness):
    jpeg_data = JPEGObject(read_jpeg(input_file))
    mutations = [
        extend_sof, corrupt_dqt
    ]

    for mutation in mutations:
        mutated_data = jpeg_data.mutate(mutation)
        base64_encoded_data = base64.b64encode(mutated_data).decode('utf-8')
        harness.run_retrieve(binary, base64_encoded_data)
        jpeg_data.data = read_jpeg(input_file)
