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
        
        # Initialize QEMU coverage tracking
        self.qemu_coverage = QEMUCoverage()
        self.best_coverage = 0
        self.best_input = None
            
    def run_retrieve(self, binary, input):        
        # process = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # output, errors = process.communicate(input=input.encode())
        
        # if errors:
        #     filename = os.path.basename(binary)
        #     crash_log(process.returncode, errors.decode().strip(), 
        #             input, output.decode().strip(), filename)
        
        # CHECK QEMUCOVERAGE.py FOR INITIAL FEATURES IMPLEMENTED.
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
        
        # Update best coverage if we found new blocks
        # Very basic, needs more logic...
        current_coverage = len(result['blocks'])
        if current_coverage > self.best_coverage:
            self.best_coverage = current_coverage
            self.best_input = input
            print(f"New best coverage found: {current_coverage} blocks")
            return True  # Indicate that we found better coverage
            
        return False
    
    """Establish baseline coverage for initial input."""
    # Donno if this is necessary, but added stub anyway...
    def establish_baseline(self, binary, input_data):
        result = self.qemu_coverage.get_coverage(binary, input_data)
        self.qemu_coverage.set_baseline(result['blocks'])
        self.best_coverage = len(result['blocks'])
        self.best_input = input_data

    def get_best_input(self):
        return self.best_input
