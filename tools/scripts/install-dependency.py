# python -m nuitka --onefile --enable-plugin=tk-inter --output-dir=dist tools/scripts/install-dependency.py

from os.path import exists as osp_exists
from subprocess import run as sp_run

def pip_install(path_pip: str, path_requirements: str, root_pkg: str):
    try:
        sp_run(
            [path_pip, "install", "-r", path_requirements, "-t", root_pkg],
            check=True
        )
    except Exception as E:
        return False, str(E)
    else:
        return True, None

def run(pause: bool = True):
    path_pip = "projects/python_standalone/Scripts/pip.exe"
    path_requirements: str = "config/requirements.txt"
    root_pkg: str = "src/tevm/site-packages"
    if not osp_exists(path_pip):
        print("\033[91mError[check_python]:\n    pip not installed yet, pls install pip with <get-pip> first.\033[0m")
        return input() if pause else None
    
    _state_pip_install_, _ = pip_install(path_pip, path_requirements, root_pkg)
    if not _state_pip_install_:
        print("\033[91mError[pip_install]:\n    " + _ + "\033[0m")
        return input() if pause else None
    else:
        print("\033[94mInfo[pip_install]:\n    install dependency success.\033[0m")
    
    return input() if pause else None

if __name__ == "__main__":
    run()