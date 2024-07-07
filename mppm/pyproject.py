import os
from typing import Dict, Any, Optional, List

from platform import python_version
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from tomlkit.toml_file import TOMLFile

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
        raise Exception('Not found requires python version.')