# Generate versions of the sample input with keywords removed.
def delete_keywords(sample_input, keywords) -> bytearray:
    for keyword in keywords:
        return sample_input.replace(keyword, b"")

# Generate versions of the sample input with repeated keywords.
def repeat_keywords(sample_input, keywords, repetitions) -> bytearray:
    for keyword in keywords:
        for n in range(1, repetitions):
            return sample_input.replace(keyword, keyword * n)