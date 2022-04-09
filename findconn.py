import sys
import re


def search(path: str) -> list:
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

    connections_list = []
    file = open(path, 'r')

    for line in file:
        match = regex.finditer(line)
        for sqlString in match:
            connections_list.append(sqlString.group(0))
    connections_list.sort()

    return connections_list


def main():
    if len(sys.argv) < 2:
        print("Usage: findconn.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    connections_list = search(path)
    for connection in connections_list:
        print(connection)


if __name__ == '__main__':
    main()
