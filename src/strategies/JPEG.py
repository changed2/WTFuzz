# #!/usr/bin/env python3

# import random
# from collections import UserList

# class JPEGMutator(UserList):
#     def __init__(self, data):
#         super().__init__(data)

#     def modify_magic_numbers(self):
#         magic_values = [
#             (1, [0xff, 0x7f, 0x00]),
#             (2, [0xffff, 0x0000]),
#             (4, [0xffffffff, 0x00000000, 0x80000000, 0x40000000, 0x7fffffff])
#         ]
#         length = len(self.data) - 8
#         for size, values in magic_values:
#             idx = random.randint(0, length)
#             value = random.choice(values)
#             for i in range(size):
#                 self.data[idx + i] = (value >> (8 * (size - 1 - i))) & 0xff

#     def tweak_bits(self, count=100):
#         length = len(self.data) - 4
#         for _ in range(count):
#             idx = random.randint(2, length)
#             bit = 1 << random.randint(0, 7)
#             self.data[idx] ^= bit

# def read_jpeg_text(input_file):
#     with open(input_file, 'r') as file:
#         hex_data = file.read().strip()
#     jpeg_data = bytes.fromhex(hex_data)
#     return JPEGMutator(jpeg_data)

# def save_jpeg(jpeg_mutator, output_file):
#     with open(output_file, 'wb') as file:
#         file.write(bytes(jpeg_mutator))

# def mutate_jpeg(input_file, output_file, harness):
#     jpeg_mutator = read_jpeg_text(input_file)
#     jpeg_mutator.modify_magic_numbers()
#     jpeg_mutator.tweak_bits()

#     save_jpeg(jpeg_mutator, output_file)

#     mutated_data = bytes(jpeg_mutator)
#     harness.run_retrieve(output_file, mutated_data)



# # A JPEG image consists of a sequence of segments,
# # each beginning with a marker, each of which begins
# # with a 0xFF byte, followed by a byte indicating what
# # kind of marker it is.


