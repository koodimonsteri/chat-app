


class ResourceNotFoundError(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)


class PermissionError(Exception):
    def __init__(self, message="Not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)


# Maybe extend sqlalchemy?
class DatabaseError(Exception):
    def __init__(self, message="Something happened with database.."):
        self.message = message
        super().__init__(self.message)