from argparse import ArgumentParser
from pprint import pprint
from os import environ


from .chatgpt_api import CodeAnalyzer 
from .git_handler import GitHandler
from .utils import join_diffs

OPEN_API_KEY = environ.get('OPEN_API_KEY', False)
code_analyzer = CodeAnalyzer(
    api_key=OPEN_API_KEY,
    model_engine='gpt-3.5-turbo',
)


if __name__ == '__main__':
    parser = ArgumentParser(prog='shift_left_secure')
    parser.add_argument('-d', '--directory', help='directory of git project', dest='directory', type=str, required=True)
    parser.add_argument('-c', '--commit_hash', help='commit hash', dest='commits', type=str, default=1)

    args = parser.parse_args()

    # get diff changes
    git = GitHandler(repo_dir=args.directory)
    diff_changes = join_diffs(git.get_diff(args.commits))

    for diff in diff_changes:
        file_name = diff.get('file_path')
        changed_lines = diff.get('changed_lines')

        # analyzed_data = code_analyzer.analyze_code(file_name='testing.py', code=changed_lines)
        # pprint(analyzed_data)