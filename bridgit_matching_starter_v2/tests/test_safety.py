from src.safety import contains_protected
def test_contains():
    assert contains_protected("mentions religion")
    assert not contains_protected("plain text")
