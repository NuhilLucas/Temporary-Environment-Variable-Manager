from sys import argv as sys_argv
print(sys_argv)

from pprint import pprint
from tevm.instance import Projects, Path_Root, Path_Python, Path_PyScript, Path_CallFrom, Params

pprint({
    "Projects": Projects,
    "Path_Root": Path_Root,
    "Path_Python": Path_Python,
    "Path_PyScript": Path_PyScript,
    "Path_CallFrom": Path_CallFrom,
    "Params": Params
})