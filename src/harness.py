from magic import from_file
import subprocess
from exploit_detection import crash_log
import os
from QEMUCoverage import QEMUCoverage
from typing import List, Optional
import csv
import io

def csv_to_string(csv_data: List[List[str]]) -> str:
    """Convert CSV data (list of lists) back to string format"""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerows(csv_data)
    return output.getvalue()

class Harness():
    def __init__(self, input_file):
        self.strategy = None
        self.crash_detected = False
        self.qemu_coverage = QEMUCoverage()
        self.best_coverage = 0
        self.best_input = None
        
        file_type = from_file(input_file)
        if "CSV" in file_type:
            print("Switching to CSV mutator")
            self.strategy = "CSV"
        elif "JSON" in file_type:
            print("Switching to JSON mutator")
            self.strategy = "JSON"
        elif "JPEG" in file_type:
            print("Switching to JPEG mutator")
            self.strategy = "JPEG"
        else:
            print("No matching strategy found, defaulting to plaintext")
            self.strategy = "TEXT"
            
    def run_retrieve(self, binary, input):        
        result = self.qemu_coverage.get_coverage(binary, input)
        
        # Check for crashes
        if result['errors']:
            filename = os.path.basename(binary)
            crash_log(
                result['returncode'],
                result['errors'].decode().strip(),
                input,
                result['output'].decode().strip(),
                filename
            )
            self.crash_detected = True  # Set crash flag
            return False
        
        # Update best coverage if we found new blocks
        current_coverage = len(result['blocks'])
        if current_coverage > self.best_coverage:
            self.best_coverage = current_coverage
            self.best_input = input
            print(f"New best coverage found: {current_coverage} blocks")
            return True
            
        return False
    
    def establish_baseline(self, binary, input_data):
        if (self.strategy == 'CSV'):
            input_data = csv_to_string(input_data)
        result = self.qemu_coverage.get_coverage(binary, input_data)
        self.qemu_coverage.set_baseline(result['blocks'])
        self.best_coverage = len(result['blocks'])
        self.best_input = input_data
        
    def get_best_input(self):
        return self.best_input