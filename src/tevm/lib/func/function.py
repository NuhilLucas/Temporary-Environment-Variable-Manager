from sys import exit as __exit__
from os import remove as __remove__
from os.path import exists as __exists__

class ColorPrint:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    RESET = "\033[0m"

    def print(*args):
        return lambda color: print(color + " ".join(args) + ColorPrint.RESET)

def sys_exit(status: int = 0):
    __exit__(status)

def path_exists(path: str) -> bool:
    return __exists__(path)

def os_remove(path: str):
    __remove__(path) if __exists__(path) else None
