#!/usr/bin/env python3

import random
import sys
from harness import Harness
from exploit_detection import crash_log
from strategies.CSV import *
from strategies.JSON import *

def random_input(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    out = ""
    string_length = random.randrange(0, max_length + 1)
    for _ in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <filename> <input_file>")
        exit(1)
        
    binary = sys.argv[1]
    input_file = sys.argv[2]
    
    harness = Harness(input_file)  # Create an instance
    match harness.strategy:
        case "CSV":
            mutate_csv(input_file, binary, harness)
        case "JSON":
            mutate_json(input_file, binary, harness)
        case _:
            print(f"Unknown input file type: {harness.strategy}")
            exit(1)