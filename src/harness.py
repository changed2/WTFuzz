from magic import from_file
import threading
from exploit_detection import crash_log
import os
from QEMUCoverage import QEMUCoverage

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Harness():
    strategy = None
    _crash_logged = False  # Class-level flag
    _crash_lock = threading.Lock()  # Class-level lock
    
    def __init__(self, input_file):
        file_type = from_file(input_file)
        if "CSV" in file_type:
            print(f"{bcolors.OKGREEN}Switching to CSV mutator{bcolors.ENDC}")
            self.strategy = "CSV"
        elif "JSON" in file_type:
            print(f"{bcolors.OKGREEN}Switching to JSON mutator{bcolors.ENDC}")
            self.strategy = "JSON"
        elif "JPEG" in file_type:
            print(f"{bcolors.OKGREEN}Switching to JPEG mutator{bcolors.ENDC}")
            self.strategy = "JPEG"
        else:
            print(f"{bcolors.OKGREEN}No matching strategy found, defaulting to plaintext{bcolors.ENDC}")
            self.strategy = "TEXT"
            
    def run_retrieve(self, binary, input_data):
        qemu_coverage = QEMUCoverage()
        result = qemu_coverage.get_coverage(binary, input_data)

        if result['errors']:
            # Use the lock to check and set crash logged status
            with self._crash_lock:
                if not self._crash_logged:
                    self._crash_logged = True
                    filename = os.path.basename(binary)
                    crash_log(
                        result['returncode'],
                        result['errors'].decode().strip(),
                        input_data,
                        result['output'].decode().strip(),
                        filename
                    )

        return result

    @classmethod
    # Reset the crash logged state when starting with a new binary
    def reset_crash_state(cls):
        cls._crash_logged = False
