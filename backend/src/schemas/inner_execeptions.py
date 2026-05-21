class BaseInnerException(Exception):
    pass

class RedisStartupException(BaseInnerException):
    pass

class DatabaseStartupException(BaseInnerException):
    pass