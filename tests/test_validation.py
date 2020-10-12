
from app.utilities.validating import validate_password_format


def test_password_format():
    assert(not validate_password_format("abc"))
    assert(not validate_password_format("abcabcabc"))
    assert(not validate_password_format("123123123"))
    assert(not validate_password_format("!?!?!?!?!"))
    assert(not validate_password_format("abc123abc"))
    assert(not validate_password_format("abc!?!abc"))
    assert(not validate_password_format("123!?!123"))
    assert(validate_password_format("sdasdad8!"))
