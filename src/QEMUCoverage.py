import subprocess
import os
import re
import tempfile

class QEMUCoverage:
    def _parse_trace_log(self, trace_file_location):
        blocks = set()
        try:
            with open(trace_file_location, 'r') as f:
                trace_pattern = re.compile(r"Trace [0-9]+: (0x\w+) ", re.I)
                
                for line in f:
                    if 'Trace' not in line:
                        continue
                    
                    match = trace_pattern.search(line)
                    if match:
                        addr = int(match.group(1), 16)
                        blocks.add(addr)
        except FileNotFoundError:
            print("Warning: QEMU trace log not found")
        return blocks

    def get_coverage(self, binary, input):
        trace_file = tempfile.NamedTemporaryFile(delete=False)
        trace_file_location = trace_file.name
        trace_file.close()
        
        try:
            process = subprocess.Popen(
                ["qemu-x86_64", "-d", "exec", "-D", trace_file_location, binary],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, errors = process.communicate(input=input.encode())
            
            # Get coverage from this run
            blocks = self._parse_trace_log(trace_file_location)

            return {
                'blocks': blocks,
                'output': output,
                'errors': errors,
                'returncode': process.returncode
            }
            
        finally:
            # Remove tracefile after each run to reduce its size.
            if os.path.exists(trace_file_location):
                os.remove(trace_file_location)