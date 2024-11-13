#!/usr/bin/env python3

import csv
from mutators.negative_number_replacement import replace_numbers_with_negatives
from mutators.random_character_append import append_random_characters
from mutators.row_column_addition import add_rows_and_columns

from collections import UserList

class CSVObject(UserList):
    def __init__(self, data=None):
        super().__init__(data or [])

# Read csv file contents
def read_csv(input_file):
    data = []
    with open(input_file, mode='r') as input:
        csv_reader = csv.reader(input)
        for row in csv_reader:
            data.append(row)
    return CSVObject(data)

# Convert back to csv from list
def list_to_csv(csv_object):
    csv_string = ""
    for row in csv_object:
        row_string = [str(item) for item in row]
        csv_row = ",".join(row_string)
        csv_string += csv_row + "\n"
    return csv_string

# main function: csv fuzzer
def mutate_csv(csv_input_file, binary_file, harness):
    csv_object = read_csv(csv_input_file)

    mutations = [
        append_random_characters,
        replace_numbers_with_negatives,
        add_rows_and_columns
    ]

    for mutation in mutations:
        mutation(csv_object.data) 
        fuzzed_data = list_to_csv(csv_object)
        harness.run_retrieve(binary_file, fuzzed_data)
        csv_object.data = read_csv(csv_input_file).data