from io import BytesIO
from typing import Any, Dict, List, Optional, Tuple
from zipfile import ZipFile

import requests  # type: ignore
from packaging.metadata import RawMetadata, parse_email
from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version


class Candidate:
    def __init__(self, name: str, version: Version, url: str, hashes: Dict[str, str], core_metadata: str):
        self.name: str = canonicalize_name(name)
        self.version: str = str(version)
        self.url: str = url
        self.hashes: Dict[str, str] = hashes
        self.core_metadata: str = core_metadata
        self.metadata: Optional[RawMetadata] = None
        self.dependencies: Optional[List[Requirement]] = None

    @staticmethod
    def _get_metadata(url: str) -> Tuple[RawMetadata, Dict[str, List[str]]]:
        with ZipFile(BytesIO(requests.get(url).content)) as z:
            for n in z.namelist():
                if n.endswith(".dist-info/METADATA"):
                    return parse_email(z.open(n).read())
        return RawMetadata(), {}

    def get_dependencies(self) -> List[Requirement]:
        if self.metadata is None:
            self.metadata, _ = self._get_metadata(self.url)
        if self.dependencies is None:
            requires_dist: Any = self.metadata.get("Requires-Dist")
            if requires_dist is not None:
                deps: List[Requirement] = [Requirement(d) for d in requires_dist]
                self.dependencies = [d for d in deps if d.marker is None]
            else:
                self.dependencies = []
        return self.dependencies