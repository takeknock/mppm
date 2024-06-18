import json

class Locker:
    @staticmethod
    def lock(candidates):
        info = {}
        for k, v in candidates.items():
            info[k] = {
                "name": k,
                "version": v.version,
                "url": v.url,
                "hashes": v.hashes,
                "core_metadata": v.core_metadata
            }
        with open("mppm.lock", "w") as f:
            return json.dump(info, f, indent=4)
    
    @staticmethod
    def read():
        with open("mppm.lock", "r") as f:
            return json.load(f)