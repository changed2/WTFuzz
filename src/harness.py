from magic import from_file
import subprocess
from exploit_detection import crash_log
import os

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
            
    def run_retrieve(self, binary, input):        
        process = subprocess.Popen([binary], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate(input=input.encode())
        
        if errors:
            filename = os.path.basename(binary)
            crash_log(process.returncode, errors.decode().strip(), 
                    input, output.decode().strip(), filename)