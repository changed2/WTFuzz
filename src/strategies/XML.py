import os
import xml.etree.ElementTree as ET
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion


def format_input(input_file):
    with open(input_file, "r") as f:
        return f.read()

def mutate_string(data):
    mutations = [
        buffer_overflow(data.encode()).decode(errors='ignore'),
        bit_flip(data.encode()).decode(errors='ignore'),
        byte_flip(data.encode()).decode(errors='ignore')
    ]
    return mutations

def mutate_integer(data):
    mutated_integers = []
    for mutated_data in known_integer_insertion(data.to_bytes(4, 'little')):
        mutated_integers.append(int.from_bytes(mutated_data, 'little', signed=True))
    return mutated_integers

def mutate_element_text(element):
    if element.text:
        return mutate_string(element.text)
    return []

def mutate_attributes(element):
    mutated_elements = []
    for attr, value in element.attrib.items():
        if isinstance(value, str):
            for mutated_value in mutate_string(value):
                temp_element = ET.Element(element.tag, element.attrib)
                temp_element.text = element.text
                temp_element.attrib[attr] = mutated_value
                mutated_elements.append(temp_element)
    return mutated_elements

def mutate_xml_elements(root):
    mutated_xml_strings = []
    
    for element in root.iter():
        for mutated_text in mutate_element_text(element):
            temp_tree = ET.ElementTree(root)
            temp_element = temp_tree.find(element.tag)
            temp_element.text = mutated_text
            mutated_xml_strings.append(ET.tostring(temp_tree.getroot()).decode())

        for mutated_element in mutate_attributes(element):
            temp_tree = ET.ElementTree(root)
            temp_tree.find(element.tag).attrib = mutated_element.attrib
            mutated_xml_strings.append(ET.tostring(temp_tree.getroot()).decode())
    
    return mutated_xml_strings

def mutate(xml_input: str) -> list:
    root = ET.fromstring(xml_input)
    mutated_inputs = mutate_xml_elements(root)
    return mutated_inputs

def mutate_xml(xml_input_file, binary_file, harness):
    sample_xml = format_input(xml_input_file)
    mutated_inputs = mutate(sample_xml)

    for i in mutated_inputs:
        res = harness.run_retrieve(binary_file, i)
        if res:
            break