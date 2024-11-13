import os
import json
from collections import UserList, UserDict
from pwn import *
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion

class JsonObject:
    def __init__(self, properties=None):
        self.properties = properties or {}

    def replace(self, key, value):
        new_properties = self.properties.copy()
        new_properties[key] = value
        return JsonObject(new_properties)

    def remove(self, key):
        if key in self.properties:
            new_properties = self.properties.copy()
            del new_properties[key]
            return JsonObject(new_properties)
        return self

    def replace_in_array(self, key, index, value):
        if key in self.properties and isinstance(self.properties[key], list):
            new_properties = self.properties.copy()
            array = new_properties[key].copy()
            if 0 <= index < len(array):
                array[index] = value
            else:
                array.append(value)
            new_properties[key] = array
            return JsonObject(new_properties)
        return self

    def append_in_array(self, key, value):
        if key in self.properties and isinstance(self.properties[key], list):
            new_properties = self.properties.copy()
            array = new_properties[key].copy()
            array.append(value)
            new_properties[key] = array
            return JsonObject(new_properties)
        return self

def format_input(input_file):
    with open(input_file, "r") as f:
        sample_input = f.read()
        return sample_input

def mutate_string(data):
    mutations = [
        buffer_overflow(data.encode()).decode(errors='ignore'),
        bit_flip(data.encode()).decode(errors='ignore'),
        byte_flip(data.encode()).decode(errors='ignore')
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

# mutate lists within the JSON object
def mutate_lists(json_obj):
    mutated_inputs = []
    
    for key, value in json_obj.items():
        if isinstance(value, list):
            # mutate each element in list
            for index in range(len(value)):
                mutated_json = json_obj.copy()
                mutated_list = value.copy()
                
                # apply mutations to the list element at the current index
                for mutated_element in mutate_list_element(value[index]):
                    mutated_list[index] = mutated_element
                    mutated_json[key] = mutated_list
                    mutated_inputs.append(json.dumps(mutated_json).encode())
    
    return mutated_inputs


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

def mutate(json_input: bytes) -> bytearray:
    json_obj = json.loads(json_input)
    mutated_inputs = []

    for key, value in json_obj.items():
        # create a copy of json_obj for each key-value pair to keep mutations independent
        mutated_json = json_obj.copy()
        
        mutated_inputs.extend(mutate_lists(json_obj))
        
        apply_mutations(key, value, mutated_json, mutated_inputs)

    return mutated_inputs


def mutate_json(json_input_file, binary_file, harness):
    sample_json = format_input(json_input_file)
    mutated_input = mutate(sample_json)

    for i in mutated_input:
        harness.run_retrieve(binary_file, i.decode())
