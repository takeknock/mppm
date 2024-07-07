import json
from typing import Dict, Any, Mapping

class Locker:
    @staticmethod
    def lock(candidates: Mapping[Any, Any]) -> None:
        info: Dict[str, Dict[str, Any]] = {}
        for k, v in candidates.items():
            info[k] = {
                "name": k,
                "version": v.version,
                "url": v.url,
                "hashes": v.hashes,
                "core_metadata": v.core_metadata
            }
        with open("mppm.lock", "w") as f:
            json.dump(info, f, indent=4)

    @staticmethod
    def read() -> Dict[str, Any]:
        with open("mppm.lock", "r") as f:
            return json.load(f)