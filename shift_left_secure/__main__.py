from argparse import ArgumentParser
from pprint import pprint
from .git_handler import GitHandler


if __name__ == '__main__':
    parser = ArgumentParser(prog='shift_left_secure')
    parser.add_argument('-d', '--directory', help='directory of git project', dest='directory', type=str, required=True)
    parser.add_argument('-c', '--commit_hash', help='commit hash', dest='commits', type=str, default=None)

    args = parser.parse_args()

    git = GitHandler(repo_dir=args.directory)

    pprint(git.get_diff())