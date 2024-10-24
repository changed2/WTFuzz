from magic import from_file

class Harness():
    strategy = None
    
    def __init__(self, input_file):
        file_type = from_file(input_file)
        if "CSV" in file_type:
            print("Switching to CSV mutator")
            self.strategy = "CSV"
        elif "JSON" in file_type:
            print("Switching to JSON mutator")
            self.strategy = "JSON"
        else:
            print("No matching strategy found, defaulting to plaintext")
            self.strategy = "TEXT"