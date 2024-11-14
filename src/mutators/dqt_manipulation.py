# #!/usr/bin/env python3

def corrupt_dqt_table(data):
    qt_start_index = data.find(b'\xff\xdb')
    if qt_start_index != -1:
        qt_end_index = qt_start_index + 64  
        corrupted_data = bytearray(data)
        for i in range(qt_start_index + 5, qt_end_index, 5):
            corrupted_data[i] = corrupted_data[i] ^ 0xff
        return bytes(corrupted_data)
    return data
