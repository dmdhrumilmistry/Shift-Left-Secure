# Shift Left Secure

Secure your project source code before pushing commits to github/gitlab/bitbucket.

## Installation

### Using Pip

- From PyPi

    ```bash
    python -m pip install -U shift_left_secure
    ```

- From Github

    ```bash
    python -m pip install git+https://github.com/dmdhrumilmistry/Shift-Left-Secure.git
    ```

### Using Git Clone for Development

- Clone repo

    ```bash
    git clone https://github.com/dmdhrumilmistry/Shift-Left-Secure.git
    ```

- change directory

    ```bash
    cd Shift-Left-Secure
    ```

- Install project

    ```bash
    python -m pip install -e . 
    ```

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
