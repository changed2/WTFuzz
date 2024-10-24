#!/usr/bin/env python3

import os
import subprocess
import random
import sys
from harness import Harness
from exploit_detection import crash_log

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
        
    program = sys.argv[1]
    input_file = sys.argv[2]
    
    harness_instance = Harness(input_file)  # Create an instance
    # print(harness_instance.strategy)  # Access the instance's strategy

    generated_input = random_input()
    with open(input_file, "w") as f:
        f.write(generated_input)
        # TODO: file mutation strategy - Case/If statments
        
    with open(input_file, "r") as input_file:
        process = subprocess.Popen([program], stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()
        
    # print(f"PROGRAM OUTPUT: {output.decode().strip()}")
    
    if errors:
        crash_log(process.returncode, errors.decode().strip(), 
                  generated_input, output.decode().strip())

'''
Tasks:
    AKANKSHA
    - CSV mutation 
    
    EDISON
    - JSON mutation

    Mutation types:
        - Buffer overflow
        - Random input
        - No format strings?
    
    KOUSHIK
    - Exploit detection summarisation (retrieve output from binary)
        - Display what crashes occured, how it occured, why it occured
        - Put into resulting file
    
    WAYNE
    - Connecting everything
    - Refactoring and Feature creation
        - Splitting up to different files
        - Condensing code into functions
        - Classes etc
        
    Report Writing
    
    Future Features
    - Code coverage checker
'''