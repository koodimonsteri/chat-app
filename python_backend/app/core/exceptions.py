from sqlalchemy.exc import SQLAlchemyError
# TODO exception handler factory + error codes 

# 404
class ResourceNotFoundError(Exception):
    def __init__(self, message="Resource not found"):
        self.message = message
        super().__init__(self.message)


# 409
class ResoureExists(Exception):
    def __init__(self, message="Resource exists already"):
        self.message = message
        super().__init__(self.message)


# 403
class PermissionError(Exception):
    def __init__(self, message="Not authorized to perform this action"):
        self.message = message
        super().__init__(self.message)


# Maybe extend sqlalchemy?
class DatabaseError(SQLAlchemyError):
    def __init__(self, message="Something happened with database.."):
        self.message = message
        super().__init__(self.message)