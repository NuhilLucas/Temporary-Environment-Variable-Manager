from subprocess import run as subprocess_run
from .func import path_exists, os_remove
from ..instance import Root_BatScripts, Root_TempFiles

BatTemplate: str = '''@echo off
set "ROOT=%~dp0.."
set "CALLFROM=%CD%"
set "PYTHONPATH=%ROOT%/src"
cd /d "%ROOT%"
"%ROOT%/projects/python_standalone/python.exe" -m tevm.main "%CALLFROM%." {name} %*'''

Path_TempPS1 = Root_TempFiles + "/temp.ps1"

def bat_build(name: str, write: bool = True):
    """
    name: 在 Shell 中调用时使用的关键字, 不区分大小写.
    """
    ScriptPath: str = Root_BatScripts + "/" + name + ".bat"
    data = BatTemplate.format(name=name)

    if write:
        with open(file=ScriptPath, mode="w", encoding="utf-8") as File:
            File.write(data)
    
    return data

def ps1_build(root: str, project: dict, params: list[str], write: bool = True):
    """
    root: TEVM根路径, 用于拼接绝对路径.
    project: 项目配置数据.
    params: 被调用的可执行文件接受的参数.
    """
    os_remove(Path_TempPS1)

    executables: dict[str] = project["executables"]
    envars: dict[str] = project["envars"]

    cmd_envars: str = "\n".join([
        f"$env:{key} = \"{root + value[4:] if value.startswith('rel|') else value}\"" for key, value in envars.items()
    ]) + "\n"

    cmd_execute: str = "& " + " ".join([
        f"\"{root + _executable_[4:] if _executable_.startswith('rel|') else _executable_}\" {_params_}" for _executable_, _params_ in executables.items()
    ]) + " ".join(params)

    if write:
        with open(file=Path_TempPS1, mode="w", encoding="utf-8-sig") as File:
            File.write(data:="chcp 65001 | Out-Null" + cmd_envars + cmd_execute)
    
    return data

def run(cwd: str):
    if not path_exists(Path_TempPS1): return

    try:
        subprocess_run(
            args=["powershell", "-ExecutionPolicy", "Bypass", "-File", Path_TempPS1],
            cwd=cwd
        )
    except Exception as E:
        print(E)

    os_remove(Path_TempPS1)

if __name__ == "__main__":
    bat_build("test")
    root = "D:/Warehouse/Personal/Project/Program/Python/Temporary-Environment-Variable-Manager"
    envar = {
        "test_1": "11111",
        "test_2": "22222"
    }
    zexes = ["rel|/projects/python/python.exe", "rel|/projects/pipx/pipx-app.pyz"]
    params = ["param1", "param2"]

    ps1_build(root=root, envar=envar, zexes=zexes, params=params)