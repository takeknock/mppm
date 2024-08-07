from typing import List

from packaging.specifiers import SpecifierSet
from packaging.version import Version


def find_minimum_version(specifier_set: str, available_versions: List[str]) -> Version:
    spec = SpecifierSet(specifier_set)
    valid_versions = [v for v in available_versions if v in spec]
    if not valid_versions:
        return None
    return min(valid_versions, key=Version)

