class TaskReturnTimeout(Exception):
    pass

class MessageTypeError(Exception):
    pass

class TaskProcessingException(Exception):
    def __init__(self, message: str, code: int):
        super().__init__(message)
        self.message = message
        self.code = code


    def __repr__(self):
        f"<TaskProcessingException("
        f"code={self.code}, "
        f"message={self.message!r}, "
        f")>"

    __str__ = __repr__