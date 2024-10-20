import struct

integers_to_find = [2016, 1344, 672]
integers_to_find_bytes = {
    "4-byte_little_endian": [struct.pack('<I', i) for i in integers_to_find],
    "4-byte_big_endian": [struct.pack('>I', i) for i in integers_to_find],
    "2-byte_little_endian": [struct.pack('<H', i) for i in integers_to_find],
    "2-byte_big_endian": [struct.pack('>H', i) for i in integers_to_find],
}

def search_integers_in_file(file_path):
    offsets_dict = {key: {i: [] for i in integers_to_find} for key in integers_to_find_bytes}
    with open(file_path, 'rb') as f:
        data = f.read()

    for format_name, integer_bytes_list in integers_to_find_bytes.items():
        for i, integer_bytes in enumerate(integer_bytes_list):
            integer_value = integers_to_find[i]
            print(f"Searching for {integer_value} in {format_name} format...")
            offset = 0
            while True:
                found_at = data.find(integer_bytes, offset)
                if found_at == -1:
                    break
                offsets_dict[format_name][integer_value].append(found_at)
                print(f"{integer_value} found at offset: {hex(found_at)} in {format_name}")
                offset = found_at + len(integer_bytes)

    return offsets_dict

def find_offset_patterns(offsets_dict):
    for format_name, integer_offsets in offsets_dict.items():
        print(f"\nPatterns for {format_name}:")
        for integer, offsets in integer_offsets.items():
            if len(offsets) > 1:
                print(f"\nPatterns for integer {integer}:")
                for i in range(1, len(offsets)):
                    diff = offsets[i] - offsets[i - 1]
                    print(f"Offset difference between {hex(offsets[i - 1])} and {hex(offsets[i])}: {diff} bytes")
            elif len(offsets) == 1:
                print(f"\nNo patterns found for integer {integer} (only one occurrence).")

offsets_dict = search_integers_in_file('.\\code.bin')
find_offset_patterns(offsets_dict)