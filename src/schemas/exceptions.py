class BaseShortnererUrlException(Exception):
    pass

class InvalidURLFormatException(BaseShortnererUrlException):
    pass

class InternalDatabaseException(BaseShortnererUrlException):
    pass

class SlugAlreadyExistsException(BaseShortnererUrlException):
    def __init__(self, msg: str):
        self.msg = msg

    def __repr__(self):
        return self.msg