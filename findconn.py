import os       # for directory traversal
import sys      # for argv
import re       # for regex
import ctypes   # for readblah shared library


def search(path: str) -> list:
    output_list = []
    blah_lib = ctypes.cdll.LoadLibrary("./readblah.so")

    # specify the return value of the read_blah function explicitly, so it doesn't return int
    blah_lib.read_blah.restype = ctypes.c_char_p

    # Create re object using the specified regex below.
    regex = re.compile(r'mysql://'           # Beginning of connection string will always start with mysql://
                       
                       r'((?!\.\.).)*?/'     # Use a negative look ahead (?!) to exclude double periods but accept any 
                                             # other characters before the forward slash. Use a lazy match (*?) to 
                                             # allow for the possibility of multiple matches per line. If a greedy match
                                             # is used, the regex will match the very last forward slash of the line.
                                             # This will match both the server name and port, if the port is included.
                       
                       r'[A-Za-z]([^\s]+)')  # The database name must start with a letter [A-Za-z] and can contain
                                             # letters, digits, and underscores. This regex matches anything that comes
                                             # after the server name or port starting with a letter until the first
                                             # whitespace ([^\s]+).
    files = os.listdir(path)
    os.chdir(path)

    for file in files:
        path_extension = file[file.find(".") + 1:]

        if path_extension == "txt":
            current_file = open(file, 'r')

            # Parse through opened file for matching regex.
            # For each match, add the connection string to the list.
            for line in current_file:
                match = regex.finditer(line)
                for sqlString in match:
                    output_list.append(sqlString.group(0))

            current_file.close()

        elif path_extension == "blah":
            opened_file = blah_lib.open_blah((file.encode()))
            output = blah_lib.read_blah(opened_file)

            print("Printing contents of blah file:")
            # Parse through and print value fromm blah file.
            while output is not None:
                print(output.decode())
                output = blah_lib.read_blah(opened_file)

            blah_lib.close_blah(opened_file)

    return output_list


def main():
    if len(sys.argv) < 2:
        print("Usage: findconn.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    search_output = search(path)
    search_output.sort()

    print("Printing sorted regex matches:")
    for entry in search_output:
        print(entry)


if __name__ == '__main__':
    main()
