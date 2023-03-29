from os.path import isdir
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(prog='shift_left_secure')
    parser.add_argument('-d', '--directory', help='directory of git project', dest='directory', type=str, required=True)

    args = parser.parse_args()