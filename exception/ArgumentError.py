class ArgumentError(Exception):
    def __init__(self, reason: str):
        super().__init__(self)
        self.reason = reason

    def __str__(self):
        return self.reason
