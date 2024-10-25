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
import csv
import random
# Read csv file contents
def read_csv(input_file):
    data = []
    with open(input_file, mode = 'r') as input:
        csv_reader = csv.reader(input)
        for row in csv_reader:
            data.append(row)
    return data

# take csv, split by lines, split by commas
def csv_to_list_of_list(csv_string):
    lines = csv_string.split("\n")
    list_of_list = [line.split(",") for line in lines]
    return list_of_list

# MUTATION METHODS
def append_characters(list, mutation_count = 10):
    # size of csv data
    num_rows = len(list)
    # first list represents no of items in column
    num_cols = len(list[0])

    # repeate mutation 10 times
    for _ in range(mutation_count):
        # select random row
        row = random.randint(0, num_rows - 1)
        # select random col
        col = random.randint(0, num_cols - 1)

        # get item from randomly selected row and col
        list[row][col] = str(list[row][col]) + 'random'

    return list

# Strategy 2: replace numbers with negatives
def replace_with_negatives(list, mutation_count=10):
    num_rows = len(list)
    num_cols = len(list[0])
    for _ in range(mutation_count):
        # get a random row and col
        row = random.randint(0, num_rows - 1)
        col = random.randint(0, num_cols - 1)
        # check if value is numeric
        if isinstance(list[row][col], (int, float)):
            # replace
            list[row][col] = -abs(list[row][col])
    return list