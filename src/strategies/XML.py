import os
import xml.etree.ElementTree as ET
import copy, random
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion, known_integer_insert
from mutators.format_string import format_string_attack
import xml.dom.minidom

'''
An XML format is comprised of 3 main things
1. tags
2. attributes
3. text

<html>
    <head>
        <link href="http://somewebsite.com" />
    </head>
    <body>
        <h1>I'm not a web developer.</h1>
    </body>
</html>

For example, in the above sample input, <html> is a tag
<... href="URL"> is the attribute and "I'm not a web developer" is text.

The idea is to iterate through each tag, attribute and text and apply mutations

To the attribute and text, it applies format string, known ints, buffer overflow, bit/byte flip

To the tags, since we need to consider malformed tags cause parsing issues, we only apply format string, known ints and buffer overflow

There is also a case for repeated tags since that is known to cause programs to crash
'''


def text_mutate(root, mutated_inputs):

    elements_with_text = [elem for elem in root.iter() if elem.text is not None]

    for elem in elements_with_text:
        original_text = elem.text

        # check if the element has children (to avoid creating invalid mixed content)
        if list(elem):
            continue
        
        # format string case
        elem.text = format_string_attack().decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        # testing for known integer case
        for known in known_integer_insert():
            elem.text = known.decode()
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)

        # buffer overflow case
        elem.text = buffer_overflow().decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        # byte flip case
        elem.text = byte_flip(bytearray(original_text, "utf-8")).decode(errors="ignore")
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        # bit flip case
        elem.text = bit_flip(bytearray(original_text, "utf-8")).decode(errors="ignore")
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)

        elem.text = original_text

    return mutated_inputs

def attr_mutate(root, mutated_inputs):

    for elem in root.iter():
        # collect all attributes of the element
        attributes = elem.attrib
        for attr_name, attr_value in attributes.items():
            original_value = attr_value

            elem.attrib[attr_name] = format_string_attack().decode()
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)
            
            for known in known_integer_insert():
                elem.attrib[attr_name] = known.decode()
                mutated_xml = ET.tostring(root, encoding="unicode")
                mutated_inputs.append(mutated_xml)

            elem.attrib[attr_name] = buffer_overflow().decode()
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)
            
            elem.attrib[attr_name] = byte_flip(bytearray(original_value, "utf-8")).decode(errors="ignore")
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)
            
            elem.attrib[attr_name] = bit_flip(bytearray(original_value, "utf-8")).decode(errors="ignore")
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)

            elem.attrib[attr_name] = original_value

    return mutated_inputs

def tag_mutate(root, mutated_inputs):
    for elem in root.iter():
        original_tag = elem.tag

        elem.tag = format_string_attack().decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        elem.tag = (b"B" * 200).decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        elem.tag = original_tag
        
    # case for creating repeated tags
    for i in range(len(root)):
        for _ in range(100):
            # deep copy the child element to avoid shared references
            root.append(copy.deepcopy(root[i]))
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)

        # restore the tree to the original state by removing appended elements
        for _ in range(100):
            root.remove(root[-1])
        
    return mutated_inputs

def mutate_xml(input_data):
    try:
        root = ET.fromstring(input_data)
    except ET.ParseError as e:
        return input_data
    
    mutated_inputs = []
    mutated_inputs.extend(tag_mutate(root, mutated_inputs))
    mutated_inputs.extend(attr_mutate(root, mutated_inputs))
    mutated_inputs.extend(text_mutate(root, mutated_inputs))

    if mutated_inputs:  # Check if the list is not empty
        selected_input = random.choice(mutated_inputs)
        selected_index = mutated_inputs.index(selected_input)
        # print(f"Selected index: {selected_index}")
        return selected_input  # Return the selected input
    else:
        return None  # Return None if mutated_input is empty
