# https://git-scm.com/docs/gitignore

from os.path import exists as path_exists, isdir as path_isdir, dirname as get_dirname
from os import listdir as root_listdir, chdir as set_workdir, makedirs, removedirs, remove as file_remove
import zipfile

from pathspec import GitIgnoreSpec

class ReleasePacker():
    def __init__(self, root: str = "."):
        self.root: str = root
        self.version: str = self.get_version()
        self.repignore: GitIgnoreSpec = self.get_rules()
        self.copyneed: list[str] = self.get_copyneed()

    def get_version(self):
        version: str = ""
        with open("./pyproject.toml", "r", encoding="utf-8") as File:
            for line in File.readlines():
                if (version:=line.strip()).lower().startswith("version"):
                    version = version.split("\"")[-2]
                    break
        return version

    def get_rules(self) -> list[str]:
        if path_exists(self.root): set_workdir(self.root)
        self.root = "."

        if not path_exists(self.root + "/.repignore"):
            return GitIgnoreSpec.from_lines([])
        with open(file="./.repignore", mode="r", encoding="utf-8") as File:
            return GitIgnoreSpec.from_lines(File.readlines())

    def check(self, path: str) -> bool:
        return self.repignore.match_file(path)

    def get_copyneed(self):
        copyneed: list[str] = []
        def get_subfiles(root: str):
            subpath: str = ""
            for file in root_listdir(root):
                subpath = root + "/" + file
                if path_isdir(subpath):
                    get_subfiles(subpath)
                else:
                    if not self.check(subpath):
                        copyneed.append(subpath)
        get_subfiles(self.root)
        return copyneed

    def build(self):
        path_zip: str = "./release/tevm_v" + self.version + ".zip"
        print(path_zip)

        if path_exists(path_zip):
            if not input("This Release Already Exists. Do You Want To Overwrite It? (y/n)").lower() == "y": return
            file_remove(path_zip)

        with zipfile.ZipFile(path_zip, 'w', zipfile.ZIP_DEFLATED) as File_ZIP:
            for path in self.copyneed:
                File_ZIP.write(path, path)

if __name__ == "__main__":
    rep: ReleasePacker = ReleasePacker(".")
    rep.build()