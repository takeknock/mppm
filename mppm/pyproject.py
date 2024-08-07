import os
import subprocess
from platform import python_version
from typing import Any, Dict, List, Optional

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version
from pkg_resources import resource_string
from tomlkit.toml_file import TOMLFile

from .env import MppmEnv
from .util import find_minimum_version


def read_pyproject_text_file():
    try:
        content = resource_string(__name__, 'python_versions.txt')
        text = content.decode('utf-8')
        return text.splitlines()
    except:
        try:
            file_path = "python_versions.txt"
            with open(file_path, 'r') as file:
                versions = file.read().splitlines()
                return versions
        except:
            raise FileNotFoundError("python_versions.txt is not found.")


TOML_FILE_NAME: str = "pyproject.toml"

class PyProjectToml:
    def __init__(self, path: Optional[str] = None):
        file_path: str = os.path.join(path, TOML_FILE_NAME) if path else TOML_FILE_NAME
        toml_file = TOMLFile(file_path)
        self.toml: Dict[str, Any] = toml_file.read()

    def get_mppm_dependencies(self) -> List[Requirement]:
        dependencies: List[str] = self.toml.get("project", {}).get("dependencies", [])
        return [Requirement(x) for x in dependencies]
    
    def get_python_version(self) -> str:
        projects: Optional[str] = self.toml.get("project", {}).get("requires-python")
        systems: str = python_version()
        if projects and systems in SpecifierSet(projects):
            return systems
        try:
            cmd = ["git", "ls-remote", "--tags", "https://github.com/python/cpython.git", "|", "grep", "-v", "'\^{}'", "|", "cut", "-d/", "-f3", "|", "grep", "-E", "'^v[0-9]+\.[0-9]+\.[0-9]+$'"]
            fetchable_python_versions = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE)
            # バイトデータをUTF-8でデコードし、文字列に変換
            decoded_string = fetchable_python_versions.stdout.decode('utf-8')

            # 文字列を行ごとに分割してリストに変換
            version_list = decoded_string.strip().split('\n')
            version_list = [v.lstrip('v') for v in version_list]

        except:
            version_list = read_pyproject_text_file()
            
        if projects and any([v in SpecifierSet(projects) for v in version_list]):
            minimum_required_version = find_minimum_version(projects, version_list)
            return minimum_required_version
        
        raise Exception('Not found requires python version.')