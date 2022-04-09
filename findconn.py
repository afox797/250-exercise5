import sys
import re


def search(path: str) -> list:
    regex = re.compile(r'mysql://((?!\.\.).)*?/[A-Za-z]([^\s]+)')
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
