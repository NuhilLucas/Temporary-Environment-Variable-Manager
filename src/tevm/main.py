from tevm.instance import Projects, Path_Root, Path_Python, Path_PyScript, Path_CallFrom, Params, SourceBat

# from pprint import pprint
# pprint({
#     "Projects": Projects,
#     "Path_Root": Path_Root,
#     "Path_Python": Path_Python,
#     "Path_PyScript": Path_PyScript,
#     "Path_CallFrom": Path_CallFrom,
#     "Params": Params,
#     "SourceBat": SourceBat
# })

if SourceBat.lower()  == "tevm":
    from tevm.cli import Execute
    Execute(Params)
elif not SourceBat in Projects:
    print(f"command {SourceBat} unfind in projects.")
else:
    from tevm.lib.scripter import ps1_build, run
    ps1_build(
        root=Path_Root,
        project=Projects[SourceBat],
        params=Params
    )
    run(cwd=Path_CallFrom)

from tevm.lib.function import sys_exit
sys_exit(0)
