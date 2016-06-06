class UserError(Exception):
    def __init__(self, message):
        self.message = message

class UserNotExist(UserError):
    pass

class PasswordIncorrect(UserError):
    pass

class UserIsExist(UserError):
    pass

class EmailNotValid(UserError):
    pass

class RetypePassword(UserError):
    pass