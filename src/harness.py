from magic import from_file
import subprocess
from exploit_detection import crash_log
import os
from QEMUCoverage import QEMUCoverage

class Harness():
    strategy = None
    
    def __init__(self, input_file):
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
            
    def run_retrieve(self, binary, input_data):
        qemu_coverage = QEMUCoverage()
        result = qemu_coverage.get_coverage(binary, input_data)

        if result['errors']:
            filename = os.path.basename(binary)
            crash_log(
                result['returncode'],
                result['errors'].decode().strip(),
                input_data,
                result['output'].decode().strip(),
                filename
            )

        return result
    
    """Establish baseline coverage for initial input."""
    # Donno if this is necessary, but added stub anyway...
    def establish_baseline(self, binary, input_data):
        result = self.qemu_coverage.get_coverage(binary, input_data)
        self.qemu_coverage.set_baseline(result['blocks'])
        self.best_coverage = len(result['blocks'])
        self.best_input = input_data

    def get_best_input(self):
        return self.best_input
