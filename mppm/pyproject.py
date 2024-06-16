from platform import python_version
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from tomlkit.toml_file import TOMLFile

class PyProjectToml:

    def __init__(self):
        self.toml = TOMLFile("pyproject.toml").read()

    def get_mppm_dependencies(self):
        dependencies = self.toml["project"]["dependencies"]
        return [Requirement(x) for x in dependencies]
    
    def get_python_version(self):
        projects = self.toml["project"].get("requires-python")
        systems = python_version()
        if projects and systems in SpecifierSet(projects):
            return systems
        raise Exception('Not found requires python version.')
    
