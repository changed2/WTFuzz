#!/usr/bin/env python3

import csv
import random
import re
from fuzzer import random_input
import copy 

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
def append_characters(list_of_lists, mutation_count = 10):
    list_of_lists_ = copy.deepcopy(list_of_lists)
    # size of csv data
    num_rows = len(list_of_lists_)
    # first list represents no of items in column
    num_cols = len(list_of_lists_[0])

    # repeat mutation 10 times
    for _ in range(mutation_count):
        # select random row
        row = random.randint(1, num_rows - 1)
        # select random col
        col = random.randint(0, num_cols - 1)

        # generate a random string to append using random_input
        random_str = random_input(100, ord('a'), 26)
        # get item from randomly selected row and col
        list_of_lists_[row][col] = str(list_of_lists_[row][col]) + random_str

    return list_of_lists_

# Strategy 2: replace numbers with negatives
def replace_with_negatives(csv_list, mutation_count=10):
    num_rows = len(csv_list)
    num_cols = len(csv_list[0])
    for _ in range(mutation_count):
        # get a random row and col
        row = random.randint(1, num_rows - 1)
        col = random.randint(0, num_cols - 1)

        # check if value is numeric
        if re.match(r"^[0-9]+(\.[0-9]+)?$", csv_list[row][col]):
            # replace
            csv_list[row][col] = "-" + csv_list[row][col]
    return csv_list

# Strategy 3: Add more rows and columns
def add_rows_and_cols(csv_list, mutation_count=10):
    num_rows = len(csv_list)
    num_cols = len(csv_list[0])

    # For each mutation, randomly add anywhere between 10-100 rows/cols.
    for _ in range(mutation_count):
        new_num_rows = random.randint(10, 100)
        new_num_cols = random.randint(10, 100)

        for _ in range(new_num_rows):
            new_row = [random.choice(csv_list[random.randint(0, num_rows - 1)]) for _ in range(num_cols)]
            csv_list.append(new_row)
            num_rows += 1
            
        for _ in range(new_num_cols):
            new_values = [random.choice(csv_list[random.randint(0, num_rows - 1)]) for _ in range(num_rows)]
            for i in range(num_rows):
                csv_list[i].append(new_values[i])
            num_cols += 1

    return csv_list

# Convert back to csv from list
def list_to_csv(list_of_lists):
    csv_string = ""
    for row in list_of_lists:
        row_string = [str(item) for item in row]
        csv_row = ",".join(row_string)
        csv_string += csv_row + "\n"
    return csv_string

# main function: csv fuzzer
def mutate_csv(csv_data, binary_file, harness):
    # Mutation strategies
    csv_mutator = [append_characters, replace_with_negatives, add_rows_and_cols]
    
    # Convert binary data to lists
    csv_data = read_csv(csv_data)
    # Apply each mutator function to the csv_data once
    for mutator in csv_mutator:
        fuzzed_data = list_to_csv(mutator(csv_data))
        # print(fuzzed_data)
        harness.run_retrieve(binary_file, fuzzed_data)
