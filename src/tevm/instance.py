from os import getcwd
from tevm.lib.config_rw import config_read
from sys import argv

__state__: bool = False

Projects: dict = {}
Params: list = argv[2:] if argv.__len__() > 2 else []
Path_Root: str = getcwd().replace("\\", "/")
Path_Python: str = Path_Root + "/python_standalone/python.exe"
Path_PyScript: str = argv[0].replace("\\", "/") # python脚本文件路径
Path_CallFrom: str = argv[1].replace("\\", "/")[:-1] if argv.__len__() > 1 else ""  # bat脚本文件被调用位置
Path_HTML: str = Path_Root + "/src/tevm/web/index.html"

__state__, Projects = config_read("config/projects.json")
if not __state__: raise Exception(Projects)