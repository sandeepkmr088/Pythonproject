import json  # Import the json module to handle JSON data
import os    # Import the os module for interacting with the operating system
import sys   # Import the sys module to handle command-line arguments and system-specific parameters
import time  # Import the time module to format and manipulate time data

# Function to convert a file size to a human-readable format
def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G', 'T']:                        # Iterate through units of size
        if size < 1024:                                           # If size is less than 1024, return size with the current unit
            return f"{size}{unit}"
        size //= 1024                                             # Otherwise, divide the size by 1024 to convert to the next unit
    return f"{size}P"                                             # If size is extremely large, use 'P' for petabytes

# Function to list directory contents
def list_directory(data, show_all=False, long_format=False, reverse=False, sort_by_time=False, filter_by=None, human_readable=False):
    contents = data.get('contents', [])                                       # Get the list of contents from the data dictionary
    if filter_by:                                                             # If a filter is specified, filter the contents accordingly
        contents = [item for item in contents if (filter_by == 'dir' and 'contents' in item) or (filter_by == 'file' and 'contents' not in item)]
    if sort_by_time:                                                          # If sorting by time, sort contents by the 'time_modified' key
        contents = sorted(contents, key=lambda x: x['time_modified'], reverse=not reverse)
    elif reverse:                                                             # If reverse order is specified, reverse the list of contents
        contents = list(reversed(contents))
    for item in contents:                                                     # Iterate through the contents
        if not show_all and item['name'].startswith('.'):                     # Skip hidden files unless 'show_all' is True
            continue
        if long_format:                                                       # If long format is specified, print detailed information
            permissions = item['permissions']                                 # Get the file permissions
            size = human_readable_size(item['size']) if human_readable else item['size']  # Get the file size, optionally in human-readable format
            mod_time = time.strftime('%b %d %H:%M', time.localtime(item['time_modified']))  # Format the modification time
            name = item['name']  # Get the file name
            print(f"{permissions} {size} {mod_time} {name}")                               # Print the detailed information
        else:
            print(item['name'], end=' ')                                                   # Print the file name in a compact format
    if not long_format:                                                                    # Print a newline if not using long format
        print()

# Function to navigate through the directory path
def navigate_path(data, path):
    for part in path.split('/'):                                                           # Split the path by '/' and iterate through each part
        found = False
        for item in data.get('contents', []):                                              # Iterate through the contents of the current directory
            if item['name'] == part:                                                       # If the part matches the name of an item, navigate into that item
                data = item
                found = True
                break
        if not found:                                                                      # If the part is not found, print an error and return None
            print(f"error: cannot access '{path}': No such file or directory")
            return None
    return data                                                                            # Return the data for the final directory

# Function to print the help message
def print_help():
    help_message = """
    Usage: pyls [OPTIONS] [PATH]
    List information about the FILEs (the current directory by default).

    Options:
      -A                Do not ignore entries starting with .
      -l                Use a long listing format
      -r                Reverse order while sorting
      -t                Sort by modification time, newest first
      --filter=<option> Filter results by 'file' or 'dir'
      -h                Print sizes in human readable format
      --help            Display this help and exit
    """
    print(help_message)  # Print the help message

# Main execution block
if __name__ == "__main__":
    if '--help' in sys.argv:                                                        # If '--help' is in the command-line arguments, print the help message and exit
        print_help()
        sys.exit(0)

    # Parse command-line options
    show_all = '-A' in sys.argv                                                     # Show all files including hidden files
    long_format = '-l' in sys.argv                                                  # Use long listing format
    reverse_order = '-r' in sys.argv                                                # Reverse the order of the listing
    sort_by_time = '-t' in sys.argv                                                 # Sort the listing by modification time
    human_readable = '-h' in sys.argv                                               # Show file sizes in human-readable format

    filter_option = None
    path = ''
    for arg in sys.argv[1:]:                                                        # Iterate through the command-line arguments
        if '--filter=' in arg:                                                      # If a filter is specified, extract the filter option
            filter_option = arg.split('=')[1]
        elif not arg.startswith('-'):                                               # If the argument is not an option, treat it as the path
            path = arg

    # Load the directory structure from a JSON file
    with open('structure.json') as f:                                               # Open the JSON file
        directory_data = json.load(f)                                               # Load the JSON data

    if path:                                                                        # If a path is specified, navigate to that path
        directory_data = navigate_path(directory_data, path)
    if directory_data:                                                              # If the directory data is valid, list the directory contents
        list_directory(directory_data, show_all, long_format, reverse_order, sort_by_time, filter_option, human_readable)