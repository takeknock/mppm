import pytest
from packaging.version import Version
from mppm.util import find_minimum_version

@pytest.mark.parametrize("specifier, versions, expected", [
    (">=1.0,<2.0", ["0.9", "1.0", "1.1", "1.5", "2.0", "2.1"], "1.0"),
    (">1.0,<=1.5", ["0.9", "1.0", "1.1", "1.5", "2.0"], "1.1"),
    ("==1.0", ["0.9", "1.0", "1.1"], "1.0"),
    (">=2.0", ["0.9", "1.0", "1.5", "2.0", "2.1"], "2.0"),
    ("<1.0", ["0.8", "0.9", "1.0", "1.1"], "0.8"),
    (">=3.0", ["1.0", "2.0", "2.5"], None),
])
def test_find_minimum_version(specifier, versions, expected):
    result = find_minimum_version(specifier, versions)
    if expected is None:
        assert result is None
    else:
        assert result == expected

def test_find_minimum_version_empty_list():
    assert find_minimum_version(">=1.0", []) is None

def test_find_minimum_version_invalid_specifier():
    with pytest.raises(ValueError):
        find_minimum_version("invalid_specifier", ["1.0", "2.0"])