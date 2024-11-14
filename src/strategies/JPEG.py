# #!/usr/bin/env python3

# https://dev.exiv2.org/projects/exiv2/wiki/The_Metadata_in_JPEG_files
# https://docs.fileformat.com/image/jpeg/ 

import os
import base64
from mutators.byteflip import byte_flip

def read_jpeg(file_path):
    with open(file_path, 'rb') as file:
        return file.read()

def write_jpeg(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb') as file:
        file.write(data)


def mutate_jpeg(input_file, binary, harness):
    original_data = read_jpeg(input_file)

    mutated_data = byte_flip(original_data)
    base64_encoded_data = base64.b64encode(mutated_data).decode('utf-8')

    harness.run_retrieve(binary, base64_encoded_data)
