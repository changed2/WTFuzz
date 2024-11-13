import subprocess
import os
import re
from collections import defaultdict

################################################################################
#### Initial Basic implementation of QEMU-based code-coverage ######
"""
    Features:
        1. Runs binary using qemu rather than native subprocess to enable tracing via emulation.
        2. Generates coverage based on number of basic blocks logged in trace_file
            a. Needs to account for ASLR as right now every new run will generate new coverage even if the exact
               same addresses are being hit due to ASLR.
        3. Added stub for updating 'best input' which we can use to create further mutations of if the payload
            generates more coverage (coverage-based mutations)
    
    Assumptions:
        1. The binary will be run multiple times until a crash is generated
        2. Each iteration generates a new input either from scratch or using a previous payload as the base for mutations.
"""
################################################################################

class QEMUCoverage:
    def __init__(self):
        self.coverage_map = defaultdict(int)
        self.baseline_coverage = set()
        self.trace_file_location = "/tmp/qemu_trace.log"

    def _parse_trace_log(self):
        # extract basic block coverage.
        # For now gets all blocks covered by the input, will need to re-do this to account for unique addresses/blocks...
        blocks = set()
        try:
            with open(self.trace_file_location, 'r') as f:
                # for line in f:
                #     # Extract address from trace line
                #     addr = int(re.findall(r"0x[0-9A-F]+", str(line), re.I)[0],16)
                #     blocks.add(addr)
                
                trace_pattern = re.compile(r"Trace [0-9]+: (0x\w+) ", re.I)
            
                for line in f:
                    if 'Trace' not in line:
                        continue
                        
                    match = trace_pattern.search(line)
                    if match:
                        addr = int(match.group(1), 16)
                        blocks.add(hex(addr))
        except FileNotFoundError:
            print("Warning: QEMU trace log not found")
        return blocks

    def get_coverage(self, binary, input):
        """Get coverage information for a single run."""
        try:
            process = subprocess.Popen(["qemu-x86_64", "-d", "exec", "-D", f"{self.trace_file_location}", f"{binary}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output, errors = process.communicate(input=input.encode())
            
            # Get coverage from this run
            blocks = self._parse_trace_log()

            for block in blocks:
                self.coverage_map[block] += 1
                
            return {
                'blocks': blocks,
                'new_blocks': blocks - self.baseline_coverage if self.baseline_coverage else blocks,
                'output': output,
                'errors': errors,
                'returncode': process.returncode
            }
            
        finally:
            # Remove tracefile after each run to reduce its size.
            if os.path.exists(self.trace_file_location):
                os.remove(self.trace_file_location)

    def set_baseline(self, blocks):
        """Set baseline coverage for comparison."""
        self.baseline_coverage = blocks