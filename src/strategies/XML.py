import os
import xml.etree.ElementTree as ET
import copy, random
from bs4 import BeautifulSoup
from mutators.bitflip import bit_flip
from mutators.buffer_overflow import buffer_overflow
from mutators.byteflip import byte_flip
from mutators.known_integer import known_integer_insertion
from mutators.format_string import format_string_attack


def format_input(input_file):
    with open(input_file, "r") as f:
        return f.read()

def is_valid_xml(element):
    """Check if the provided XML element is well-formed using BeautifulSoup."""
    try:
        # Serialize element to string
        serialized_xml = ET.tostring(element).decode()
        
        # Check with BeautifulSoup for well-formedness
        soup = BeautifulSoup(serialized_xml, "xml")
        if soup.find_all():  # Check if any elements were parsed
            return True
        return False
    except Exception:
        return False


def remove_tag(elem):
    """Remove a random child tag from the given element."""
    children = list(elem)
    if children:
        elem.remove(random.choice(children))

def clear_tag(elem):
    """Clear the content and attributes of a random tag within the element."""
    children = list(elem)
    if children:
        tag_to_clear = random.choice(children)
        tag_to_clear.clear()  # Clears all sub-elements and text

def add_tag(elem):
    """Add a new random tag to the given element."""
    new_tag = ET.SubElement(elem, f"new_tag_{random.randint(0, 1000)}")
    new_tag.text = "new content"

def modify_tag(elem):
    """Modify the name or attribute of a random tag within the element."""
    children = list(elem)
    if children:
        tag_to_modify = random.choice(children)
        tag_to_modify.tag += "_modified"
        

def add_tags_overflow(elem, num_tags=100):
    """Add a large number of tags to test for overflow or memory management issues."""
    for _ in range(num_tags):
        ET.SubElement(elem, f"overflow_tag_{random.randint(0, 100)}").text = "overflow_content"
        
def remove_attr(elem):
    """Remove a random attribute from the element, if any exist."""
    if elem.attrib:
        attr_to_remove = random.choice(list(elem.attrib.keys()))
        del elem.attrib[attr_to_remove]

def add_attr(elem):
    """Add a new random attribute to the element."""
    elem.set(f"new_attr_{random.randint(0, 1000)}", f"value_{random.randint(0, 100)}")

def modify_attr(elem):
    """Modify the value of a random attribute in the element."""
    if elem.attrib:
        attr_to_modify = random.choice(list(elem.attrib.keys()))
        elem.set(attr_to_modify, f"modified_value_{random.randint(0, 1000)}")

def add_attr_overflow(elem, num_attrs=100):
    """Add a large number of attributes to test for overflow or memory management issues."""
    for i in range(num_attrs):
        elem.set(f"overflow_attr_{i}", f"overflow_value_{i}")

def clear_attr(elem):
    """Clear all attributes from the element."""
    elem.attrib.clear()
    
def remove_text(elem):
    """Remove text from a random element by setting it to an empty string."""
    elem.text = ""

def clear_text(elem):
    """Clear all sub-element text by setting each sub-element’s text to an empty string."""
    for child in elem.iter():
        child.text = ""
        

def mutate_tags(elem):
    """Apply each tag-related mutation to the given XML element."""
    mutated_versions = []
    MUTATIONS = [
        buffer_overflow,
        # bit_flip,
        # byte_flip,
        format_string_attack,
        remove_tag,
        clear_tag,
        add_tag,
        modify_tag,
        add_tags_overflow
    ]
    
    # Apply each mutation in sequence
    for mutation in MUTATIONS:
        tag_mutated = copy.deepcopy(elem)
        mutation(tag_mutated)
        print(tag_mutated.tag)
        if is_valid_xml(tag_mutated):
            mutated_versions.append(tag_mutated)
    
    print(mutated_versions)
    return mutated_versions

def mutate_attributes(elem):
    """Apply each attribute-related mutation to the given XML element."""
    mutated_versions = []
    MUTATIONS = [
        buffer_overflow,
        # bit_flip,
        # byte_flip,
        format_string_attack,
        remove_attr,
        add_attr,
        modify_attr,
        add_attr_overflow,
        clear_attr
    ]
    
    # Apply each mutation in sequence
    for mutation in MUTATIONS:
        attr_mutated = copy.deepcopy(elem)
        mutation(attr_mutated)
        if is_valid_xml(attr_mutated):
            mutated_versions.append(attr_mutated)
    
    return mutated_versions

def mutate_texts(elem):
    """Apply each text-related mutation to the given XML element."""
    mutated_versions = []
    MUTATIONS = [
        buffer_overflow,
        # bit_flip,
        # byte_flip,
        format_string_attack,
        remove_text,
        clear_text,
    ]
    
    # Apply each mutation in sequence
    for mutation in MUTATIONS:
        text_mutated = copy.deepcopy(elem)
        mutation(text_mutated)
        if is_valid_xml(text_mutated):
            mutated_versions.append(text_mutated)
    
    return mutated_versions

# Now modify apply_mutate to collect all mutated versions
def apply_mutate(root):
    all_mutated_versions = []  # To store all mutations for each element

    # Loop over all elements in the XML tree
    for elem in root.iter():
        
        # Apply all tag mutations
        tag_mutated_versions = mutate_tags(elem)
        all_mutated_versions.extend(tag_mutated_versions)

        # Apply all attribute mutations
        attr_mutated_versions = mutate_attributes(elem)
        all_mutated_versions.extend(attr_mutated_versions)

        # Apply all text mutations
        text_mutated_versions = mutate_texts(elem)
        all_mutated_versions.extend(text_mutated_versions)
        
    return all_mutated_versions

# Example use of `apply_mutate`
def mutate_xml(xml_input_file, binary_file, harness):
    sample_xml = format_input(xml_input_file)
    root = ET.fromstring(sample_xml)
    
    mutated_inputs = apply_mutate(root)
    serialized_mutated_inputs = [ET.tostring(mutated_root).decode() for mutated_root in mutated_inputs]

    # Run each mutated input through the harness
    for mutated_input in serialized_mutated_inputs:
        res = harness.run_retrieve(binary_file, mutated_input)
        if res:
            continue
        
'''
3 parts to it
element     e.g. <head>
attribute   e.g. href="" or id=""
content     e.g. I'm not a web dev

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