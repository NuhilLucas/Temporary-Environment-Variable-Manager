from sys import exit as __exit__
from subprocess import run as __run__
from os import remove as __remove__

BatTemplate: str = '''@echo off
set "ROOT=%~dp0.."
set "CALLFROM=%CD%"
set "PYTHONPATH=%ROOT%\src"
cd /d "%ROOT%"
"%ROOT%/python_standalone/python.exe" -m tevm.interface "%CALLFROM%." %*'''

def sys_exit(status: int = 0):
    __exit__(status)

def PS1Format():
    pass

def BatBuild(name: str):
    ScriptPath: str = "scripts/" + name + ".bat"
    with open(file=ScriptPath, mode="w", encoding="utf-8") as File:
        File.write(BatTemplate)

def Run(FileData: str, cwd: str):
    PathPS1: str = "temp/temp.ps1"

    try:
        with open(file=PathPS1, mode="w", encoding="utf-8") as File:
            File.write(FileData)
    except Exception as E:
        print(E)
        sys_exit(1)

    try:
        __run__(
            args=["powershell", "-ExecutionPolicy", "Bypass", "-File", PathPS1],
            cwd=cwd
        )
    except Exception as E:
        print(E)
        sys_exit(1)
    else:
        __remove__(PathPS1)

if __name__ == "__main__":
    BatBuild("test")