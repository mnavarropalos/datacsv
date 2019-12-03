import argparse as _argparse
import os as _os

_SCRIPT_TITLE = "Pollito's Magic"
_SCRIPT_VERSION_MAJOR = 0
_SCRIPT_VERSION_MINOR = 1
_SCRIPT_VERSION_PATCH = 0
_SCRIPT_TITLE_WITH_VERSION = _SCRIPT_TITLE + " ver." + str(_SCRIPT_VERSION_MAJOR) + "." + str(_SCRIPT_VERSION_MINOR) + "." + str(_SCRIPT_VERSION_PATCH)

_NEW_ENTRY_IDENTIFIERS = [

    "\n",
    "\n\r",
    "\r"
    "\r\n",
    " ",
    ""
]

def parse_arguments():

    # Create the argument parser
    argument_parser = _argparse.ArgumentParser(description=_SCRIPT_TITLE_WITH_VERSION)

    # Create script arguments
    argument_parser.add_argument("-i", "--input", help="File to parse", required=True)
    argument_parser.add_argument("-o", "--output", help="Output file name. Default <input_file_path>.csv", default='default')

    # Parse script arguments
    arguments = argument_parser.parse_args()

    # Create output file name if not provided
    if "default" in arguments.output:
        # Split path and name
        path, name = _os.path.split(arguments.input)
        # Change extension
        name = _os.path.splitext(name)[0]
        name = name + ".csv"
        # Replace arguments output path
        arguments.output = _os.path.join(path, name)

    print("--Input file path: " + arguments.input)
    print("--Output file path: " + arguments.output)

    return arguments

def file_to_dict_list(file_path):

    # List of dictionaries with all entries
    data_dict_list = []

    # Each of the entries in the file as a dictionary
    data_dict = {}

    try:

        # Open input path
        with open(file_path) as file_to_parse:

            # Read line by line
            lines = file_to_parse.readlines()
            for line in lines:            

                # Is this a new entry?
                if line in _NEW_ENTRY_IDENTIFIERS:

                    data_dict_list.append(data_dict)

                    data_dict = {}

                else:

                    # This is part of existing entry

                    # Clean read line
                    line = line.replace(" ", "")
                    line = line.replace("\n", "")

                    # Tokenize line
                    line_key, line_value = line.split(":")

                    # Create the attribute if does not exist
                    if not data_dict.has_key(line_key):
                        data_dict[line_key] = []

                    data_dict[line_key].append(line_value)

    except IOError:
        print("--Error: Could not open input file")

    # Now simplify the data dict list
    data_dict_list = simplify_data_dict_list(data_dict_list)

    return data_dict_list

def simplify_data_dict_list(data_dict_list):

    attributes_dict = {}

    simplified_data_dict_list = []

    # Phase 1: Identify master attributes

    # Iterate thru all entries
    for data_dict in data_dict_list:

        # Iterate thru each entry
        for data_dict_key, data_dict_values in data_dict.iteritems():

            current_value_count = 0
            
            # Detect how many repeated attributes contains this entry
            for data_dict_value in data_dict_values:

                # Create a new key for this attribute
                new_data_dict_key = data_dict_key + "_" + str(current_value_count)

                attributes_dict[new_data_dict_key] = ""

                current_value_count += 1
    
    # Phase 2: Fill master attributes

    # Iterate thru all entries
    for data_dict in data_dict_list:

        # Create a new simplified entry
        simplified_data_dict = attributes_dict.copy()

        # Iterate thru each entry
        for data_dict_key, data_dict_values in data_dict.iteritems():

            current_value_count = 0
            
            # Detect how many repeated attributes contains this entry
            for data_dict_value in data_dict_values:

                # Create a new key for this attribute
                new_data_dict_key = data_dict_key + "_" + str(current_value_count)

                simplified_data_dict[new_data_dict_key] = data_dict_value

                current_value_count += 1

        # Insert the new entry
        simplified_data_dict_list.append(simplified_data_dict)

    # Return a list of dicts which contains all attributes
    return simplified_data_dict_list


def dict_list_to_csv(data_dict_list):


    # Create CSV header
    csv_header = ""
    for attribute in data_dict_list[0].iterkeys():
        csv_header += ","
        csv_header += attribute
    csv_header = csv_header[1:]
    
    # Create CSV rows
    csv_rows = ""
    for data_dict in data_dict_list:

        # Create CSV row
        csv_row = ""
        for attribute, value in data_dict.iteritems():
            csv_row += ","
            csv_row += value
        csv_row = csv_row[1:]

        # Append CSV row
        csv_rows += csv_row
        csv_rows += "\n"
    
    return csv_header + "\n" + csv_rows

def main():

    print(_SCRIPT_TITLE_WITH_VERSION)

    # Parse script arguments
    print("-Parsing arguments")
    arguments = parse_arguments()

    print("-Parsing input file")
    data_dict_list = file_to_dict_list(arguments.input)
    if len(data_dict_list) == 0:
        print("--Error: Could not parse input file")
        exit(1)

    # Create CSV from key:value
    print("-Creating CSV data")
    csv_data = dict_list_to_csv(data_dict_list)
    if csv_data == "":
        print("--Error: Could not create csv data")
        exit(1)

    # Create output file
    print("-Creating output file")
    try:
        with open(arguments.output, 'w') as output_file:
            output_file.write(csv_data)
    except:
        print("--Error: Could not create output file")
        exit(1)

    print("-Output file created: " + arguments.output)

if __name__== "__main__":
    main()