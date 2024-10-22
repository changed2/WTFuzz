from magic import from_file

def detect_input_format(file_path):
    file_type = from_file(file_path)
    if "CSV" in file_type:
        print("CSV Detected")
        return
    elif "JSON" in file_type:
        print("JSON Detected")
        return
    
    print("Unknown type, plaintext selected")

file_path = 'example_inputs/csv1.txt'
detected_format = detect_input_format(file_path)