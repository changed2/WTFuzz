### **COMP6447 Final Submission \- WTFuzz**

Authors: Wayne (z5425577), Koushik (z5421830), Edison (z5358446), Akanksha (z5421482)

### **Fuzzer functionality**

#### Different mutation strategies used

Currently, our fuzzer supports two main fuzzing strategies, JSON and CSV.  
For CSV, our fuzzer attempts seven different mutation strategies that are repeated multiple times (default: 10):

* String corruption: the fuzzer appends a randomly generated string to randomly selected values from the sample input  
* Replacing numeric values with their negatives: the fuzzer replaces numeric values in the sample input with their negative counterparts  
* Increasing field sizes: randomly generated number of rows and columns are added to the sample input  
* Insertion of special characters: the fuzzer inserts special characters (non-ASCII) into random positions within the CSV file  
* Extra comma insertion: the fuzzer inserts extra commas into the file to exploit field misalignments   
* Extra numeric values: the fuzzer inserts extremely high and low numeric values   
* Simulated end-of-file (EOF): the fuzzer simulates an end-of-file scenario by clearing all the data provided

For JSON, our fuzzer attempts various mutation strategies:

* Buffer overflow in different keys: This strategy tests if the program crashes when receiving a large value or a large input. For the input, a cyclic string is used so that gdb can be attached and we can see which values are in the registers to figure out the offset.  
* Null value: In this strategy, each key is tested with null values to see if the program breaks  
* Removing keys: In this strategy, the “input” key is removed and “len” is set to 0 to see if the program would crash  
* Changing list values: For this strategy, if a JSON input contains a list as one of the values for the keys, it will have iterations for each element in the array being replaced with null, and also null/unexpected value will be appended to the array to see if the program will crash  
* Large list case: This strategy tests a large list to see if the program will crash based on the list size

For JPEG, our fuzzer attempts various strategies:

* Extend SOF: increase the length of the SOF segment randomly and insert random bytes  
* Corrupt DQT: manipulate the  Define Quantization Table (DQT)  segment by injecting random values  
* Shuffle segments: rearrange JPEG segments (e.g. DQT, DHT, and SOF) randomly  
* Corrupt Huffman tables: apply random bitwise operations to the Define Huffman Table segment  
* Corrupt SOI and EOI: modify the start of image (SOI) and end of image (EOI) markers  
* Remove random segment: delete segments like APP0 or the Start of Scan (SOS)  
* Insert zero-length segments: insert segments with a length of zero at various points 

For XML, our fuzzer attempts various strategies:

* Buffer overflow in tags, attributes or text fields  
* Known integers in attributes or text fields  
* Duplicate tags/Tag overflow  
* Format string in tags, attributes or text fields  
* Byte and bit flip in attributes or text fields

#### How the harness works

Our `harness.py` file runs the fuzzed input through the targeted binary and detects any crashes or errors. The run\_retrieve function is called by the fuzzer after it selects the appropriate strategy for the given binary. `run_retrieve` runs the program via QEMU to enable coverage and passes the coverage results back to the fuzzer, which determines whether to continue mutations or print out the crash summary based on these results.

#### Fuzzer capabilities

Expanding on from our midpoint submission, our fuzzer currently supports the following file types:

* Plaintext  
* JSON  
* CSV  
* JPEG  
* XML

Once the binary crashes, the program output and error messages are fed to the result generator, which summarises the program behaviour for the user via stdout and writes the successful payload to the appropriate text file for analysis. The summary provides the crash type, detected vulnerability, crash cause, and payload size.

#### Code Coverage

The harness now integrates `QEMU` to enable code coverage. By running the binary in qemu’s emulation mode, we can use the generated trace file to track the number of basic block addresses called. For each mutation round, the fuzzer uses that to determine the current “best payload”, which forms the baseline for future mutations until a crash is detected. This however comes at the cost of speed as emulation is slower than using the native subprocess to run the binary. To account for this we implemented multi-threading detailed below.

### **Bugs Identified by the Fuzzer**

Our fuzzer is now capable of finding:

* Buffer overflows (with/without stack canary)  
* Format strings via memory leaks, and  
* Integer/arithmetic errors

### **Something Awesome**

#### Multi-Threading

Our implementation of multi-threading for the fuzzer has significantly reduced the time taken to detect vulnerabilities compared to using a single thread. We use 4 threads that initially start with the example input with each then randomly choosing their mutation method. If we don’t detect a crash/vulnerability we base further rounds on the payload which gave the most coverage previously.

These rounds are based on an 8-second timeout such that we assume if a vulnerability is not detected we’re likely exploring an incorrect branch without a vulnerability so we reset the payload and start again. To this end, if after 60 seconds no vulnerability has been found it is automatically skipped and the next binary in the queue is fuzzed.

### **Further Improvements**

**Expanded Mutation Strategies**  
The current implementation does not support all of the required strategies and file types. An improvement to be made is implementing further ways of fuzzing input to identify bugs. This would come in the form of expanded strategies, namely:

* PDF, and  
* ELF.

**Coverage Improvements**  
The coverage detection mechanism currently is very rudimentary and has not been optimised for efficiency. One improvement is to incorporate some of the optimisations that AFL uses in for QEMU so that it can run faster.

**XML Tag mutations**  
Since the tag manipulations easily cause parsing errors, we were unable to find a way to efficiently perform mutations on the tags the same way we could on the attributes or text fields. Improvements would be finding more ways to mutate tags. 