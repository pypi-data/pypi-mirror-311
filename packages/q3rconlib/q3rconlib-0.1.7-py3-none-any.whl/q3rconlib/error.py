class Q3RconLibError(Exception):
    """Base Q3RconLib error class"""


class Q3RconLibLoginError(Q3RconLibError):
    """Exception raised when a bad rcon login attempt is made"""

    err_msg = {
        1: "Invalid rcon password.",
        2: "Unable to contact the server, perhaps it's down?",
        3: "No rcon password set on server or password is shorter than 8 characters.",
    }

    def __init__(self, code):
        self.code = code
        super().__init__(self.err_msg[self.code])
