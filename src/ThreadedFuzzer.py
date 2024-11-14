#!/usr/bin/env python3
import random
import sys
from harness import Harness
from exploit_detection import crash_log
from strategies.CSV import *
import os 
import glob
import csv
import threading
import time
from queue import Queue
from typing import List, Optional
import concurrent.futures

class ThreadedFuzzer:
    def __init__(self, num_workers: int = 4, timeout: int = 60):
        self.num_workers = num_workers
        self.timeout = timeout
        self.best_coverage = 0
        self.best_input = None
        self.crash_detected = threading.Event()
        self.lock = threading.Lock()
        self.print_lock = threading.Lock()  # Add lock for printing
        self.trace_lock = threading.Lock()  # Add lock for trace file operations
        
    def safe_print(self, *args, **kwargs):
        """Thread-safe printing"""
        with self.print_lock:
            print(*args, **kwargs)
            sys.stdout.flush()  # Ensure output is flushed

    def worker_task(self, binary: str, harness: Harness, base_input: List[List[str]]) -> dict:
        """Individual worker task that fuzzes input and checks for crashes"""
        try:
            if self.crash_detected.is_set():
                return {"status": "stopped", "message": "Crash detected in another thread"}

            # Generate mutated input
            fuzzed_data = mutate_csv(base_input)
            
            # Run the binary with mutated input using trace file lock
            with self.trace_lock:
                result = harness.run_retrieve(binary, fuzzed_data)
            
            if harness.crash_detected:
                self.crash_detected.set()
                return {
                    "status": "crash",
                    "message": "Crash detected and logged"
                }
                
            if result:  # better coverage found
                return {
                    "status": "success",
                    "coverage": harness.best_coverage,
                    "input": harness.get_best_input()
                }
                
            return {
                "status": "success",
                "coverage": 0,
                "input": None
            }
            
        except Exception as e:
            self.crash_detected.set()
            return {"status": "error", "error": str(e)}

    def fuzz_binary(self, binary: str, input_file: str) -> None:
        """Fuzzes a single binary using ThreadPoolExecutor"""
        self.safe_print(f"\nFuzzing binary: {os.path.basename(binary)}")
        
        self.crash_detected.clear()
        
        # Read initial input
        with open(input_file, mode='r') as f:
            csv_reader = csv.reader(f)
            base_input = [row for row in csv_reader]
        
        # Create harness and establish baseline
        harness = Harness(input_file)
        with self.trace_lock:
            harness.establish_baseline(binary, base_input)
        
        self.best_coverage = harness.best_coverage
        self.best_input = base_input
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            while (time.time() - start_time) < self.timeout and not self.crash_detected.is_set():
                # Submit batch of tasks
                futures = [
                    executor.submit(self.worker_task, binary, harness, self.best_input)
                    for _ in range(self.num_workers)
                ]
                
                # Process completed tasks
                try:
                    for future in concurrent.futures.as_completed(futures):
                        try:
                            result = future.result()
                            
                            if result["status"] == "crash" or result["status"] == "error":
                                self.safe_print(f"Worker detected crash or error: {result.get('message', result.get('error', 'Unknown error'))}")
                                executor.shutdown(wait=False)
                                return
                                
                            if result["status"] == "stopped":
                                continue
                            
                            # Update best coverage if better found
                            if result.get("coverage", 0) > self.best_coverage:
                                with self.lock:
                                    if result["coverage"] > self.best_coverage:
                                        self.best_coverage = result["coverage"]
                                        self.best_input = result["input"]
                                        self.safe_print(f"New best coverage found: {self.best_coverage}")
                                        
                        except Exception as e:
                            self.safe_print(f"Worker generated an exception: {str(e)}")
                            self.crash_detected.set()
                            executor.shutdown(wait=False)
                            return
                            
                except concurrent.futures.TimeoutError:
                    continue
        
        if self.crash_detected.is_set():
            self.safe_print(f"Fuzzing stopped due to crash in {os.path.basename(binary)}")
        else:
            self.safe_print(f"Finished fuzzing {os.path.basename(binary)}")
            self.safe_print(f"Best coverage achieved: {self.best_coverage}")

    def fuzz_all_binaries(self, binaries_dir: str, inputs_dir: str) -> None:
        """Fuzzes all CSV binaries in the given directory"""
        if not os.path.isdir(binaries_dir):
            self.safe_print("Unable to find binaries directory")
            return
            
        if not os.path.isdir(inputs_dir):
            self.safe_print("Unable to find example_inputs directory")
            return
            
        for binary in glob.glob(f"{binaries_dir}/*"):
            filename = os.path.basename(binary)
            input_file = f"{inputs_dir}/{filename}.txt"
            
            if not os.path.exists(input_file):
                continue
                
            harness = Harness(input_file)
            if harness.strategy != "CSV":
                continue
            
            self.fuzz_binary(binary, input_file)

if __name__ == "__main__":
    fuzzer = ThreadedFuzzer(num_workers=4, timeout=60)
    fuzzer.fuzz_all_binaries("../binaries", "../example_inputs")