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

# 3: shuffle random segements e.g. DQT, DHT, SOF
def shuffle_segments(data):
    segments = [b'\xFF\xC0', b'\xFF\xC2', b'\xFF\xC4', b'\xFF\xDB', b'\xFF\xDD', b'\xFF\xDA', b'\xFF\xD9']
    start_indices = [data.find(segment) for segment in segments if data.find(segment) != -1]
    if not start_indices:
        return
    start_indices.sort()
    segment_data = [data[start:end] for start, end in zip(start_indices, start_indices[1:] + [None])]
    random.shuffle(segment_data)
    new_data = bytearray()
    for segment in segment_data:
        new_data.extend(segment)
    data[:] = new_data

# 4: huffman table DHT
def corrupt_huffman_tables(data):
    dht_index = data.find(b'\xFF\xC4')
    if dht_index != -1:
        length_index = dht_index + 2
        length = int.from_bytes(data[length_index:length_index + 2], 'big')
        end_index = length_index + 2 + length
        for i in range(length_index + 2, end_index):
            data[i] = data[i] ^ random.randint(0x00, 0xFF)

#5: corrupt start and end of frame
def corrupt_soi_eoi(data):
    soi_index = data.find(b'\xFF\xD8')
    if soi_index != -1:
        data[soi_index:soi_index+2] = b'\xFF\xD7'
    eoi_index = data.rfind(b'\xFF\xD9')
    if eoi_index != -1:
        data[eoi_index:eoi_index+2] = b'\xFF\xD8'


def mutate_jpeg(input_file, binary, harness):
    jpeg_data = JPEGObject(read_jpeg(input_file))
    mutations = [
        extend_sof, corrupt_dqt, shuffle_segments, corrupt_huffman_tables
    ]

    for mutation in mutations:
        mutated_data = jpeg_data.mutate(mutation)
        base64_encoded_data = base64.b64encode(mutated_data).decode('utf-8')
        harness.run_retrieve(binary, base64_encoded_data)
        jpeg_data.data = read_jpeg(input_file)
