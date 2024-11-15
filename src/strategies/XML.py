import os
import xml.etree.ElementTree as ET
import copy, random
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion, known_integer_text
from mutators.format_string import format_string_attack
import xml.dom.minidom


def format_input(input_file):
    with open(input_file, "r") as f:
        return f.read()

def text_mutate(root, mutated_inputs):

    elements_with_text = [elem for elem in root.iter() if elem.text is not None]

    for elem in elements_with_text:
        original_text = elem.text

        # check if the element has children (to avoid creating invalid mixed content)
        if list(elem):
            continue
        
        
        elem.text = format_string_attack().decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        for known in known_integer_text():
            elem.text = known.decode()
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)

        elem.text = buffer_overflow().decode()
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
            
            for known in known_integer_text():
                elem.attrib[attr_name] = known.decode()
                mutated_xml = ET.tostring(root, encoding="unicode")
                mutated_inputs.append(mutated_xml)

            elem.attrib[attr_name] = buffer_overflow().decode()
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
        
        for known in known_integer_text():
            elem.tag = known.decode()
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)
        
        elem.tag = (b"B" * 200).decode()
        mutated_xml = ET.tostring(root, encoding="unicode")
        mutated_inputs.append(mutated_xml)
        
        elem.tag = original_tag
        
    for i in range(len(root)):
        for _ in range(100):
            # Deep copy the child element to avoid shared references
            root.append(copy.deepcopy(root[i]))
            mutated_xml = ET.tostring(root, encoding="unicode")
            mutated_inputs.append(mutated_xml)

        # Restore the tree to the original state by removing appended elements
        for _ in range(100):
            root.remove(root[-1])
        
    return mutated_inputs

def pretty_print_xml(xml_string):
    """
    Pretty prints the XML string in an indented format.
    """
    try:
        # Parse the XML string
        parsed_xml = xml.dom.minidom.parseString(xml_string)

        # Convert to a pretty-printed format
        pretty_xml = parsed_xml.toprettyxml(indent="    ")

        # Print the formatted XML
        print(pretty_xml)
    except Exception as e:
        print(f"Error formatting XML: {e}")

def mutate_xml(xml_input_file, binary_file, harness):
    sample_xml = format_input(xml_input_file)
    root = ET.fromstring(sample_xml)
    
    mutated_inputs = []
    mutated_inputs.extend(tag_mutate(root, mutated_inputs))
    mutated_inputs.extend(attr_mutate(root, mutated_inputs))
    mutated_inputs.extend(text_mutate(root, mutated_inputs))
    
    #for idx, mutated_xml in enumerate(mutated_inputs, start=1):
        #print(f"Mutation {idx}:")
        #pretty_print_xml(mutated_xml)
        #print("-" * 80)  # Separator for better readability
    # Run each mutated input through the harness
    for mutated_input in mutated_inputs:
        res = harness.run_retrieve(binary_file, mutated_input)
        if res:
            continue
        
'''
SAMPLE INPUT

<html>
    <head>
        <link href="http://somewebsite.com" />
    </head>
    <body>
        <h1>I'm not a web developer.</h1>
    </body>
    <div id="#lol">
        <a href="http://google.com">Here is some link...</a>
    </div>
    <tail>
        <a href="http://bing.com">Footer link</a>
    </tail>
</html>


'''

#3 parts to it
#element     e.g. <head>
#attribute   e.g. href="" or id=""
#content     e.g. I'm not a web dev