import os
import subprocess
from typing import Dict, Any, Optional, List

from platform import python_version
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from tomlkit.toml_file import TOMLFile

from .env import MppmEnv

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
            cmd = "git ls-remote --tags https://github.com/python/cpython.git | grep -v '\^{}' | cut -d/ -f3 | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$'"
            fetchable_python_versions = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE)
            # バイトデータをUTF-8でデコードし、文字列に変換
            decoded_string = fetchable_python_versions.stdout.decode('utf-8')

            # 文字列を行ごとに分割してリストに変換
            version_list = decoded_string.strip().split('\n')
        except:
            def read_versions_to_list(file_path):
                with open(file_path, 'r') as file:
                    versions = file.read().splitlines()
                    return versions

            # ファイルパスを指定
            file_path = 'python_versions.txt'

            # 関数を呼び出してバージョンリストを取得
            version_list = read_versions_to_list(file_path)
        if projects and version_list in SpecifierSet(projects):
            minimum_required_version = ""
            MppmEnv.install_python(minimum_required_version)

        raise Exception('Not found requires python version.')