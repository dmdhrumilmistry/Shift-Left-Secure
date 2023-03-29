from argparse import ArgumentParser
from asyncio import run
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
    parser.add_argument('-c', '--commit_hash', help='commit hash', dest='commits', type=int, default=1)

    args = parser.parse_args()

    # get diff changes
    git = GitHandler(repo_dir=args.directory)
    diff_changes = join_diffs(git.get_diff(args.commits))

    analyzed_code_snippets = run(code_analyzer.analyze_git_changes(diff_changes))

    pprint(analyzed_code_snippets)