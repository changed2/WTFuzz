#!/usr/bin/env python3

import os
import subprocess
import random
import sys
from magic import from_file

def detect_input_format(file_path):
    file_type = from_file(file_path)
    if "CSV" in file_type:
        print("CSV Detected")
        return
    elif "JSON" in file_type:
        print("JSON Detected")
        return
    
    print("Unknown type, plaintext selected")

file_path = 'example_inputs/csv1.txt'
detected_format = detect_input_format(file_path)

def random_input(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    out = ""
    string_length = random.randrange(0, max_length + 1)
    for _ in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} [filename] [input_file]")
        exit()
        
    program = sys.argv[1]
    input_file = sys.argv[2]
    
    # Detect the type of the sample input (JSON or CSV)
    detect_input_format(input_file)

    with open(input_file, "w") as f:
        f.write(random_input())
        
    with open(input_file, "r") as input_file:
        process = subprocess.Popen([program], stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        
    print(f"PROGRAM OUTPUT: {output.decode().strip()}")
    
    if errors:
        print(f"PROGRAM ERRORS: {errors.decode().strip()}")

'''
TODO:
    - Figure out what type of file input a program expects and create the payload accordingly
        1. Find the actual file input type
        2. Create appropriate payload
    - Different input mutation strategies (JSON and CSV for checkin)
        - csv: large values in columns
            - numbers: postive and negative
            - remove random commas from csv 
    - Exploit detection
        - Buffer overflows (Large random strings)
        - Format strings   (% symbols with characters such as p, n, x, c, s)
    - Code coverage checker
'''

'''
Some hints if you are stuck on where to start.

- Try sending some known sample inputs (nothing, certain numbers, certain strings, etc)
- Try parsing the format of the input (normal text, json, etc) and send correctly formatted data with fuzzed fields.
- Try manipulating the sample input (bit flips, number replacement, etc)
- For the check-in, we will only test your fuzzer against two binaries (csv1, json1).
'''