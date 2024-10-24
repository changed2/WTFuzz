#!/usr/bin/env python3

# Format string vulnerabilities inside fields
# Buffer overflow vulnerabilities inside fields
# Bugs with missing or extra control characters
# Bugs parsing non-printable or ascii characters
# Bugs parsing large files
# Integer overflows
# Integer underflows

#  In fuzz_csv.c, the fuzzer initially runs 4 payloads that attempt the same techniques without any randomisation. These include some buffer overflow and format string attacks as well as swapping some values with known problematic input such as swapping 1 with -1, -999999, 0 etc. These functions run the same checks for each invocation so there is no added value in running them a second time on a binary. After this set of functions are executed the fuzzer progresses into an infinite loop which mutates the input in random ways in random locations. The loop will exit when a crash occurs. Some techniques include bit shifts (bit_shift_in_range), bit flips (bit_flip_in_range), increasing the number of cells (fuzz_populate_width), increasing the number of rows (fuzz_populate_length) and creating numerous empty cells (fuzz_empty_cells). These strategies continue to execute with different outputs due to varying execution based on a pseudo random number generator rand().

# Overflowing columns

# Overflowing lines
