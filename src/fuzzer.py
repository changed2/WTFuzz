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
from concurrent.futures import ThreadPoolExecutor, as_completed

def fuzz_worker(strategy_func, binary, harness, current_input_data):
    try:
        mutated_input_data = strategy_func(current_input_data)
        result = harness.run_retrieve(binary, mutated_input_data)
        coverage = len(result['blocks'])

        print(f"{threading.current_thread().name} - Coverage: {coverage} blocks")

        return {
            'coverage': coverage,
            'mutated_input_data': mutated_input_data,
            'crash_detected': bool(result['errors'])
        }
    except Exception as e:
        print(f"Exception in Thread {threading.current_thread().name}: {e}")
        return {
            'coverage': 0,
            'mutated_input_data': current_input_data,
            'crash_detected': False
        }
    
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
        if filename != "csv1":
            continue
        
        input_file = f"../example_inputs/{filename}.txt"
        with open(input_file, 'r') as f:
            input_data = f.read()

        harness = Harness(input_file)
        strategy = harness.strategy

        strategy_functions = {
            'CSV': mutate_csv,
            'JSON': mutate_json,
            'JPEG': mutate_jpeg
        }

        strategy_func = strategy_functions.get(strategy)
        if strategy_func is None:
            print(f"Unknown strategy: {strategy}")
            continue

        best_input_data = input_data
        best_coverage = 0
        crashed = False

        # Baseline number of threads
        num_threads = 4 

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            while not crashed:
                futures = [
                    executor.submit(fuzz_worker, strategy_func, binary, harness, best_input_data)
                    for _ in range(num_threads)
                ]

                for future in as_completed(futures):
                    result = future.result()
                    if result['crash_detected']:
                        print("Crash detected! Fuzzing terminated.")
                        crashed = True
                        break
                    if result['coverage'] > best_coverage:
                        best_coverage = result['coverage']
                        best_input_data = result['mutated_input_data']
                        print(f"New best coverage: {best_coverage} blocks")

        print(f"Fuzzing finished for binary: {filename}")