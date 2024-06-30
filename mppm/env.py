import os
import subprocess

from virtualenv import cli_run


class MppmEnv:
    @staticmethod
    def create(python_version):
        cli_run([".mppmenv", f"--python={python_version}"])

    @staticmethod
    def install(package):
        env = os.environ.copy()
        env["PATH"] = os.pathsep.join([".mppmenv/bin", env["PATH"]])
        cmd = ["pip", "install", package, "--no-deps"]
        subprocess.run(cmd, env=env, check=True)

    @staticmethod
    def run(args):
        env = os.environ.copy()
        env["PATH"] = os.pathsep.join([".mppmenv/bin", env["PATH"]])
        subprocess.run(args, env=env, check=True)

