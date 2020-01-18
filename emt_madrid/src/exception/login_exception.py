class LoginException(Exception):
    def __init__(self, message):
        super(LoginException, self).__init__(message)
