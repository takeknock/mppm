from operator import attrgetter
import requests
from packaging.specifiers import SpecifierSet
from packaging.tags import sys_tags
from packaging.utils import canonicalize_name, parse_wheel_filename
from resolvelib import AbstractProvider

from .candidate import Candidate

class Provider(AbstractProvider):
    def __init__(self, python_version):
        self.python_version = python_version
    
    def find_matches(self, identifier, requirements, incompatibilities):
        data = requests.get(
            f"https://pypi.org/simple/{identifier}",
            headers={"Accept":"application/vnd.pypi.simple.v1+json"}
        ).json()
    
        candidates = []

        source_specifiers = [r.specifier for r in requirements[identifier]]

        bad_versions = {c.version for c in incompatibilities[identifier]}

        fp = ''.join(self.python_version.split('.')[:2])
        py = {f"cp{fp}", f"py{fp}", f"py{fp[0]}"}
        system_tags = {x for x in sys_tags() if x.interpreter in py}

        for d in data["files"]:
            if not d['url'].endswith('.whl'):
                continue
            
            requires_python = d['requires-python']
            if requires_python and self.python_version not in SpecifierSet(requires_python):
                continue
            name, version, _, tags = parse_wheel_filename(d['filename'])

            if not tags & system_tags:
                continue

            if version not in bad_versions and all(version in x for x in source_specifiers):
                c = Candidate(
                    name,
                    version,
                    d['url'],
                    d['hashes'],
                    d['core-metadata']
                )
                candidates.append(c)
        return sorted(candidates, key=attrgetter("version"), reverse=True)

    def identify(self, requirement_or_candidate):
        return canonicalize_name(requirement_or_candidate.name)

    def is_satisfied_by(self, requirement, candidate):
        if canonicalize_name(requirement.name) != candidate.name:
            return False
        return candidate.version in requirement.specifier

    def get_preference(self, identifier, resolutions, candidates, information, backtrack_causes):
        return sum(1 for _ in candidates[identifier])

    def get_dependencies(self, candidate):
        return candidate.get_dependencies()