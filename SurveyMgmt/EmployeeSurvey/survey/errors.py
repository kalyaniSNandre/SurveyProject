class PasswordError(Exception):

    def __init__(self, password):
        self.password = password


