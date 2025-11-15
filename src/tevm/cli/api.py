from typing import Literal
from os.path import exists as Path_Exists, isabs as Path_IsABS, normpath as Path_NormPath
from ..instance import Projects as PROJECTS, Path_ConfigProjects, Root_BatScripts
from ..lib.config_rw import json_write
from ..lib.scripter import bat_build
from ..lib.function import os_remove, ColorPrint as CP

def Execute(): pass
def __help__(): pass
def __gui__(): pass
def __project__(): pass
def __project_gui__(): pass
def __project_list__(): pass
def __project_new__(): pass
def __project_del__(): pass
def __project_modify__(): pass
def __show__(): pass

CMDS: dict[str, dict[str]] = {
    "description": "TEVM, Your Env Manage Helper.",
    "sub": {
        "help": {
            "description": "command help of tevm.",
            "sub": {},
            "call": __help__
        },
        "project": {
            "description": "Project Projects With TEVM.",
            "sub": {
                "gui": {
                    "description": "A Web GUI For User To Project.",
                    "sub": {
                        "-debug": {
                            "description": "Open The Debug Console.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_gui__
                },
                "list": {
                    "description": "List All Project.",
                    "sub": {},
                    "call": __project_list__
                },
                "new": {
                    "description": "Add New Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_new__
                },
                "del": {
                    "description": "Remove Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_del__
                },
                "modify": {
                    "description": "Modfiy Project.",
                    "sub": {
                        "--name": {
                            "description": "Name Of Project.",
                            "sub": {},
                            "call": None
                        }
                    },
                    "call": __project_modify__
                },
            },
            "call": __project__
        }
    },
    "call": Execute
}

def Execute(params: str | list[str]):
    if params.__len__() == 0:
        params.append("help")
    match params[0].lower():
        case "help":
            if params.__len__() == 1:
                __help__(help_level="info")
            else:
                __help__(
                    msg=f"Unknow Command: tevm {" ".join(params)}",
                    help_level="error"
                )
        case "project":
            __project__(params[1:])
        case _:
            __help__(
                msg=f"Unknow Command: tevm {" ".join(params)}",
                help_level="error"
            )

def __help__(
        msg: str | Literal["Unknow Command"] = None,
        help_params: list[str] = [],
        help_level: Literal["error", "warn", "info"] = "info"
    ) -> str:
    if help_level and help_level != "info":
        print(help_level.upper(), end="\n\n")

    if msg:
        print(msg, end="\n\n")
    
    zCMDS = CMDS
    for key in help_params:
        zCMDS = zCMDS["sub"][key]

    print(f'Command:\n    [tevm]{" " if help_params else ""}{" ".join(help_params)}: {zCMDS["description"]}')

    def PrintSub(zCMDS: dict, index: int = 2):
        for key in zCMDS["sub"]:
            print(f'{"    " * index}[{key}]: {zCMDS["sub"][key]["description"]}')
            if zCMDS["sub"][key]["sub"]:
                PrintSub(zCMDS["sub"][key], index+1)
    PrintSub(zCMDS)

def __project__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["project"],
            help_level="info"
        )
        return
    match params[0].lower():
        case "gui":
            __project_gui__(params[1:])
        case "list":
            __project_list__(params[1:])
        case "new":
            __project_new__(params[1:])
        case "del":
            __project_del__(params[1:])
        case "modify":
            __project_modify__(params[1:])
        case _:
            __help__(
                msg=f"Unknow Command: tevm project {" ".join(params)}",
                help_params=["project"],
                help_level="error"
            )

def __project_gui__(params: list[str]):
    from tevm.gui import runGUI
    if params.__len__() == 0:
        runGUI()
    elif params.__len__() == 1 and params[0].lower() == "-debug":
        runGUI(debug=True)
    else:
        __help__(
            msg=f"Unknow Command: tevm project gui {" ".join(params)}",
            help_params=["project", "gui"],
            help_level="error"
        )

def __project_list__(params: list[str]):
    if params.__len__() == 0:
        from tevm.instance import Projects
        print("TEVM Projects List:")
        for ProjectName in Projects:
            print("    " + ProjectName)
    else:
        __help__(
            msg=f"Unknow Command: tevm project gui {" ".join(params)}",
            help_params=["project", "list"],
            help_level="error"
        )

def __project_new__(params: list[str]):
    if params.__len__() > 1:
        __help__(
            msg=f"Unknow Command: tevm project new {" ".join(params)}",
            help_params=["project", "new"],
            help_level="error"
        )
        return

    Project_Name: str = ""
    Project_Data: dict = {
        "executables": {},
        "envars": {}
    }

    # 项目名称
    Project_Name = params[0].lower() if params.__len__() == 1 else ""
    while 1:
        if Project_Name == "":
            Project_Name = input("Project Name: ").lower()
        else:
            print("Project Name: " + Project_Name)

        if Project_Name in PROJECTS:
            CP.print(f"Project {Project_Name} Is Already Exists.")(CP.YELLOW)
            Project_Name = ""
        elif not Project_Name.replace("_", "").isalnum():
            CP.print("Project Name are only allowed to consist of underline, letters and numbers.")(CP.YELLOW)
            Project_Name = ""
        elif Project_Name.startswith("_") or Project_Name[0].isdigit():
            CP.print("Project Name are only allowed to start with letters.")(CP.YELLOW)
            Project_Name = ""
        else:
            break

    # 可执行文件与执行参数
    Executables: dict[str] = {}
    Executable: str = ""
    Executable_Params: str = ""
    print("\nInput <N> To Finish.")
    while 1:
        # 输入接收
        Executable = input("Executable Path: ")
        if Executable[0] == Executable[-1] in ("\"", "'") and Executable.__len__() > 1:
            Executable = Executable[1:-1]


        # 结束输入检查
        if Executable.lower() == "n" and input("Sure The Finish? (y/n)").lower() == "y":
            if Executables:
                break
            else:
                CP.print("Please Specify The Executable File.")(CP.YELLOW)
        # 文件存在性校验
        elif Path_Exists(Executable):
            # 判断相对路径
            if Path_IsABS(Executable):
                Executable = Executable.replace("\\", "/")
            else:
                Executable = "rel|/" + Path_NormPath(Executable).replace("\\", "/")

            # 设置可执行文件执行参数
            Executable_Params = input("Which Parameters Does This Executable File Receive: ")

            # 保存
            Executables[Executable] = Executable_Params
        else:
            CP.print(f"Executable Not Found. [{Executable}]")(CP.YELLOW)
    CP.print("\nExecutables:")(CP.BLUE)
    for Executable, Executable_Params in Executables.items():
        CP.print(f"    {Executable}: {Executable_Params}")(CP.BLUE)

    # 环境变量
    Envars: dict = {}
    Envar_Key: str = ""
    Envar_Value: str = ""
    print("\nInput <N> To Finish.")
    while 1:
        Envar_Key = input("Key Of Envar: ")

        if Envar_Key.lower() == "n" and input("Sure The Finish? (y/n)").lower() == "y":
            break
        elif Envar_Key == "":
            CP.print("Please Specify The Envar Key.")(CP.YELLOW)
        else:
            Envar_Value = input("Value Of Envar: ")
            Envars[Envar_Key] = Envar_Value
    CP.print("\nEnvars:")(CP.BLUE)
    for Envar_Key, Envar_Value in Envars.items():
        CP.print(f"    {Envar_Key}: {Envar_Value}")(CP.BLUE)

    Project_Data["executables"] = Executables
    Project_Data["envars"] = Envars

    # 写入配置文件
    PROJECTS[Project_Name] = Project_Data
    __state__, Projects = json_write(Path_ConfigProjects, PROJECTS)
    if not __state__: print(Projects)

    # 生成bat脚本
    bat_build(Project_Name)

def __project_del__(params: list[str]):
    Project_Name: str = ""
    match params.__len__():
        case 0:
            __help__(
                help_params=["project", "del"],
                help_level="info"
            )
            return
        case 1:
            Project_Name = params[0]
        case _:
            __help__(
                msg=f"Unknow Command: tevm project del {" ".join(params)}",
                help_params=["project", "del"],
                help_level="error"
            )
            return

    if not Project_Name in PROJECTS:
        CP.print(f"Project {Project_Name} Not Exists.")(CP.YELLOW)
    else:
        os_remove(Root_BatScripts + "/" + Project_Name + ".bat")
        PROJECTS.pop(Project_Name)
        __state__, Projects = json_write(Path_ConfigProjects, PROJECTS)
        if not __state__: print(Projects)

def __project_modify__(params: list[str]):
    if params.__len__() == 0:
        __help__(
            help_params=["project", "modify"],
            help_level="info"
        )
        return

    Project_Name: str = params[0].lower()

    if not Project_Name in PROJECTS:
        CP.print(f"Project {Project_Name} Not Exists.")(CP.YELLOW)
        return

if __name__ == "__main__":
    # __help__(msg="123123", help_params=["project"])
    __project_new__(["test", "1"])