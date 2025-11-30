class BusinessException(Exception):
    """Base exception for business logic errors"""
    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class ValidationException(BusinessException):
    """Raised when input validation fails"""
    pass


class NotFoundError(BusinessException):
    """Raised when a requested resource is not found"""
    pass


class ConflictError(BusinessException):
    """Raised when there's a conflict with existing data"""
    pass


class DatabaseError(BusinessException):
    """Raised when database operations fail"""
    pass