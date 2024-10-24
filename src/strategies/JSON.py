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
    
def format_input():
    with open("json_input/input.txt", "r") as f:
        sample_input = f.read()
        return sample_input

def mutate(json_input: bytes):
    json_obj = json.loads(json_input)
    
    if "input" in json_obj:
        json_obj["len"] = len(json_obj["input"])
    
    obj = JsonObject(json_obj)
    
    with open("json_input/mutated_input.txt", "w") as f:
        for key in list(json_obj.keys()):
            if key == "input":
                # buffer overflow case
                buffer_overflow = "A" * 99999999
                mutated = obj.replace(key, buffer_overflow)
                f.write(json.dumps(mutated.properties) + "\n")
    
                # null case
                mutated = obj.replace(key, None)
                f.write(json.dumps(mutated.properties) + "\n")
                
                # remove key case
                mutated = obj.remove(key)
                f.write(json.dumps(mutated.properties) + "\n")
    
                # binary data case
                mutated = obj.replace(key, b'\xFF\x00'.hex())
                f.write(json.dumps(mutated.properties) + "\n")

            if key == "more_data" and isinstance(json_obj["more_data"], list):
                # empty array case
                mutated = obj.replace(key, [])
                f.write(json.dumps(mutated.properties) + "\n")
                
                # replace each value in array with null case
                for i in range(len(json_obj["more_data"])):
                    mutated_array_replace = obj.replace_in_array("more_data", i, None)
                    f.write(json.dumps(mutated_array_replace.properties) + "\n")
                
                # null array case
                mutated = obj.replace(key, None)
                f.write(json.dumps(mutated.properties) + "\n")
                
                # append normal value to array case
                mutated = obj.append_in_array("more_data", "aa")
                f.write(json.dumps(mutated.properties) + "\n")
                
                # append null to array case
                mutated = obj.append_in_array("more_data", None)
                f.write(json.dumps(mutated.properties) + "\n")
                
                # large list case
                large_array = ["element" + str(i) for i in range(5555)]
                json_obj_with_large_array = obj.replace("more_data", large_array)
                f.write(json.dumps(json_obj_with_large_array.properties) + "\n")
                
                
                
                
    '''
        for key in list(json_obj.keys()):
            if key == "len":
                continue
            mutated_replace_1 = obj.replace(key, 1)
            f.write(json.dumps(mutated_replace_1.properties) + "\n")

            mutated_replace_null = obj.replace(key, None)
            f.write(json.dumps(mutated_replace_null.properties) + "\n")
            
            mutated_remove = obj.remove(key)
            f.write(json.dumps(mutated_remove.properties) + "\n")
            
        for key, value in list(json_obj.items()):
            if key == "len":
                continue
            mutated_replace_1 = obj.replace(key, 1)
            f.write(json.dumps(mutated_replace_1.properties) + "\n")

            mutated_replace_null = obj.replace(key, None)
            f.write(json.dumps(mutated_replace_null.properties) + "\n")
    '''
            
def test_mutated_inputs(binary_path, mutated_file):
# Read all the mutated inputs from the file
    with open(mutated_file, "r") as f:
        mutated_inputs = f.readlines()

# Iterate over each mutated input
    for i, json_input in enumerate(mutated_inputs):
        try:
            # Execute the binary and pass the JSON input
            result = subprocess.run(
                [binary_path],  # Path to the binary
                input=json_input,  # Pass the JSON input as bytes
                capture_output=True,  # Capture stdout and stderr
                text=True  # Return output as string instead of bytes
            )

            # Print the result of the execution
            print(f"Test {i + 1}:")
            print(f"Input: {json_input.strip()}")
            print(f"Output: {result.stdout.strip()}")
            print(f"Error: {result.stderr.strip()}" if result.stderr else "No Errors")
            print("-" * 50)

        except Exception as e:
            print(f"Error during test {i + 1}: {e}")
                
if __name__ == "__main__":
    sample_json = format_input()
    mutate(sample_json)
    
    binary_path = "json_input/json1"
    mutated_file = "json_input/mutated_input.txt"
    test_mutated_inputs(binary_path, mutated_file)
    #p = process("json_input/json1")
    
    #p.interactive()
