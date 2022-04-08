import sys
import re


def search(path: str) -> list:
    file = open(path, 'r')

    for line in file:
        pass



def main():
    if len(sys.argv) < 2:
        print("Usage: findconn.py <path>")
        sys.exit(1)

    path = sys.argv[1]
    search(path)


if __name__ == '__main__':
    main()
