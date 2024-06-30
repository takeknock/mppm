from mppm.main_impl import *
from mppm.pyproject import PyProjectToml


def test_lock():
    toml = PyProjectToml("test/conf/python_version/311")
    lock_impl(toml)

