import json
import os
import sys
import ast  # For safely evaluating the string representation of the list

# Function to transform the array into a JSON
def transform_to_json(data):
    result = []
    block = {}
    
    for line in data:
        if line == "":
            # When an empty line is encountered, we consider it as the end of a block
            if block:
                result.append(block)
                block = {}
        else:
            # Split line at the first occurrence of ':'
            key, value = line.split(":", 1)
            key = key.strip()  # Remove any leading/trailing whitespace
            value = value.strip()  # Remove any leading/trailing whitespace
            block[key] = value
    
    # If the last block exists and is not appended
    if block:
        result.append(block)
    
    return result

def main():
    # Check if input is provided
    if len(sys.argv) < 2:
        sys.exit(1)

    # Get the raw input string
    raw_data = sys.argv[1]
    
    try:
        # Parse the raw string into a Python list
        data = ast.literal_eval(raw_data)
        
        # Validate the parsed data is a list
        if not isinstance(data, list):
            raise ValueError("The input data must be a list.")

        # Transform the data
        transformed_data = transform_to_json(data)

        # Get the directory where the script is located
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Define the output file path in the same directory as the script
        output_file = os.path.join(script_dir, "transformed_data.json")
        
        # Write the transformed dictionary to a JSON file
        with open(output_file, 'w') as json_file:
            json.dump(transformed_data, json_file, indent=4)

    except (ValueError, SyntaxError) as e:
        sys.exit(1)

if __name__ == '__main__':
    main()
