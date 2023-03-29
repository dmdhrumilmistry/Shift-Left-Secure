from argparse import ArgumentParser
from asyncio import run
from os import environ


from .chatgpt_api import CodeAnalyzer 
from .git_handler import GitHandler
from .utils import join_diffs, json_to_file, analyzed_data_to_console


OPEN_API_KEY = environ.get('OPEN_API_KEY', False)
code_analyzer = CodeAnalyzer(
    api_key=OPEN_API_KEY,
    model_engine='gpt-3.5-turbo',
)


if __name__ == '__main__':
    parser = ArgumentParser(prog='shift_left_secure')
    parser.add_argument('-d', '--directory', help='directory of git project', dest='directory', type=str, required=True)
    parser.add_argument('-c', '--commit_hash', help='no of commits to be analyzed from current HEAD', dest='commits', type=int, default=1)
    parser.add_argument('-o', '--output', help='output path to json file', dest='output_path' ,required=False, default=False, type=str)

    args = parser.parse_args()

    # get diff changes
    git = GitHandler(repo_dir=args.directory)
    diff_changes = join_diffs(git.get_diff(args.commits))

    analyzed_code_snippets = run(code_analyzer.analyze_git_changes(diff_changes))

    analyzed_data_to_console(analyzed_code_snippets)

    if args.output_path:
        json_to_file(args.output_path,analyzed_code_snippets)
