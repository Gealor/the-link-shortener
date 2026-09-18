class BaseShortnererUrlException(Exception):
    pass

class InvalidURLFormatException(BaseShortnererUrlException):
    pass

class InternalDatabaseException(BaseShortnererUrlException):
    pass

class OutOfAttemptsForRepeatException(BaseShortnererUrlException):
    pass

class SlugAlreadyExistsException(BaseShortnererUrlException):
    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        return self.msg

class URLBySlugDontExistException(BaseShortnererUrlException):
    pass


class AuthException(Exception):
    pass


class UserNotFoundException(AuthException):
    pass


class NicknameAlreadyExistsException(AuthException):
    pass


class PasswordsNotMatchException(AuthException):
    pass


class UserNotActiveException(AuthException):
    pass


class SessionTokenNotFoundException(AuthException):
    pass


class AuthDatabaseException(AuthException):
    pass
