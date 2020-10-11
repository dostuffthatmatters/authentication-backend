
def validate_password_format(password: str):
    try:
        assert(8 <= len(password))
        assert(len(password) <= 32)
        assert(any([c.isnumeric() for c in password]))
        assert(any([c.isalpha() for c in password]))
        assert(any([not (c.isnumeric() or c.isalpha()) for c in password]))
        return True
    except AssertionError:
        return False


if __name__ == '__main__':
    assert(not validate_password_format("sda"))
    assert(validate_password_format("sdasdad8!"))
