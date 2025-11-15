from os import getcwd, _exit as os_exit
from signal import signal, SIGINT
from .lib.config_rw import json_read
from sys import argv as __argv__

# 防止 Ctrl + C 退出报错
signal(SIGINT, lambda sig, frame: (print(), os_exit(0)))

__state__: bool = False
__param_useable__: bool = __argv__.__len__() > 2

Projects: dict = {}
SourceBat: str = __argv__[2] if __param_useable__ else ""
Params: list = __argv__[3:] if __param_useable__ else []
Path_Root: str = getcwd().replace("\\", "/") # TEVM 的根路径.
Path_Python: str = Path_Root + "/python_standalone/python.exe" # TEVM 内置的 python 解释器.
Path_PyScript: str = __argv__[0].replace("\\", "/") # python脚本文件路径.
Path_CallFrom: str = __argv__[1].replace("\\", "/")[:-1] if __argv__.__len__() > 1 else "" # bat脚本文件被调用位置.
Path_HTML: str = Path_Root + "/src/tevm/gui/index.html" # WEB GUI 的 index 文件.
Path_ConfigProjects: str = Path_Root + "/config/projects.json"
Root_BatScripts: str = Path_Root + "/scripts"
Root_TempFiles: str = Path_Root + "/temp"

__state__, Projects = json_read(Path_ConfigProjects)
if not __state__: raise Exception(Projects)

