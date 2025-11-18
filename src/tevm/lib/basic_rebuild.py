from .func.function import path_exists
from os import makedirs

def projects_json(path: str):
    try:
        if not path_exists(path[path.rfind("/")]): makedirs(name=path[path.rfind("/")], exist_ok=True)
        with open(path, "w", encoding="utf-8") as File:
            File.write("{}")
    except Exception as E:
        return False, str(E)
    else:
        return True, path

def temp(path: str):
    try:
        if not path_exists(path): makedirs(name=path, exist_ok=True)
    except Exception as E:
        return False, str(E)
    else:
        return True, path
    
if __name__ == "__main__":
    print(path_exists("."))