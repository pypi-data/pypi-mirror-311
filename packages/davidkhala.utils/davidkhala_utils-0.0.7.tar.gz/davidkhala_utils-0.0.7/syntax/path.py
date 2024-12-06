import os
from pathlib import Path


def resolve(*path_tokens):
    return str(Path(os.path.join(*path_tokens)))


def homedir():
    return os.path.expanduser('~')


def home_resolve(*path_tokens):
    return resolve(homedir(), *path_tokens)
