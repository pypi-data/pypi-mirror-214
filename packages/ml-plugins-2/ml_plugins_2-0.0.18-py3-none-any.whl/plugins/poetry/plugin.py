import sys
import functools
import subprocess

from metaflow.includefile import IncludeFile 
from metaflow.exception import MetaflowException

def write_to_disk(data: str, filename: str):
    with open(filename, mode='w+') as f:
        f.write(data)

def poetry():
    def decorator(function):
        @functools.wraps(function)
        def wrapper(self, *args):
            if hasattr(self, "lockfile"):
                write_to_disk(self.lockfile, "poetry.lock")
            write_to_disk(self.pyproject, "pyproject.toml")
            subprocess.run([sys.executable, '-m', 'poetry', 'install', '--no-pylint', '-C', 'pyproject.toml'])
            return function(self, *args)
        return wrapper
    return decorator

