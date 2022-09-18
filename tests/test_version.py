import re

def test_version() -> None:
    from oooscript import __version__
    regex = r"^\d+.\d+.\d+$"
    
    ver_match = re.match(regex, __version__)
    assert ver_match is not None
    