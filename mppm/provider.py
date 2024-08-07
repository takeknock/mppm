from operator import attrgetter
from typing import Any, Dict, Iterator, List, Mapping, Sequence, Set

import requests
from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.tags import Tag, sys_tags
from packaging.utils import canonicalize_name, parse_wheel_filename
from packaging.version import Version
from resolvelib import AbstractProvider
from resolvelib.resolvers import RequirementInformation

from .candidate import Candidate


class Provider(AbstractProvider):
    def __init__(self, python_version: str):
        self.python_version: str = python_version
    
    def find_matches(
        self,
        identifier: Any,
        requirements: Mapping[str, Iterator[Requirement]],
        incompatibilities: Mapping[str, Iterator[Candidate]]
    ) -> List[Candidate]:
        data: Dict[str, Any] = requests.get(
            f"https://pypi.org/simple/{identifier}",
            headers={"Accept":"application/vnd.pypi.simple.v1+json"}
        ).json()
    
        candidates: List[Candidate] = []

        source_specifiers: List[SpecifierSet] = [r.specifier for r in requirements[identifier]]

        bad_versions: Set[str] = {c.version for c in incompatibilities[identifier]}

        fp: str = ''.join(self.python_version.split('.')[:2])
        py: Set[str] = {f"cp{fp}", f"py{fp}", f"py{fp[0]}"}
        system_tags: Set[Tag] = {x for x in sys_tags() if x.interpreter in py}

        for d in data["files"]:
            if not d['url'].endswith('.whl'):
                continue
            
            requires_python: str = d['requires-python']
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

    def identify(self, requirement_or_candidate: Any) -> str:
        return canonicalize_name(requirement_or_candidate.name)

    def get_preference(
        self,
        identifier: str,
        resolutions: Mapping[str, Any],
        candidates: Mapping[str, Iterator[Candidate]],
        information: Mapping[str, Iterator[RequirementInformation]],
        backtrack_causes: Sequence[RequirementInformation]
    ) -> int:
        return sum(1 for _ in candidates[identifier])

    def get_dependencies(self, candidate: Candidate) -> List[Requirement]:
        return candidate.get_dependencies()

    def is_satisfied_by(self, requirement: Requirement, candidate: Candidate) -> bool:
        if canonicalize_name(requirement.name) != candidate.name:
            return False
        return candidate.version in requirement.specifier