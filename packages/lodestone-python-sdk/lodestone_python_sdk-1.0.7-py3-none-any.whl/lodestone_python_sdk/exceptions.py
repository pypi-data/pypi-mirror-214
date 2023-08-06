class AuthException(Exception):
    pass

class AppAuthException(AuthException):
    pass

class UserAuthException(AuthException):
    pass
