import os
import json
from collections import UserList, UserDict
import subprocess
from pwn import *

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


def mutate(json_input: bytes):
    json_obj = json.loads(json_input)

    if "input" in json_obj:
        json_obj["len"] = len(json_obj["input"])

    obj = JsonObject(json_obj)

    mutated_inputs = []

    '''i think the buffer overflow is just the first key'''
    mutated_inputs.append(json.dumps({}))


    for key in list(json_obj.keys()):
        if key == "len":
            # difference greater than 30 between input length and length in json
            #mutated_inputs.append(json.dumps(obj.replace("len", 42).properties))
            mutated_inputs.append(json.dumps(obj.replace("len", 500).properties))
            mutated_inputs.append(json.dumps(obj.replace("len", -1).properties))
            mutated_inputs.append(json.dumps(obj.replace("len", None).properties))

        if key == "input":
            # buffer overflow case
            buffer_overflow = cyclic(10024).decode()
            mutated = obj.replace(key, buffer_overflow)
            mutated2 = mutated.replace("len", len(buffer_overflow))
            mutated_inputs.append(json.dumps(mutated2.properties))

            # null case
            mutated = obj.replace(key, None)
            mutated2 = mutated.replace("len", 0)
            mutated_inputs.append(json.dumps(mutated2.properties))

            # remove key case
            mutated = obj.remove(key)
            mutated2 = mutated.replace("len", 0)
            mutated_inputs.append(json.dumps(mutated2.properties))

            # binary data case
            binary_string = b'\xFF\x00'.hex()
            mutated = obj.replace(key, binary_string)
            mutated2 = mutated.replace("len", len(binary_string))
            mutated_inputs.append(json.dumps(mutated2.properties))

        if key == "more_data" and isinstance(json_obj["more_data"], list):
            # empty array case
            mutated = obj.replace(key, [])
            mutated_inputs.append(json.dumps(mutated.properties))

            # replace each value in array with null case
            for i in range(len(json_obj["more_data"])):
                mutated_array_replace = obj.replace_in_array("more_data", i, None)
                mutated_inputs.append(json.dumps(mutated_array_replace.properties))

            # null array case
            mutated = obj.replace(key, None)
            mutated_inputs.append(json.dumps(mutated.properties))

            # append normal value to array case
            mutated = obj.append_in_array("more_data", "aa")
            mutated_inputs.append(json.dumps(mutated.properties))

            # append null to array case
            mutated = obj.append_in_array("more_data", None)
            mutated_inputs.append(json.dumps(mutated.properties))

            # large list case
            large_array = ["element" + str(i) for i in range(124)]
            json_obj_with_large_array = obj.replace("more_data", large_array)
            mutated_inputs.append(json.dumps(json_obj_with_large_array.properties))

    return mutated_inputs


def mutate_json(json_input_file, binary_file, harness):
    sample_json = format_input(json_input_file)
    mutated_input = mutate(sample_json)

    for i in mutated_input:
        fuzzed_data = ''.join(i)
        harness.run_retrieve(binary_file, fuzzed_data)
