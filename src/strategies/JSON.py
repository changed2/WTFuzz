import os
import json
from collections import UserList, UserDict
from pwn import *
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion
from mutators.format_string import format_string_attack

def format_input(input_file):
    with open(input_file, "r") as f:
        sample_input = f.read()
        return sample_input
    

def add_key(mutated_json, mutated_inputs):
    # Define possible types of values to add
    value_options = [
        None,                                    
        random.randint(-1000, 1000),             
        ''.join(random.choices(string.ascii_letters, k=10)), 
        [random.randint(0, 5) for _ in range(3)], 
        {"nested_key": "nested_value"}            
    ]

    for value in value_options:
        temp_json = mutated_json.copy()
        random_key = ''.join(random.choices(string.ascii_letters, k=5))
        temp_json[random_key] = value
        mutated_inputs.append(json.dumps(temp_json).encode())

def mutate_string(data):
    mutations = [
        buffer_overflow().decode(errors='ignore'),
        bit_flip(data.encode()).decode(errors='ignore'),
        byte_flip(data.encode()).decode(errors='ignore'),
        format_string_attack().decode(errors='ignore')
    ]
    return mutations

def mutate_integer(data):
    mutated_integers = []
    # Iterate over each mutated bytearray from known_integer_insertion
    for mutated_data in known_integer_insertion(data.to_bytes(4, 'little')):
        # Convert the mutated bytearray back to an integer and add to the list
        mutated_integers.append(int.from_bytes(mutated_data, 'little', signed=True))
    return mutated_integers

# mutate individual elements in a list
def mutate_list_element(element):
    if isinstance(element, str):
        return mutate_string(element)
    elif isinstance(element, int):
        return mutate_integer(element)
    return []


def apply_mutations(key, value, mutated_json, mutated_inputs):

    if isinstance(key, str):
        for mutated_key in mutate_string(key):
            temp_json = mutated_json.copy()
            temp_json[mutated_key] = value
            mutated_inputs.append(json.dumps(temp_json).encode())

    if isinstance(value, str):
        for mutated_value in mutate_string(value):
            temp_json = mutated_json.copy()
            temp_json[key] = mutated_value
            mutated_inputs.append(json.dumps(temp_json).encode())

    if isinstance(key, int):
        for mutated_key in mutate_integer(key):
            temp_json = mutated_json.copy()
            temp_json[str(mutated_key)] = value
            mutated_inputs.append(json.dumps(temp_json).encode())

    if isinstance(value, int):
        for mutated_value in mutate_integer(value):
            temp_json = mutated_json.copy()
            temp_json[key] = mutated_value
            mutated_inputs.append(json.dumps(temp_json).encode())
            
    if isinstance(value, list):
        for index in range(len(value)):
            temp_json = mutated_json.copy()
            mutated_list = value.copy()
                
            # apply mutations to the list element at the current index
            for mutated_element in mutate_list_element(value[index]):
                mutated_list[index] = mutated_element
                temp_json[key] = mutated_list
                mutated_inputs.append(json.dumps(temp_json).encode())
            
    temp_json = mutated_json.copy()
    del temp_json[key]
    mutated_inputs.append(json.dumps(temp_json).encode())
    
    temp_json = mutated_json.copy()
    temp_json[key] = None
    mutated_inputs.append(json.dumps(temp_json).encode())
    

def mutate(json_input: bytes) -> bytearray:
    json_obj = json.loads(json_input)
    mutated_inputs = [b'{}']

    for key, value in json_obj.items():
        mutated_json = json_obj.copy()
        
        apply_mutations(key, value, mutated_json, mutated_inputs)

    add_key(json_obj, mutated_inputs)
    
    temp_json = mutated_json.copy()
    for _ in range(250):
        random_key = ''.join(random.choices(string.ascii_letters, k=5))
        temp_json[random_key] = random.randint(0, 100)
    mutated_inputs.append(json.dumps(temp_json).encode())

    return mutated_inputs

def print_mutated_inputs(mutated_inputs):
    for i, mutation in enumerate(mutated_inputs):
        # Decode the mutation (it's in byte format) and limit to 25 characters
        print(f"Mutation {i+1}: {mutation.decode()[:200]}")

def mutate_json(json_input_file, binary_file, harness):
    sample_json = format_input(json_input_file)
    mutated_input = mutate(sample_json)

    #print_mutated_inputs(mutated_input)
    for i in mutated_input:
        res = harness.run_retrieve(binary_file, i.decode())
        if res:
            break