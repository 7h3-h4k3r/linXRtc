from pymongo.errors import DuplicateKeyError

class DuplicateUserError(Exception):
    def __init__(self, message="user credentials already Exits"):
        self.message = message
        super().__init__(self.message)

class NotFoundUserError(Exception):
    def __init__(self, message="Hey! Aura , please signup Before Login"):
        self.message = message
        super().__init__(self.message)

class PasswordError(Exception):
    def __init__(self, message="Incorrect Password !"):
        self.message = message
        super().__init__(self.message)


