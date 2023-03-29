# Shift Left Secure

Secure your project source code before pushing commits to github/gitlab/bitbucket.

## Usage

- Add your ChatGPT API key to environment variable

    ```bash
    export OPEN_API_KEY=KEY
    ```

- Use help to view options

    ```bash
    $ python -m shift_left_secure -h
    usage: shift_left_secure [-h] -d DIRECTORY [-c COMMITS] [-o OUTPUT_PATH]

    options:
    -h, --help            show this help message and exit
    -d DIRECTORY, --directory DIRECTORY
                            directory of git project
    -c COMMITS, --commit_hash COMMITS
                            no of commits to be analyzed from current HEAD
    -o OUTPUT_PATH, --output OUTPUT_PATH
                            output path to json file
    ```

- Start analyzing changes between commits using below cmd:

    ```bash
    python -m shift_left_secure -d 'path_to_git_project' -c 1 -o test.json
    ```
