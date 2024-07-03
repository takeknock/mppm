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

    @staticmethod
    def install_python(python_version):
        cmd = "git ls-remote --tags https://github.com/python/cpython.git | grep -v '\^{}' | cut -d/ -f3 | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -r"
        subprocess.run(cmd, check=True)
