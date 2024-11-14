import os
import json
import random
import string
from collections import UserDict
from pwn import *
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion

class JSONObject(UserDict):
    def __init__(self, data=None):
        super().__init__(data or {})

def read_json(input_file):
    with open(input_file, "r") as f:
        data = json.load(f)
        return data

def helper_add_key(mutated_json):
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
        yield json.dumps(temp_json).encode()

def helper_string(data):
    mutations = [
        buffer_overflow(data.encode()).decode(errors='ignore'),
        bit_flip(data.encode()).decode(errors='ignore'),
        byte_flip(data.encode()).decode(errors='ignore')
    ]
    return mutations

def helper_integer(data):
    mutated_integers = []
    for mutated_data in known_integer_insertion(data.to_bytes(4, 'little')):
        mutated_integers.append(int.from_bytes(mutated_data, 'little', signed=True))
    return mutated_integers

def mutate_keys(key, value, mutated_json):
    if isinstance(key, str):
        for mutated_key in helper_string(key):
            temp_json = mutated_json.copy()
            temp_json[mutated_key] = value
            return json.dumps(temp_json).encode()

    elif isinstance(key, int):
        for mutated_key in helper_integer(key):
            temp_json = mutated_json.copy()
            temp_json[str(mutated_key)] = value
            return json.dumps(temp_json).encode()

def mutate_values(key, value, mutated_json):
    if isinstance(value, str):
        for mutated_value in helper_string(value):
            temp_json = mutated_json.copy()
            temp_json[key] = mutated_value
            return json.dumps(temp_json).encode()

    elif isinstance(value, int):
        for mutated_value in helper_integer(value):
            temp_json = mutated_json.copy()
            temp_json[key] = mutated_value
            return json.dumps(temp_json).encode()

    elif isinstance(value, list):
        for index in range(len(value)):
            temp_json = mutated_json.copy()
            mutated_list = value.copy()
            for mutated_element in helper_list_element(value[index]):
                mutated_list[index] = mutated_element
                temp_json[key] = mutated_list
                return json.dumps(temp_json).encode()

def remove_key(key, value, mutated_json):
    temp_json = mutated_json.copy()
    del temp_json[key]
    return json.dumps(temp_json).encode()

def null_key(key, value, mutated_json):
    temp_json = mutated_json.copy()
    temp_json[key] = None
    return json.dumps(temp_json).encode()

def add_keys(key, value, mutated_json):
    temp_json = mutated_json.copy()
    for _ in range(250):
        random_key = ''.join(random.choices(string.ascii_letters, k=5))
        temp_json[random_key] = random.randint(0, 100)
    return json.dumps(temp_json).encode()

def mutate_json(json_input_file, binary_file, harness):
    json_object = read_json(json_input_file)
    original_json = json_object.copy()

    json_mutations = [
        mutate_keys,
        mutate_values,
        remove_key,
        null_key,
        add_keys
    ]
    
    mutator = random.choice(json_mutations)
    key, value = random.choice(list(json_object.items()))
    fuzzed_data = mutator(key, value, original_json)
    print(fuzzed_data)
    return fuzzed_data
            