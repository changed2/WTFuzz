#!/usr/bin/env python3

import random
import sys
from harness import Harness
from exploit_detection import crash_log
from strategies.CSV import *
from strategies.JSON import *
import os 
import glob

def random_input(max_length: int = 100, char_start: int = 32, char_range: int = 32) -> str:
    out = ""
    string_length = random.randrange(0, max_length + 1)
    for _ in range(0, string_length):
        out += chr(random.randrange(char_start, char_start + char_range))
    return out

if __name__ == "__main__":
    if not os.path.isdir("../binaries"):
        print("Unable to find binaries directory")
        
    if not os.path.isdir("../example_inputs"):
        print("Unable to find binaries directory")
        
    for binary in glob.glob("../binaries/*"):
        filename = os.path.basename(binary)
        input_file = f"../example_inputs/{filename}.txt"
        harness = Harness(input_file)  # Create an instance

        match harness.strategy:
            case "CSV":
                mutate_csv(input_file, binary, harness)
            case "JSON":
                mutate_json(input_file, binary, harness)
            case _:
                print(f"Unknown input file type: {harness.strategy}")
