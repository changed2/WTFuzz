#!/usr/bin/env python3

import csv
import random
from queue import Queue

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

# Convert back to csv from list
def list_to_csv(list):
    csv_string = ""
    for row in list:
        row_string = [str(item) for item in row]
        csv_row = ",".join(row_string)
        csv_string += csv_row + "\n"
    return csv_string

# main function: csv fuzzer
def mutate_csv(csv_data, fuzzed_data, binary_file, output_from_binary):
    # Mutation strategies
    csv_mutator = [append_characters, replace_with_negatives]
    
    # Convert binary data to lists
    csv_data = csv_to_list_of_list(csv_data)
    
    # Apply each mutator function to the csv_data once
    for mutator in csv_mutator:
        csv_data = mutator(csv_data)  # apply mutation
    
    fuzzed_data = list_to_csv(csv_data)
    
    # TO DO: run data through binary
    process_output = ""
    
    output_from_binary.put(process_output)
    
    return fuzzed_data
        