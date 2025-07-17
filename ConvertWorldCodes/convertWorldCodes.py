#!/usr/bin/env python3

import json
import re


def main():
    try:
        with open('/mnt/ramdisk/tmp/data.txt', 'r') as file:
            lines = file.readlines()

        # Remove newline characters (optional)
        lines = [line.rstrip('\n') for line in lines]

        print(f"Read {len(lines)} lines from data.txt")

        sections = []
        current_section = None

        for line in lines:
            line = line.strip()

            if line.startswith("////////"):
                break

            if line.startswith("const "):
                # Start a new section
                current_section = [line]
            elif current_section is not None:  # Only process if we're in a section
                current_section.append(line)

                # Check if this line ends the section
                if line.startswith("};"):
                    sections.append(current_section)
                    current_section = None

        # Check if we have an unfinished section at the end
        if current_section is not None:
            sections.append(current_section)

        print(f"Split into {len(sections)} sections")

        # Split sections into tuples of three
        grouped_sections = []
        for i in range(0, len(sections), 3):
            group = tuple(sections[i:i+3])
            grouped_sections.append(group)

        print(f"Created {len(grouped_sections)} groups of sections")

        processed_data = []

        for group in grouped_sections:
            if not group:  # Skip empty groups
                continue

            # Process first section in the group
            first_section = group[0]
            if not first_section:  # Skip empty sections
                continue

            # Extract name from the first line
            first_line = first_section[0]
            name_match = re.search(r'code_(\w+)Times', first_line)
            if name_match:
                name = name_match.group(1)
            else:
                print(f"Warning: Could not extract name from {first_line}")
                name = "unknown"

            # Remove the first line (declaration) and the last line (closing bracket)
            content_lines = first_section[1:-1]

            # Process number lines
            number_text = " ".join(content_lines)
            # Remove commas and collect all numbers
            numbers = [int(num) for num in re.findall(r'-?\d+', number_text)]

            # Process second section (hex values) if it exists
            if len(group) > 1 and group[1]:
                second_section = group[1]

                # Extract name from the second section's first line
                second_line = second_section[0]
                second_name_match = re.search(r'code_(\w+)Codes', second_line)
                if second_name_match:
                    second_name = second_name_match.group(1)
                    # Check if names match
                    if second_name != name:
                        print(f"Warning: Name mismatch - '{name}' in first section vs '{second_name}' in second section")
                else:
                    print(f"Warning: Could not extract name from second section: {second_line}")

                # Remove the first line (declaration) and the last line (closing bracket)
                hex_content_lines = second_section[1:-1]

                # Process hex lines
                hex_text = " ".join(hex_content_lines)

                # Find all hex values and convert to integers
                hex_numbers = [int(num, 16) for num in re.findall(r'0x[0-9A-Fa-f]+', hex_text)]
            else:
                hex_numbers = []

            # Process third section (configuration) if it exists
            frequency = 0
            items_count = 0
            bits_per_entry = 0

            if len(group) > 2 and group[2]:
                third_section = group[2]

                # Join all lines in the section
                config_text = " ".join(third_section)

                # Extract name from the config text
                third_name_match = re.search(r'code_(\w+)Code', config_text)
                if third_name_match:
                    third_name = third_name_match.group(1)
                    # Check if names match
                    if third_name != name:
                        print(f"Warning: Name mismatch - '{name}' in first section vs '{third_name}' in third section")
                else:
                    print(f"Warning: Could not extract name from third section")

                # Extract all integers from the config text
                integers = re.findall(r'(?<=[{(),])\s*(\d+)\s*[,)}]', "{" + config_text)
                if len(integers) >= 3:  # Need at least 3 numbers (freq, items, bits)
                    frequency = int(integers[0])
                    items_count = int(integers[1])
                    bits_per_entry = int(integers[2])
                else:
                    print(f"Warning: Could not extract frequency, items count, and bits per entry for {name}")

            # Convert hex numbers to a continuous bit string
            bit_string = ""
            for hex_num in hex_numbers:
                # Convert to binary string, remove '0b' prefix
                binary = bin(hex_num)[2:].zfill(8)
                bit_string += binary

            # Extract items from the bit string
            extracted_items = []
            for i in range(items_count):
                start_bit = i * bits_per_entry
                if start_bit + bits_per_entry <= len(bit_string):
                    # Extract bits for this item (MSb first)
                    item_bits = bit_string[start_bit:start_bit + bits_per_entry]
                    # Convert binary string to integer
                    item_value = int(item_bits, 2)
                    extracted_items.append(item_value)

            # Create a dictionary with all extracted information
            processed_data.append({
                "name": name,
                "numbers": numbers,
                "hex_numbers": hex_numbers,
                "frequency": frequency,
                "items_count": items_count,
                "bits_per_entry": bits_per_entry,
                "extracted_items": extracted_items,
            })

        print(f"Processed {len(processed_data)} data entries")
        for i, entry in enumerate(processed_data):
            print(f"Entry {i}: {entry['name']} with {len(entry['numbers'])} numbers")
            print(f"  Extracted items: {entry['extracted_items']}")
            # Create a filtered dictionary with only the requested fields
            filtered_entry = {
                "name": entry['name'],
                "frequency": entry['frequency'],
                "times": [num * 10 for num in entry['numbers']],  # Multiply each time by 10
                "indices": entry['extracted_items']
            }
            print(json.dumps(filtered_entry))

    except FileNotFoundError:
        print("Error: File 'data.txt' not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
