#!/usr/bin/env python3

import time
import threading
from harness import Harness, bcolors
from exploit_detection import crash_log
from strategies.CSV import *
from strategies.JSON import *
from strategies.JPEG import *
import os 
import glob
from concurrent.futures import ThreadPoolExecutor, as_completed
import traceback

crash_event = threading.Event()
banner = f'''{bcolors.HEADER}
 __      ________________________                        
/  \    /  \__    ___/\_   _____/_ __________________ /\ 
\   \/\/   / |    |    |    __)|  |  \___   /\___   / \/ 
 \        /  |    |    |     \ |  |  //    /  /    /  /\ 
  \__/\  /   |____|    \___  / |____//_____ \/_____ \ )/ 
       \/                  \/              \/      \/    
{bcolors.ENDC}
'''

# Performs a fuzzing run using a given mutation strategy.
def fuzz_worker(strategy_func, binary, harness, current_input_data):
    try:
        if crash_event.is_set():
            return

        mutated_input_data = strategy_func(current_input_data)
        result = harness.run_retrieve(binary, mutated_input_data)
        coverage = len(result['blocks'])

        return {
            'coverage': coverage,
            'mutated_input_data': mutated_input_data,
            'crash_detected': bool(result['errors'])
        }
    except Exception as e:
        print(f"Exception in Thread {threading.current_thread().name}: {e}")
        traceback.print_exc()
        return {
            'coverage': 0,
            'mutated_input_data': current_input_data,
            'crash_detected': False
        }

if __name__ == "__main__":
    thread_timeout = 8  # Timeout in seconds for resetting to the original payload
    binary_timeout = 60
    
    if not os.path.isdir("../binaries"):
        print("Unable to find binaries directory")
        exit(1)
    if not os.path.isdir("../example_inputs"):
        print("Unable to find example_inputs directory")

    print(banner)

    for binary in glob.glob("../binaries/*"):
        filename = os.path.basename(binary)
        crash_event.clear()
        if filename != "json1" and filename != "json2" and filename != "csv1" and filename != "csv2":
            continue

        input_file = f"../example_inputs/{filename}.txt"
        with open(input_file, 'r') as f:
            input_data = f.read()

        Harness.reset_crash_state()
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
        num_threads = 4  # Number of threads to use

        # Timestamps for tracking reset intervals
        last_reset_time = time.time()
        starting_time = time.time()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            while not crashed:
                # Check if binary timeout has been exceeded
                if time.time() - starting_time >= binary_timeout:
                    print(f"{bcolors.FAIL}Binary time limit reached without crash. Skipping.{bcolors.ENDC}")
                    break
                
                # Check if round timeout has been exceeded
                if time.time() - last_reset_time >= thread_timeout:
                    print(f"{bcolors.WARNING}Timeout reached without crash. Resetting input.{bcolors.ENDC}")
                    best_input_data = input_data
                    last_reset_time = time.time()

                futures = [
                    executor.submit(fuzz_worker, strategy_func, binary, harness, best_input_data)
                    for _ in range(num_threads)
                ]

                for future in as_completed(futures):
                    result = future.result()
                    if result['crash_detected']:
                        print(f"Crash detected in {round(time.time() - starting_time, 2)} seconds!")
                        crash_event.set()
                        crashed = True
                        break

                    if result['coverage'] > best_coverage:
                        best_coverage = result['coverage']
                        best_input_data = result['mutated_input_data']
                        last_reset_time = time.time()  # Update reset time on finding new best coverage

        print(f"Fuzzing finished for binary: {filename}\n")