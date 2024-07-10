import os
import subprocess
from typing import List, Dict

from virtualenv import cli_run


class MppmEnv:
    @staticmethod
    def create(python_version: str) -> None:
        cli_run([".mppmenv", f"--python={python_version}"])

    @staticmethod
    def install(package: str) -> None:
        env: Dict[str, str] = os.environ.copy()
        env["PATH"] = os.pathsep.join([".mppmenv/bin", env["PATH"]])
        cmd: List[str] = ["pip", "install", package, "--no-deps"]
        subprocess.run(cmd, env=env, check=True)

    @staticmethod
    def run(args: List[str]) -> None:
        env: Dict[str, str] = os.environ.copy()
        env["PATH"] = os.pathsep.join([".mppmenv/bin", env["PATH"]])
        print(f"args: {args}")
        subprocess.run(args, env=env, check=True)

    @staticmethod
    def install_python(python_version: str) -> None:
        pass