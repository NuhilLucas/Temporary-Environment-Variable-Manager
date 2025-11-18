from os import getcwd, _exit as os_exit
from signal import signal, SIGINT
from sys import argv as __argv__
from .lib.func import path_exists
from .lib.config_rw import json_read

# 防止 Ctrl + C 退出报错
signal(SIGINT, lambda sig, frame: (print(), os_exit(0)))

__state__: bool = False
__param_useable__: bool = __argv__.__len__() > 2

Projects: dict = {}
SourceBat: str = __argv__[2] if __param_useable__ else ""
Params: list = __argv__[3:] if __param_useable__ else []
Path_Root: str = getcwd().replace("\\", "/") # TEVM 的根路径.

# Basic File
Path_ConfigProjects: str = Path_Root + "/config/projects.json" # 配置文件.
Root_BatScripts: str = Path_Root + "/scripts" # 作为启动器的 bat 脚本文件的根目录.
Root_TempFiles: str = Path_Root + "/temp" # 临时文件文件夹.

Path_PyScript: str = __argv__[0].replace("\\", "/") # 作为执行目标的 Python 脚本文件路径.
Path_CallFrom: str = __argv__[1].replace("\\", "/")[:-1] if __argv__.__len__() > 1 else "" # bat脚本文件被调用位置.

Path_Python: str = Path_Root + "/python_standalone/python.exe" # TEVM 内置的 Python 解释器.
Root_Packages: str = Path_Root + "/src/tevm/site-packages" # 执行部分操作所需的 Python 第三方库.

Path_HTML: str = Path_Root + "/src/tevm/gui/index.html" # WEB GUI 的 index 文件.

if not path_exists(Path_ConfigProjects):
    from .lib.basic_rebuild import projects_json
    projects_json(Path_ConfigProjects)

if not path_exists(Root_TempFiles):
    from .lib.basic_rebuild import temp
    temp(Root_TempFiles)

__state__, Projects = json_read(Path_ConfigProjects)
if not __state__: raise Exception(Projects)

