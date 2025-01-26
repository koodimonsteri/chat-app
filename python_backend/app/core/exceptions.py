


class ResourceNotFoundError(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)


class PermissionError(Exception):
    def __init__(self, message="Not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)

