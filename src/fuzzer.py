#!/usr/bin/env python3

import random
import sys
from harness import Harness
from exploit_detection import crash_log
from strategies.CSV import *
from strategies.JSON import *
from strategies.JPEG import *
import os 
import glob
import csv

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
        print("Unable to find example_inputs directory")
        
    for binary in glob.glob("../binaries/*"):    
        filename = os.path.basename(binary)
        # if filename != "json1":
        #     continue
        
        input_file = f"../example_inputs/{filename}.txt"
        harness = Harness(input_file)  # Create an instance

        input_data = null
        if harness.strategy == "CSV":
            with open(input_file, mode='r') as input_file:
                csv_reader = csv.reader(input_file)
                input_data = [row for row in csv_reader]
        elif harness.strategy != "JPEG":
            with open(input_file, mode='r') as input_file:
                input_data = input_file.read()

        match harness.strategy:
            case "CSV":
                fuzzed_data = mutate_csv(input_data, binary, harness)
                harness.run_retrieve(binary, fuzzed_data)
            case "JSON":
                continue
                mutate_json(input_file, binary, harness)
            case "JPEG":
                continue
                mutate_jpeg(input_file, binary, harness)
            case _:
                print(f"Unknown input file type: {harness.strategy}")
