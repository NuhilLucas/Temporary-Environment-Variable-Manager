from urllib.request import (
    build_opener as ulr_build_opener,
    ProxyHandler as ulr_ProxyHandler
)
from urllib.error import (
    HTTPError as ule_HTTPError,
    URLError as ule_URLError
)
from os import remove as os_remove
from os.path import exists as osp_exists
from subprocess import run as sp_run

def get_script(url: str, proxy: str | dict = None):
    if isinstance(proxy, str):
        proxy_handler = ulr_ProxyHandler({'http': proxy, 'https': proxy})
    elif isinstance(proxy, dict):
        proxy_handler = ulr_ProxyHandler(proxy)
    else:
        proxy_handler = None

    opener = ulr_build_opener() if proxy_handler is None else ulr_build_opener(proxy_handler)

    data: str = ""
    try:
        with opener.open(url, timeout=10) as response:
            data = response.read().decode('utf-8')
    except (ule_HTTPError, ule_URLError) as E:
        return False, E.reason
    except Exception as E:
        return False, str(E)
    else:
        return True, data

def run_script(data: str, python: str):
    path_script: str = "temp/get-pip.py"

    try:
        if osp_exists(path_script): os_remove(path_script)

        with open(path_script, "w", encoding="utf-8") as File:
            File.write(data)
        
        sp_run(
            [python, path_script],
            check=True
        )

        if osp_exists(path_script): os_remove(path_script)
    except Exception as E:
        return False, str(E)
    else:
        return True, None

def run(pause: bool = True):
    path_python: str = "projects/python_standalone/python.exe"
    url_get_pip: str = "https://bootstrap.pypa.io/get-pip.py"
    if not osp_exists(path_python):
        print("\033[91mError[check_python]:\n    python not installed yet, pls install python with <get-python> first.\033[0m")
        return input() if pause else None

    _state_get_script_, data = get_script(url_get_pip)
    if not _state_get_script_:
        print("\033[91mError[get_script]:\n    " + data + "\033[0m")
        return input() if pause else None
    else:
        print("\033[94mInfo[run_script]:\n    get get-pip.py script success.\033[0m")
    
    _state_run_script_, _ = run_script(data, path_python)
    if not _state_run_script_:
        print("\033[91mError[run_script]:\n    " + _ + "\033[0m")
        return input() if pause else None
    else:
        print("\033[94mInfo[run_script]:\n    run get pip success.\033[0m")
    
    return input() if pause else None

if __name__ == "__main__":
    run()